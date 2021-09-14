from abc import ABC, abstractmethod


class TransformCommand(ABC):

    def __init__(self, data: dict, metadata: dict):
        self.__data = data
        self.__metadata = metadata

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def metadata(self) -> dict:
        return self.__metadata

    @data.setter
    def data(self, new_data: dict):
        self.__data = new_data

    @abstractmethod
    def execute(self) -> dict:
        ...
