from abc import ABC, abstractmethod
from typing import Any, Union

from src.the_flash.abstractions.aio_comunicators import AIOConsumer
from src.the_flash.application import Application


class ApplicationBridge(ABC):

    def __init__(self, application: Application):
        self.__application = application

    @abstractmethod
    def extract_data(self, payload) -> Any:
        ...

    async def feed_application(self, raw_data) -> None:
        await self.__application.ingest_data(self.extract_data(raw_data))


class ConsumerBridge(ApplicationBridge, ABC):

    def __init__(self, application: Application, aio_consumer: AIOConsumer):
        super().__init__(application)
        self.__aio_consumer = aio_consumer

    async def consume(self) -> None:
        async for msg in self.__aio_consumer:
            await self.feed_application(msg)


class ServerlessBridge(ApplicationBridge, ABC):

    def __init__(self, application: Application):
        super().__init__(application)

    async def entrypoint(self, raw_data: Union[str, bytes]):
        await self.feed_application(raw_data)
