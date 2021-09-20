import logging
from abc import ABC, abstractmethod

import ujson
from pydantic import BaseModel
from the_flash.utils.parsing import ujson_dumps

logger = logging.getLogger(__name__)


class BaseTransformerConfig(BaseModel):

    def __hash__(self) -> int:
        return hash(str(self))

    class Config:
        json_dumps = ujson_dumps
        json_loads = ujson.loads


class TransformerConfig(BaseTransformerConfig):
    command_name: str


class Transformer(ABC):

    @abstractmethod
    def __init__(self, config: BaseTransformerConfig):
        logger.info(
            "Initializing object of class %s with config parameter of class %s ...",
            self.__class__.__name__, config.__class__.__name__
        )

    @abstractmethod
    def transform(self, data: dict, metadata: dict) -> dict:
        ...
