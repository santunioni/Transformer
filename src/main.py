import asyncio
import logging
from asyncio import Queue
from contextlib import asynccontextmanager
from typing import Tuple, AsyncIterator

import uvloop

from src.the_flash.application import Application
from src.the_flash.feeders.abstract_feeders import ConsumerImplementation
from src.the_flash.feeders.consumer_feeders.aiokafka.factory import KafkaSettings, kafka_factory
from src.the_flash.feeders.consumer_feeders.aiokafka.kafka_feeder import KafkaFeeder
from src.the_flash.senders.aio_kafka_producer import AIOProducerKafkaAdapter
from src.the_flash.senders.aio_producer import AIOProducer
from src.the_flash.settings import EnvironmentSettings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def instantiate_pieces(settings: EnvironmentSettings) -> AsyncIterator[Tuple[Application,
                                                                                   ConsumerImplementation]]:
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
    feeder: ConsumerImplementation = KafkaFeeder(
        application=app,
        aio_consumer=consumer
    )

    async with producer, consumer:
        yield app, feeder


async def main(settings: EnvironmentSettings):
    async with instantiate_pieces(settings) as pieces:
        app, feeder = pieces
        app.process_tasks(settings.CONCURRENT_TASKS)
        await asyncio.gather(feeder.consume(), *app.tasks)
        await app.queue.join()

    for task in app.tasks:
        task.cancel()


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main(EnvironmentSettings()))
