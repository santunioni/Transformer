import asyncio
import logging
from asyncio import Queue, Task
from typing import Callable, Optional, Mapping, Coroutine, List, Any

from pydantic import ValidationError

from src.service.entrypoint import handler
from src.the_flash.models.mat_events import ServiceLetter, ServiceResponse
from src.the_flash.senders.aio_producer import AIOProducer

logger = logging.getLogger(__name__)


class Application:
    """
    This is the highest level class in the code, responsible for calling the methods that trigger the major
    events in the code.
    """
    __custom_entries: Mapping[str, Callable[[
                                                ServiceLetter], Coroutine[Any, Any, Optional[ServiceResponse]]]] = {}

    @staticmethod
    def __mat_entries(
            mat_id: str) -> Callable[[ServiceLetter], Coroutine[Any, Any, Optional[ServiceResponse]]]:
        if mat_id in Application.__custom_entries.keys():
            return Application.__custom_entries[mat_id]
        return handler

    def __init__(self, aio_producer: AIOProducer,
                 queue: Queue[ServiceLetter] = Queue()):
        """
        :param aio_producer: The producer that will send the treated data back to TheFlash services.
        :param queue: This queue holds the data so they can be picked asynchronously to be treated and sent.
        """
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
            self.__tasks.append(asyncio.create_task(self.__process_letters()))

    async def __process_letters(self) -> None:
        """
        This method implement the core functionality of this code, it processes the configuration JSON applying the
        necessary transformations. And them it sends it back to Kafka Queue.
        :return: None
        """
        while True:
            letter: ServiceLetter = await self.__queue.get()
            try:
                response = await Application.__mat_entries(letter.mat_id)(letter)
                if response is not None:
                    result = await self.__aio_producer.send(response)
                    if result:
                        logger.info("Sent: %s", response.event_trace)
            except Exception:
                logger.critical(
                    "Some general exception occurred",
                    exc_info=True)
            self.__queue.task_done()

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
            await self.__queue.put(letter)
        except ValidationError as err:
            logger.error(
                "Got ValidationError while parsing message. Check traceback: %s", err)
