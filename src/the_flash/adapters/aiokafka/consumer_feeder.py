from typing import Union

from aiokafka import AIOKafkaConsumer, ConsumerRecord

from src.the_flash.adapters.abstract_feeders import ConsumerFeeder
from src.the_flash.application import Application


class KafkaConsumerFeeder(ConsumerFeeder):

    def __init__(self, application: Application, aio_consumer: AIOKafkaConsumer):
        super().__init__(application, aio_consumer)

    def extract_data(self, payload: ConsumerRecord) -> Union[str, bytes, dict]:
        return payload.value
