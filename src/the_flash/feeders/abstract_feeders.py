from abc import ABC, abstractmethod
from typing import Any, Union

from src.the_flash.application import Application
from src.the_flash.feeders.consumer_feeders.aio_consumer import AIOConsumer


class FeederImplementation(ABC):
    """
    The Feeder is responsible for getting data from TheFlash service and feeding it to the queue.
    The feeding method can be injected into the feeder. This class connected to the Application makes a bridge
    to whichever feeding method you choose.
    """

    def __init__(self, application: Application):
        """
        :param application: The application object that bridge is constructed to.
        """
        self.__application = application

    @abstractmethod
    def extract_data(self, payload) -> Any:
        """
        This method is responsible for extracting from the data that comes from TheFlash service only the
        part that should be transformed by this service.
        :param payload: The TheFlash incoming data.
        :return: Data that should be transformed by this service.
        """
        ...

    async def feed_app(self, raw_data) -> None:
        """
        This function feeds the app using whichever implementation.
        :param raw_data: Untransformed data that shall be transformed.
        :return: None
        """
        await self.__application.ingest_data(self.extract_data(raw_data))


class ConsumerImplementation(FeederImplementation, ABC):
    """
    A Consumer implementation is any Feeder implementation that is of the publish-subscriber type.
    They need a proper AIOConsumer in order to work.
    """

    def __init__(self, application: Application, aio_consumer: AIOConsumer):
        """
        :param application: This service App, where the bridge will connect to.
        :param aio_consumer: Asynchronous consumer.
        """
        super().__init__(application)
        self.__aio_consumer = aio_consumer

    async def consume(self) -> None:
        """
        This function starts the consuming process that will insert data into the queue, it gets the that from the
        AIOConsumer
        :return: None
        """
        async for msg in self.__aio_consumer:
            await self.feed_app(msg)


class ServerlessImplementation(FeederImplementation, ABC):
    """
    Serverless implementation are for lambda serverless functions.
    """

    async def entrypoint(self, raw_data: Union[str, bytes]):
        """
        Starts the process of feeding the app using serverless functions.
        :param raw_data:
        :return:
        """
        await self.feed_app(raw_data)
