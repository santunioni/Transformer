from typing import Tuple

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.helpers import create_ssl_context
from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    """Kafka settings needed to instantiate consumer and producers"""
    IS_LOCALHOST: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_FIELD_TRANSLATOR: str
    KAFKA_TOPIC_SERVICE_RESPONSE: str
    KAFKA_CONSUMER_GROUP_ID: str = "field_translator"

    def __hash__(self):
        return hash(str(self))


def kafka_factory(
        settings: KafkaSettings) -> Tuple[AIOKafkaConsumer, AIOKafkaProducer]:
    """
    Provides the producer and consumer to instantiate the producers and consumers.
    :return: consumer and producer in a tuple
    """
    kafka_conn_settings = dict(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        security_protocol="PLAINTEXT" if settings.IS_LOCALHOST else "SSL",
        ssl_context=None if settings.IS_LOCALHOST else create_ssl_context()
    )
    kafka_consumer = AIOKafkaConsumer(
        *settings.KAFKA_TOPIC_FIELD_TRANSLATOR.split(","),
        group_id=settings.KAFKA_CONSUMER_GROUP_ID,
        **kafka_conn_settings
    )
    kafka_producer = AIOKafkaProducer(
        **kafka_conn_settings
    )
    return kafka_consumer, kafka_producer
