import logging
import re
from typing import Literal, Optional

from pydantic import root_validator

from src.service.transform.abstract import Transformer, TransformerConfig

logger = logging.getLogger(__name__)


class AggregateKeyValueConfig(TransformerConfig):
    command_name: Literal["aggregate-keys"]
    keys: Optional[list[str]]
    pattern: Optional[str]
    new_key: str

    @root_validator
    def check_if_at_least_one_is_passed(cls, values):
        keys, pattern = values.get('keys'), values.get('pattern')
        if keys is None and pattern is None:
            raise ValueError("Keys and Pattern can't be both None.")
        return values


class AggregateKeyValue(Transformer):

    def __init__(self, config: AggregateKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        data_copy = data.copy()
        value_list = []
        if self.__config.keys is not None:
            keys_filter = filter(lambda k: k in data.keys(), self.__config.keys)
        else:
            pattern = re.compile(self.__config.pattern)
            keys_filter = filter(lambda k: bool(pattern.fullmatch(k)), data.keys())

        for key in keys_filter:
            value_list.append(data[key])
            del data_copy[key]

        data_copy[self.__config.new_key] = value_list
        return data_copy
