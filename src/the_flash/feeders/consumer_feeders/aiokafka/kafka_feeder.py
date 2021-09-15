from typing import Union

from aiokafka import ConsumerRecord, AIOKafkaConsumer

from src.the_flash.application import Application
from src.the_flash.feeders.abstract_feeders import ConsumerImplementation


class KafkaFeeder(ConsumerImplementation):
    """
    The Kafka feeder implements the Kafka feeding method.
    """

    def __init__(self, application: Application,
                 aio_consumer: AIOKafkaConsumer):
        super().__init__(application, aio_consumer)

    def extract_data(self, payload: ConsumerRecord) -> Union[str, bytes, dict]:
        """
        Kafka feeding method requires the relevant data to be extracted like so.
        :param payload: Complete data.
        :return: Relevant data.
        """
        return payload.value
