from abc import ABC, abstractmethod
from typing import Generic, Any, Union

from src.the_flash.abstractions.aio_comunicators import EntrypointRawData, AIOConsumer
from src.the_flash.application import Application


class ApplicationBridge(ABC, Generic[EntrypointRawData]):

    def __init__(self, application: Application):
        self.application = application

    @abstractmethod
    def extract_data(self, payload: EntrypointRawData) -> Any:
        ...


class ConsumerBridge(ApplicationBridge[EntrypointRawData], ABC):

    def __init__(self, application: Application, aio_consumer: AIOConsumer[EntrypointRawData]):
        super().__init__(application)
        self.aio_consumer = aio_consumer

    async def consume(self):
        async for msg in self.aio_consumer:
            await self.application.ingest_data(self.extract_data(msg))


class ServerlessBridge(ApplicationBridge[EntrypointRawData], ABC):

    def __init__(self, application: Application):
        super().__init__(application)

    async def entrypoint(self, raw_data: Union[str, bytes]):
        await self.application.ingest_data(self.extract_data(raw_data))
