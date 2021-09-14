
from src.the_flash.application import Application
from src.the_flash.senders.aio_kafka_producer import AIOProducerKafkaAdapter
from src.the_flash.feeders.consumer_feeders.aiokafka.factory import kafka_settings, kafka_factory
from src.the_flash.feeders.consumer_feeders.aiokafka.kafka_feeder import KafkaFeeder

consumer, producer = kafka_factory()

aio_producer = AIOProducerKafkaAdapter(
    aio_kafka_producer=producer,
    topic=kafka_settings().KAFKA_TOPIC_SERVICE_RESPONSE
    )

app = Application(aio_producer=aio_producer)

entrypoint = KafkaFeeder(application=app, aio_consumer=consumer)

entrypoint.consume()

app.process_letters()
