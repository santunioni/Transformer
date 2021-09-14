from typing import Protocol

from src.models.mat_events import ServiceResponse


class AIOProducer(Protocol):
    """
    This is an interface for any AIOProducer that you send the transformed data asynchronously to TheFlash services.
    """

    async def send(self, response: ServiceResponse):
        """
        This method is the only responsible for sending the treated data to TheFlash services.
        :param response: the transformed data that will be sent.
        :return: Generally metadata about the sending process.
        """
        ...
