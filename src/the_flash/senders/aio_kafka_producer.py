from aiokafka import AIOKafkaProducer
from aiokafka.structs import RecordMetadata

from src.models.mat_events import ServiceResponse


class AIOProducerKafkaAdapter:
    """
    This is the concrete implementation of a Producer that sends transformed data to the TheServices.
    """

    def __init__(self, topic: str, aio_kafka_producer: AIOKafkaProducer):
        """
        :param topic: The transaction topic in the Kafka broker on TheFlash service where the
        transformed data will be sent.
        :param aio_kafka_producer: The object from AIOKafka that makes the producer connection.
        """
        self.__topic = topic
        self.__aio_kafka_producer = aio_kafka_producer

    async def send(self, response: ServiceResponse) -> RecordMetadata:
        """
        This method sends the transformed data to TheFlash services.
        :param response: The transformed data.
        :return: Metadata about the process of storing messages on a kafka topic.
        """
        return await self.__aio_kafka_producer.send_and_wait(self.__topic, response.json().encode("utf-8"))
