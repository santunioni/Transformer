from typing import Protocol


class AIOConsumer(Protocol):
    """
    Every ConsumerFeeder needs a AIOConsumer that should implement these dunder methods.
    """

    async def __aiter__(self):
        ...

    async def __anext__(self):
        ...
