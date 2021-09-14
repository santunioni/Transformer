from typing import Any

from aiokafka import ConsumerRecord, AIOKafkaConsumer


from src.the_flash.application import Application
from src.the_flash.feeders.abstract_feeders import ConsumerImplementation


class KafkaFeeder(ConsumerImplementation[ConsumerRecord]):
    """
    The Kafka feeder i
    """

    def __init__(self, application: Application, aio_consumer: AIOKafkaConsumer):
        super().__init__(application, aio_consumer)

    def extract_data(self, payload: ConsumerRecord) -> Any:
        return payload.value
