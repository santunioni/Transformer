from typing import TypeVar, Protocol

from src.models.mat_events import ServiceResponse

ProducerRawData = TypeVar("ProducerRawData")
EntrypointRawData = TypeVar("EntrypointRawData")


class AIOProducer(Protocol[ProducerRawData]):

    async def send(self, response: ServiceResponse) -> ProducerRawData:
        ...


class AIOConsumer(Protocol[EntrypointRawData]):

    async def __aiter__(self) -> EntrypointRawData:
        ...
