from typing import TypeVar, Protocol


EntrypointRawData = TypeVar("EntrypointRawData")


class AIOConsumer(Protocol[EntrypointRawData]):

    async def __aiter__(self) -> EntrypointRawData:
        ...
