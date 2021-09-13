from typing import Any

from aiokafka import AIOKafkaConsumer

from src.the_flash.adapters.abstract_bridges import ConsumerBridge
from src.the_flash.application import Application


class KafkaConsumerBridge(ConsumerBridge):

    def __init__(self, application: Application, aio_consumer: AIOKafkaConsumer):
        super().__init__(application, aio_consumer)
        self.__aio_consumer = aio_consumer

    def extract_data(self, payload) -> Any:
        return payload.value

    async def __aenter__(self):
        await self.__aio_consumer.start()

    async def __aexit__(self, exc_type, exc, tb):
        await self.__aio_consumer.stop()
