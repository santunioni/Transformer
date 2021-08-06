import json
from typing import Tuple

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.helpers import create_ssl_context

from src.settings import EnvironmentSettings


def kafka_factory(settings: EnvironmentSettings) -> Tuple[AIOKafkaConsumer, AIOKafkaProducer]:
    first_boostrap_server_is_localhost: bool = settings.KAFKA_BOOTSTRAP_SERVERS.split(":")[0].lower() == "localhost"
    kafka_conn_settings = dict(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        security_protocol="PLAINTEXT" if first_boostrap_server_is_localhost else "SSL",
        ssl_context=None if first_boostrap_server_is_localhost else create_ssl_context()
    )
    letter_consumer = AIOKafkaConsumer(
        *settings.KAFKA_TOPIC_FIELD_TRANSLATOR.split(","),
        group_id=settings.KAFKA_CONSUMER_GROUP_ID,
        **kafka_conn_settings
    )
    response_producer = AIOKafkaProducer(
        value_serializer=lambda v: json.dumps(v.dict()).encode('utf-8'),
        **kafka_conn_settings
    )
    return letter_consumer, response_producer
