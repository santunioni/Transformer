from aiokafka import AIOKafkaProducer
from aiokafka.structs import RecordMetadata

from src.models.mat_events import ServiceResponse


class AIOProducerKafkaAdapter:

    def __init__(self, topic: str, aio_kafka_producer: AIOKafkaProducer):
        self.__topic = topic
        self.__aio_kafka_producer = aio_kafka_producer

    async def __aenter__(self):
        await self.__aio_kafka_producer.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.__aio_kafka_producer.stop()

    async def send(self, response: ServiceResponse) -> RecordMetadata:
        return await self.__aio_kafka_producer.send_and_wait(self.__topic, response.json().encode("utf-8"))