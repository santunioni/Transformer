import asyncio
import contextlib
import logging
import uuid

from dotenv import load_dotenv, find_dotenv

from src.models.mat_events import ServiceLetter
# / ---------------------------------------- CONFIGS ----------------------------------------
from src.the_flash.feeders.consumer_feeders.aiokafka.factory import kafka_factory, KafkaSettings
from tests.factory.letter_factory import data_factory, config_factory

logger = logging.getLogger(__name__)
from aiocache import cached


@cached()
async def get_producer():
    _, producer = kafka_factory(KafkaSettings())
    await contextlib.AsyncExitStack().enter_async_context(producer)
    return producer


def letter_gen(number: int):
    for _ in range(number):
        yield ServiceLetter(
            event_trace=str(uuid.uuid4()),
            mat_id="field_translator",
            data=data_factory(),
            config=config_factory(),
            index_in_flow=0
        ).json().encode("utf-8")


async def send_sequence(number: int):
    producer = await get_producer()
    for letter in letter_gen(number):
        await producer.send_and_wait(
            topic=KafkaSettings().KAFKA_TOPIC_FIELD_TRANSLATOR,
            value=letter
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
    load_dotenv(find_dotenv(filename="local.env", raise_error_if_not_found=True))
    try:
        asyncio.run(send_sequence(1000))
    except BaseException as e:
        print(e)
        print("Shutting down.")
