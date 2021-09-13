import asyncio
import logging
from asyncio import Queue

from src.models.mat_events import ServiceLetter, ServiceResponse
from src.settings import EnvironmentSettings

logger = logging.getLogger(__name__)


async def main(settings: EnvironmentSettings):
    letter_consumer, response_producer = kafka_factory(settings)

    letters: Queue[ServiceLetter] = Queue(maxsize=settings.NUMBER_OF_MAX_CONCURRENT_MESSAGES)
    responses: Queue[ServiceResponse] = Queue()

    processors = [
        asyncio.create_task(
            process_message(letters, responses)
        ) for _ in range(settings.NUMBER_OF_CONCURRENT_SERVICE_CALLS)
    ]
    async with letter_consumer, response_producer:
        consumer = asyncio.create_task(kafka_consume(letter_consumer, letters))

        await asyncio.gather(consumer, *processors)
        await letters.join()
        await responses.join()

    for looper in processors:
        looper.cancel()


if __name__ == "__main__":
    environment_settings = EnvironmentSettings()
    asyncio.run(main(environment_settings))
