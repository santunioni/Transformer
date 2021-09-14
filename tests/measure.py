import asyncio
import logging
import uuid

from dotenv import load_dotenv, find_dotenv

from src.models.mat_events import ServiceLetter
# / ---------------------------------------- CONFIGS ----------------------------------------
from src.the_flash.feeders.consumer_feeders.aiokafka.factory import kafka_factory, KafkaSettings
from tests.factory.letter_factory import data_factory, config_factory

logger = logging.getLogger(__name__)


def letter_gen(number: int):
    for _ in range(number):
        yield ServiceLetter(
            event_trace=str(uuid.uuid4()),
            mat_id="field_translator",
            data=data_factory(),
            config=config_factory(),
            index_in_flow=0
        )


async def main(number_of_messages: int):
    _, producer = kafka_factory(KafkaSettings())
    async with producer:
        for letter in letter_gen(number_of_messages):
            await producer.send_and_wait(
                topic=KafkaSettings().KAFKA_TOPIC_FIELD_TRANSLATOR,
                value=letter.json().encode("utf-8")
            )


if __name__ == "__main__":
    load_dotenv(find_dotenv(filename="local.env", raise_error_if_not_found=True))
    try:
        asyncio.run(main(1000))
    except BaseException as e:
        print(e)
        print("Shutting down.")
