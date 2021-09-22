import asyncio
import contextlib
import logging
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from dotenv import load_dotenv, find_dotenv

# / ---------------------------------------- CONFIGS ---------------------
from the_flash.builder.suplies.kafka_factory import KafkaSettings

from tests.factory.letter_factory import letter_gen

logger = logging.getLogger(__name__)


@lru_cache
async def get_producer() -> AIOKafkaProducer:
    producer = KafkaSettings().get_producer()
    await contextlib.AsyncExitStack().enter_async_context(producer)
    return producer


async def send_sequence(number: int):
    producer = await get_producer()
    for letter in letter_gen(number):
        await producer.send_and_wait(
            topic=KafkaSettings().KAFKA_CONSUMER_TOPIC,
            value=letter.json().encode("utf-8")
        )


async def send_parallel(number: int):
    producer = await get_producer()
    await asyncio.gather(*[
        producer.send_and_wait(
            topic=KafkaSettings().KAFKA_CONSUMER_TOPIC,
            value=letter.json().encode("utf-8")
        ) for letter in letter_gen(number)
    ])


if __name__ == "__main__":
    load_dotenv(
        find_dotenv(
            filename="local.env",
            raise_error_if_not_found=True))
    try:
        asyncio.run(send_parallel(1000))
    except BaseException as e:
        print(e)
        print("Shutting down.")
