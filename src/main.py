import asyncio
import logging
from asyncio import Queue
from typing import Tuple

from src.settings import EnvironmentSettings
from src.the_flash.abstractions.aio_comunicators import AIOProducer
from src.the_flash.adapters.aiokafka.aiokafkaconsumer import KafkaConsumerBridge
from src.the_flash.adapters.aiokafka.aiokafkaproducer import AIOProducerKafkaAdapter
from src.the_flash.adapters.aiokafka.factory import kafka_factory, KafkaSettings
from src.the_flash.application import Application

logger = logging.getLogger(__name__)


def pieces(settings: EnvironmentSettings) -> Tuple[Application, KafkaConsumerBridge]:
    kafka_settings = KafkaSettings()
    consumer, producer = kafka_factory(kafka_settings)
    producer_adapter: AIOProducer = AIOProducerKafkaAdapter(
        aio_kafka_producer=producer,
        topic=kafka_settings.KAFKA_TOPIC_SERVICE_RESPONSE
    )

    app: Application = Application(
        aio_producer=producer_adapter,
        queue=Queue(maxsize=settings.MAX_CONCURRENT_MESSAGES)
    )
    entrypoint: KafkaConsumerBridge = KafkaConsumerBridge(
        application=app,
        aio_consumer=consumer
    )
    return app, entrypoint


async def main(settings: EnvironmentSettings):
    app, entrypoint = pieces(settings)
    async with app, entrypoint:
        app.increase_tasks(settings.CONCURRENT_TASKS)
        await asyncio.gather(*app.tasks, entrypoint.consume())
        await app.queue.join()

    for task in app.tasks:
        task.cancel()


if __name__ == "__main__":
    environment_settings = EnvironmentSettings()
    asyncio.run(main(environment_settings))
