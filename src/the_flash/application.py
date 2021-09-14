import logging
from asyncio import Queue

from pydantic import ValidationError

from src.models.mat_events import ServiceLetter
from src.the_flash.senders.aio_producer import AIOProducer
from src.transformer.entrypoint import service_entrypoint

logger = logging.getLogger(__name__)


class Application:
    """
    This is the highest level class in the code, responsible for calling the methods that trigger the major
    events in the code.
    """

    def __init__(self, aio_producer: AIOProducer, queue: Queue[ServiceLetter] = Queue()):
        """
        :param aio_producer: The producer that will send the treated data back to TheFlash services.
        :param queue: This queue holds the data so they can be picked asynchronously to be treated and sent.
        """
        self.aio_producer = aio_producer
        self.queue = queue

    async def process_letters(self) -> None:
        """
        This method implement the core functionality of this code, it processes the configuration JSON applying the
        necessary transformations. And them it sends it back to Kafka Queue.
        :return: None
        """
        while True:
            letter: ServiceLetter = await self.queue.get()
            try:
                response = await service_entrypoint(letter)
                if response is not None:
                    await self.aio_producer.send(response)
            except Exception:
                logger.critical("Some general exception occurred", exc_info=True)
            self.queue.task_done()

    async def ingest_data(self, raw_data) -> None:
        """
        This method is responsible for putting data inside the queue. But before it does that it turns the JSON into
        a dictionary, a format that the processing step above is able handle.
        :param raw_data: JSON with configuration fields.
        :return: None
        """
        try:
            letter = ServiceLetter.parse_raw(raw_data)
            logger.info("Received: %s", letter.event_trace)
            await self.queue.put(letter)
        except ValidationError as err:
            logger.error("Got ValidationError while parsing message. Check traceback: %s", err)
