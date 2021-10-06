import logging
from abc import ABC, abstractmethod

import ujson
from pydantic import BaseModel, Extra

logger = logging.getLogger(__name__)


def ujson_dumps(data, default, **dumps_kwargs):  # pylint: disable=W0613
    return ujson.dumps(data, ensure_ascii=False)


class BaseHashableModel(BaseModel):
    def __hash__(self):
        return hash(str(self))

    class Config:
        json_dumps = ujson_dumps
        json_loads = ujson.loads
        extra = Extra.allow


class TransformerConfig(BaseHashableModel):
    """
    A General transformer config has a UNIQUE name, declared in each transformer config.
    Each Transformer config has also its own parameters.
    New Transformer's added to this service require the creation of a standard name for it.
    """

    name: str


class Transformer(ABC):
    """
    A abstract transformer has declares and interface for the general transformer method.
    """

    @abstractmethod
    def __init__(self, config: BaseHashableModel):
        logger.info(
            "Initializing object of class %s with config parameter of class %s ...",
            self.__class__.__name__,
            config.__class__.__name__,
        )

    @abstractmethod
    def transform(self, data: dict, metadata: dict) -> dict:
        """
        A General transformer method, each concrete transformer will implement this method. This method is the one
        that actually implements the transformation on the relevant data.
        :param data: The data tha comes in the ServiceLetter.
        :param metadata: Metadata can possibly be used to insert a few alterations in the transformer.
        :return: returns the data that will be insert on a ServiceResponse object.
        """
        ...