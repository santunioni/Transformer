import logging
from abc import ABC, abstractmethod

from the_flash import BaseHashableModel

logger = logging.getLogger(__name__)


class TransformerConfig(BaseHashableModel):
    """
    A General transformer config has a UNIQUE name, declared in each transformer config.
    Each Transformer config has also its own parameters.
    New Transformer's added to this service require the creation of a standard name for it.
    """
    command_name: str


class Transformer(ABC):
    """
    A abstract transformer has declares and interface for the general transform method.
    """
    @abstractmethod
    def __init__(self, config: BaseHashableModel):
        logger.info(
            "Initializing object of class %s with config parameter of class %s ...",
            self.__class__.__name__,
            config.__class__.__name__)

    @abstractmethod
    def transform(self, data: dict, metadata: dict) -> dict:
        """
        A General transform method, each concrete transformer will implement this method. This method is the one
        that actually implements the transformation on the relevant data.
        :param data: The data tha comes in the ServiceLetter.
        :param metadata: Metadata can possibly be used to insert a few alterations in the transform.
        :return: returns the data that will be insert on a ServiceResponse object.
        """
        ...
