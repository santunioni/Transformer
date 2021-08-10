import logging
from asyncio import Queue

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, ConsumerRecord
from pydantic import ValidationError

from src.models.mat_events import ServiceLetter, ServiceResponse

logger = logging.getLogger(__name__)


async def kafka_produce(topic: str, response_producer: AIOKafkaProducer, responses: Queue[ServiceResponse]):
    while True:
        service_response = await responses.get()
        await response_producer.send(topic=topic, value=service_response)
        responses.task_done()
        logger.info("Sent: %s", service_response.event_trace)


async def kafka_consume(letter_consumer: AIOKafkaConsumer, letters: Queue[ServiceLetter]):
    async for msg in letter_consumer:  # type: ConsumerRecord
        logger.debug(
            "Received message from Kafka: topic=%s, partition=%s, offset=%s, key=%s, value=%s, timestamp=%s",
            msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp
        )
        try:
            service_letter = ServiceLetter.parse_raw(msg.value)
            logger.info("Received: %s", service_letter.event_trace)
            await letters.put(service_letter)
        except ValidationError as err:
            logger.error("Got ValidationError while parsing message. Check traceback: %s", err)
