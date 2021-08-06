import logging

from pydantic import BaseSettings

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:%(lineno)s - %(message)s',
    level=logging.INFO
)


class EnvironmentSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_FIELD_TRANSLATOR: str
    KAFKA_TOPIC_SERVICE_RESPONSE: str
    KAFKA_CONSUMER_GROUP_ID: str = "field_translator"
    SERVICE_IDENTIFIER: str = "field_translator"

    NUMBER_OF_MAX_CONCURRENT_MESSAGES: int = 0
    NUMBER_OF_CONCURRENT_SERVICE_CALLS: int = 1000
    NUMBER_OF_KAFKA_PRODUCERS: int = 1000
