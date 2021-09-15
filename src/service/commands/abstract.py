import logging
from abc import ABC, abstractmethod

import ujson
from pydantic import BaseModel

from src.the_flash.utils import ujson_dumps

logger = logging.getLogger(__name__)


class TransformerConfig(BaseModel):

    def __hash__(self):
        return hash(str(self))

    class Config:
        json_dumps = ujson_dumps
        json_loads = ujson.loads


class Transformer(ABC):

    @abstractmethod
    def __init__(self, config: TransformerConfig):
        logger.info("Estou instanciando a classe: %s", self.__class__.__name__)

    @abstractmethod
    def transform(self, data: dict, metadata: dict) -> dict:
        ...
