import asyncio
import json
import logging
import random
import statistics
import time
import uuid
from collections import deque
from typing import Dict, Tuple, Any, Deque

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.helpers import create_ssl_context
from dotenv import load_dotenv, find_dotenv
from pydantic import ValidationError

from src.models.mat_events import ServiceLetter, ServiceResponse
from src.settings import EnvironmentSettings
# / ---------------------------------------- CONFIGS ----------------------------------------
from tests.factory.letter_factory import letter_factory, config_factory

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:%(lineno)s - %(message)s',
                    level=logging.INFO)


async def kafka_produce(topic: str, letter_producer: AIOKafkaProducer, letters: Dict[str, float], number: int):
    for _ in range(number):
        service_letter = ServiceLetter(
            event_trace=str(uuid.uuid4()),
            mat_identifier="field_translator",
            data=letter_factory(),
            config=config_factory()
        )
        logger.info("Data sent: %s", service_letter.dict())
        await letter_producer.send_and_wait(topic=topic, value=service_letter)
        logger.info("Sent: %s", service_letter.event_trace)
        letters[service_letter.event_trace] = time.time()


async def kafka_consume(response_consumer: AIOKafkaConsumer, responses: Dict[str, float], timing: Deque[float],
                        messages_sent: int):
    counter = 1
    async for msg in response_consumer:
        try:
            service_response: ServiceResponse = msg.value
            responses[service_response.event_trace] = time.time()
            timing.append(service_response.stats.duration)
            logger.info("Received: %s", service_response.event_trace)
        except ValidationError as err:
            logger.error(
                "Got ValidationError while parsing message. Check traceback: %s", err)

        counter += 1
        if counter - messages_sent > 0:
            break


async def main(settings: EnvironmentSettings, number_of_producers: int, number_of_messages: int):
    first_boostrap_server_is_localhost: bool = settings.KAFKA_BOOTSTRAP_SERVERS.split(":")[
        0].lower() == "localhost"
    response_consumer = AIOKafkaConsumer(
        *settings.KAFKA_TOPIC_FIELD_TRANSLATOR.split(","),
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_TOPIC_FIELD_TRANSLATOR,
        value_deserializer=ServiceResponse.parse_raw,
        security_protocol="PLAINTEXT" if first_boostrap_server_is_localhost else "SSL",
        ssl_context=None if first_boostrap_server_is_localhost else create_ssl_context()
    )
    letter_producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v.dict()).encode('utf-8'),
        security_protocol="PLAINTEXT" if first_boostrap_server_is_localhost else "SSL",
        ssl_context=None if first_boostrap_server_is_localhost else create_ssl_context()
    )

    letters: Dict[str, float] = {}
    responses: Dict[str, float] = {}
    timing: Deque[float] = deque()
    async with response_consumer, letter_producer:
        try:
            consumer = asyncio.create_task(
                kafka_consume(
                    response_consumer=response_consumer,
                    responses=responses,
                    timing=timing,
                    messages_sent=number_of_messages
                )
            )
            producers = [asyncio.create_task(
                kafka_produce(
                    topic=settings.KAFKA_TOPIC_FIELD_TRANSLATOR,
                    letter_producer=letter_producer,
                    letters=letters,
                    number=number_of_messages // number_of_producers
                )) for _ in range(number_of_producers)]

            await asyncio.gather(consumer, *producers)
        except BaseException:
            pass

        print("\n\nCollecting results: ")
        print()
        print(f"Numbers of producers:\t\t{number_of_producers}")
        print(f"Messages per producer:\t\t{number_of_messages}")
        print(f"Service processing mean:\t{statistics.mean(timing):.3f}" +
              u"\u00B1" + f"{statistics.variance(timing):.3f}s")
        print()
        print(f"Messages sent:\t\t{len(letters)}")
        print(f"Messages received:\t{len(responses)}")
        delays = [responses[key] - letters[key] for key in letters.keys()]
        print(f"Response time:\t{statistics.mean(delays):.3f}" +
              u"\u00B1" + f"{statistics.stdev(delays):.3f}s")
        print(f"Normalized time:\t{1000*statistics.mean(delays)/len(letters):.3f}" +
              u"\u00B1" + f"{1000*statistics.stdev(delays)/len(letters):.3f}ms")
        print("\n")


if __name__ == "__main__":
    load_dotenv(find_dotenv(filename="local.env",
                raise_error_if_not_found=True))
    environment_settings = EnvironmentSettings()
    print(environment_settings)
    try:
        asyncio.run(main(environment_settings,
                    number_of_producers=1, number_of_messages=1))
    except BaseException as e:
        print(e)
        print("Shutting down.")
