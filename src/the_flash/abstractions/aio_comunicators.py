from __future__ import annotations

from typing import Protocol

from src.models.mat_events import ServiceResponse


class AIOProducer(Protocol):

    async def send(self, response: ServiceResponse):
        ...


class AIOConsumer(Protocol):

    async def __aiter__(self):
        ...

    async def __anext__(self):
        ...
