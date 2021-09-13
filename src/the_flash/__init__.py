from src.the_flash.adapters.aiokafka.aiokafkaproducer import AIOProducerKafkaAdapter
from src.the_flash.adapters.aiokafka.factory import kafka_factory, kafka_settings
from src.the_flash.adapters.aiokafka.kafka_consumer_bridge import KafkaConsumerBridge
from src.the_flash.application import Application

consumer, producer = kafka_factory()
app = Application(
    aio_producer=AIOProducerKafkaAdapter(
        aio_kafka_producer=producer,
        topic=kafka_settings().KAFKA_TOPIC_SERVICE_RESPONSE
    )
)

entrypoint = KafkaConsumerBridge(
    application=app,
    aio_consumer=consumer
)
entrypoint.consume()
