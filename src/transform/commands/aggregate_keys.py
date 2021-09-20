import logging
import re
from typing import Literal, Optional

from src.transform.abstract import Transformer, TransformerConfig

logger = logging.getLogger(__name__)


class AggregateKeyValueConfig(TransformerConfig):
    name: Literal["aggregate-keys"]
    keys: list[str]
    pattern: Optional[str]
    new_key: str


class AggregateKeyValue(Transformer):

    def __init__(self, config: AggregateKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        value_list = []
        if self.__config.keys is not None:
            keys_filter = filter(lambda k: k in data.keys(), self.__config.keys)
        else:
            pattern = re.compile(self.__config.pattern)
            keys_filter = filter(lambda k: bool(pattern.fullmatch(k)), data.keys())

        for key in keys_filter:
            value_list.append(data[key])
            del data[key]

        data[self.__config.new_key] = value_list
        return data
