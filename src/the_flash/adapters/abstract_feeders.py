from abc import ABC, abstractmethod
from typing import Union

from src.the_flash.abstractions.aio_comunicators import AIOConsumer
from src.the_flash.application import Application


class ApplicationFeeder(ABC):

    def __init__(self, application: Application):
        self.__application = application

    @abstractmethod
    def extract_data(self, payload) -> Union[str, bytes, dict]:
        ...

    async def feed_app(self, raw_data) -> None:
        await self.__application.ingest_data(self.extract_data(raw_data))


class ConsumerFeeder(ApplicationFeeder, ABC):

    def __init__(self, application: Application, aio_consumer: AIOConsumer):
        super().__init__(application)
        self.__aio_consumer = aio_consumer

    async def consume(self) -> None:
        async for msg in self.__aio_consumer:
            await self.feed_app(msg)


class ServerlessFeeder(ApplicationFeeder, ABC):

    async def entrypoint(self, raw_data: Union[str, bytes]):
        await self.feed_app(raw_data)
