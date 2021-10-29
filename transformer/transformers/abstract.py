import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Tuple, TypeVar, Union, overload

import ujson
from pydantic import BaseModel, Extra

logger = logging.getLogger(__name__)


def ujson_dumps(data, default, **dumps_kwargs):  # pylint: disable=W0613
    return ujson.dumps(data, ensure_ascii=False)


class ExtraHashableModel(BaseModel):
    class Config:
        json_dumps = ujson_dumps
        json_loads = ujson.loads
        extra = Extra.allow
        frozen = True


TransformerConfig = TypeVar("TransformerConfig")


class Transformer(Generic[TransformerConfig], ABC):
    """
    A abstract transformer has declares and interface for the general transformer method.
    """

    def __init__(self, config: TransformerConfig):
        logger.debug(
            "Initializing object of class %s with config parameter of class %s ...",
            self.__class__.__name__,
            config.__class__.__name__,
        )
        self._config = config

    @overload
    def transform(self, payload: Dict[str, Any]) -> Dict:
        ...

    @overload
    def transform(
        self, payload: Dict[str, Any], metadata: Dict[str, Any]
    ) -> Tuple[Dict, Dict]:
        ...

    @abstractmethod
    def transform(
        self, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> Union[Dict, Tuple[Dict, Dict]]:
        """
        A General transformer method, each concrete transformer will implement this method. This method is the one
        that actually implements the transformation on the relevant data.
        :param payload: The data tha comes in the ServiceLetter.
        :param metadata: Metadata can possibly be used to insert a few alterations in the transformer.
        :return: returns the data that will be insert on a ServiceResponse object.
        """
        ...

    @overload
    def __call__(self, payload: Dict[str, Any]) -> Dict:
        ...

    @overload
    def __call__(
        self, payload: Dict[str, Any], metadata: Dict[str, Any]
    ) -> Tuple[Dict, Dict]:
        ...

    def __call__(
        self, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> Union[Dict, Tuple[Dict, Dict]]:
        return self.transform(payload, metadata or {})
