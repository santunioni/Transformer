from typing import Any

from aiokafka import ConsumerRecord, AIOKafkaConsumer

from src.the_flash.adapters.abstract_bridges import ConsumerBridge
from src.the_flash.application import Application


class KafkaConsumerBridge(ConsumerBridge[ConsumerRecord]):

    def __init__(self, application: Application, aio_consumer: AIOKafkaConsumer):
        super().__init__(application, aio_consumer)

    def extract_data(self, payload: ConsumerRecord) -> Any:
        return payload.value
