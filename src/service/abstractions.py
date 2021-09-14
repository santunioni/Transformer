from abc import ABC, abstractmethod
from typing import Protocol


class TransformCommand(ABC):

    @abstractmethod
    def transform(self, data: dict, metadata: dict) -> dict:
        ...
