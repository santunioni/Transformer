import asyncio
import logging
from asyncio import Queue, Task
from typing import Callable, Optional, Mapping, Coroutine, List, Any

from pydantic import ValidationError

from src.models.mat_events import ServiceLetter, ServiceResponse
from src.the_flash.abstractions.aio_comunicators import AIOProducer
from src.transformer.entrypoint import letter_entrypoint

logger = logging.getLogger(__name__)


class Application:
    __custom_entries: Mapping[
        str, Callable[[ServiceLetter], Coroutine[Any, Any, Optional[ServiceResponse]]]
    ] = {

    }

    @staticmethod
    def __mat_entries(mat_id: str) -> Callable[[ServiceLetter], Coroutine[Any, Any, Optional[ServiceResponse]]]:
        if mat_id in Application.__custom_entries.keys():
            return Application.__custom_entries[mat_id]
        return letter_entrypoint

    def __init__(self, aio_producer: AIOProducer, queue: Queue[ServiceLetter] = Queue()):
        self.__aio_producer = aio_producer
        self.__queue = queue
        self.__tasks: List[Task] = []

    @property
    def tasks(self):
        return self.__tasks

    @property
    def queue(self):
        return self.__queue

    def increase_tasks(self, amount: int = 1):
        for _ in range(amount):
            self.__tasks.append(asyncio.create_task(self.__consume_letters()))

    async def __consume_letters(self) -> None:
        while True:
            letter: ServiceLetter = await self.__queue.get()
            try:
                response = await Application.__mat_entries(letter.mat_id)(letter)
                if response is not None:
                    result = await self.__aio_producer.send(response)
                    if result:
                        logger.info("Sent: %s", response.event_trace)
            except Exception:
                logger.critical("Some general exception occurred", exc_info=True)
            self.__queue.task_done()

    async def ingest_data(self, raw_data) -> None:
        try:
            letter = ServiceLetter.parse_raw(raw_data)
            logger.info("Received: %s", letter.event_trace)
            await self.__queue.put(letter)
        except ValidationError as err:
            logger.error("Got ValidationError while parsing message. Check traceback: %s", err)
