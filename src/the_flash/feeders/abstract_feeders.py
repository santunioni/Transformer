from abc import ABC, abstractmethod
from typing import Generic, Any, Union


from src.the_flash.application import Application
from src.the_flash.feeders.consumer_feeders.aio_consumer import EntrypointRawData, AIOConsumer


class FeederImplementation(ABC, Generic[EntrypointRawData]):
    """
    The Feeder is responsible for getting data from TheFlash service and feeding it to the queue.
    The feeding method can be injected into the feeder. This class connected to the Application makes a bridge
    to whichever feeding method you choose.
    """
    def __init__(self, application: Application):
        """
        :param application: The application object that bridge is constructed to.
        """
        self.application = application

    @abstractmethod
    def extract_data(self, payload: EntrypointRawData) -> Any:
        """
        This method is responsible for extracting from the data that comes from TheFlash service only the
        part that should be transformed by this service.
        :param payload: The TheFlash incoming data.
        :return: Data that should be transformed by this service.
        """
        ...


class ConsumerImplementation(FeederImplementation[EntrypointRawData], ABC):
    """
    A Consumer implementation is any Feeder implementation that is of the publish-subscriber type.
    They need a proper AIOConsumer in order to work.
    """

    def __init__(self, application: Application, aio_consumer: AIOConsumer[EntrypointRawData]):
        super().__init__(application)
        self.aio_consumer = aio_consumer

    async def consume(self):
        async for msg in self.aio_consumer:
            await self.application.ingest_data(self.extract_data(msg))


class ServerlessImplementation(FeederImplementation[EntrypointRawData], ABC):

    def __init__(self, application: Application):
        super().__init__(application)

    async def entrypoint(self, raw_data: Union[str, bytes]):
        await self.application.ingest_data(self.extract_data(raw_data))
