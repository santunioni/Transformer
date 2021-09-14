from abc import ABC, abstractmethod
from typing import Protocol


class CommandReceiver(Protocol):
    """An interface for """
    data: dict
    metadata: dict


class TransformCommand(ABC):

    def __init__(self, receiver: CommandReceiver):
        self.__receiver = receiver

    @property
    def data(self) -> dict:
        return self.__receiver.data

    @property
    def metadata(self) -> dict:
        return self.__receiver.metadata

    @data.setter
    def data(self, new_data: dict):
        self.__receiver.data = new_data

    @abstractmethod
    def execute(self):
        ...
