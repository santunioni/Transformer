import asyncio
import contextlib
import logging
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from dotenv import load_dotenv, find_dotenv

# / ---------------------------------------- CONFIGS ---------------------
from src.the_flash.feeders.consumer_feeders.aiokafka.factory import kafka_factory, KafkaSettings
from tests.factory.letter_factory import letter_gen

logger = logging.getLogger(__name__)


@lru_cache
async def get_producer() -> AIOKafkaProducer:
    _, producer = kafka_factory(KafkaSettings())
    await contextlib.AsyncExitStack().enter_async_context(producer)
    return producer


async def send_sequence(number: int):
    producer = await get_producer()
    for letter in letter_gen(number):
        await producer.send_and_wait(
            topic=KafkaSettings().KAFKA_TOPIC_FIELD_TRANSLATOR,
            value=letter.json().encode("utf-8")
        )


async def send_parallel(number: int):
    producer = await get_producer()
    await asyncio.gather(*[
        producer.send_and_wait(
            topic=KafkaSettings().KAFKA_TOPIC_FIELD_TRANSLATOR,
            value=letter
        ) for letter in letter_gen(number)
    ])


if __name__ == "__main__":
    load_dotenv(
        find_dotenv(
            filename="local.env",
            raise_error_if_not_found=True))
    try:
        asyncio.run(send_sequence(1))
    except BaseException as e:
        print(e)
        print("Shutting down.")
