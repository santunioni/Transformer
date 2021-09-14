import asyncio
import logging
from asyncio import Queue
from contextlib import asynccontextmanager
from typing import Tuple, AsyncIterator

import uvloop

from src.settings import EnvironmentSettings
from src.the_flash.abstractions.aio_comunicators import AIOProducer
from src.the_flash.adapters.abstract_feeders import ConsumerFeeder
from src.the_flash.adapters.aiokafka.aio_producer_adapter import AIOProducerKafkaAdapter
from src.the_flash.adapters.aiokafka.consumer_feeder import KafkaConsumerFeeder
from src.the_flash.adapters.aiokafka.factory import kafka_factory, KafkaSettings
from src.the_flash.application import Application

logger = logging.getLogger(__name__)


@asynccontextmanager
async def instantiate_pieces(settings: EnvironmentSettings) -> AsyncIterator[Tuple[Application, ConsumerFeeder]]:
    kafka_settings = KafkaSettings()
    consumer, producer = kafka_factory(kafka_settings)
    producer_adapter: AIOProducer = AIOProducerKafkaAdapter(
        aio_kafka_producer=producer,
        topic=kafka_settings.KAFKA_TOPIC_SERVICE_RESPONSE
    )
    app = Application(
        aio_producer=producer_adapter,
        queue=Queue(maxsize=settings.MAX_CONCURRENT_MESSAGES)
    )
    feeder: ConsumerFeeder = KafkaConsumerFeeder(
        application=app,
        aio_consumer=consumer
    )

    async with producer, consumer:
        yield app, feeder


async def main(settings: EnvironmentSettings):
    async with instantiate_pieces(settings) as pieces:
        app, feeder = pieces
        app.increase_tasks(settings.CONCURRENT_TASKS)
        await asyncio.gather(feeder.consume(), *app.tasks)
        await app.queue.join()

    for task in app.tasks:
        task.cancel()


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main(EnvironmentSettings()))
