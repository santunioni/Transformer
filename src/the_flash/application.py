import logging
from asyncio import Queue

from pydantic import ValidationError

from src.models.mat_events import ServiceLetter
from src.the_flash.abstractions.aio_comunicators import AIOProducer
from src.transformer.entrypoint import service_entrypoint

logger = logging.getLogger(__name__)


class Application:

    def __init__(self, aio_producer: AIOProducer, queue: Queue[ServiceLetter] = Queue()):
        self.aio_producer = aio_producer
        self.queue = queue

    async def consume_letters(self):
        while True:
            letter: ServiceLetter = await self.queue.get()
            try:
                response = await service_entrypoint(letter)
                if response is not None:
                    await self.aio_producer.send(response)
            except Exception:
                logger.critical("Some general exception occurred", exc_info=True)
            self.queue.task_done()

    async def ingest_data(self, raw_data):
        try:
            letter = ServiceLetter.parse_raw(raw_data)
            logger.info("Received: %s", letter.event_trace)
            await self.queue.put(letter)
        except ValidationError as err:
            logger.error("Got ValidationError while parsing message. Check traceback: %s", err)
