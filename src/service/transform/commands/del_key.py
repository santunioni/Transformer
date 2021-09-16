import re
from typing import Literal, Optional

from pydantic import root_validator

from src.service.transform.abstract import Transformer, TransformerConfig


class DeleteKeysConfig(TransformerConfig):
    command_name: Literal["delete-keys"]
    keys: Optional[list[str]]
    pattern: Optional[str]

    @root_validator
    def check_if_at_least_one_is_passed(cls, values):
        keys, pattern = values.get('keys'), values.get('pattern')
        if keys is None and pattern is None:
            raise ValueError("Keys and Pattern can't be both None.")
        return values


class DeleteKeys(Transformer):

    def __init__(self, config: DeleteKeysConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        data_copy = data.copy()
        if self.__config.keys is not None:
            for key in self.__config.keys:
                try:
                    del data_copy[key]
                except KeyError:
                    pass
        if self.__config.pattern is not None:
            pattern = re.compile(self.__config.pattern)
            for key in filter(lambda k: bool(pattern.fullmatch(k)), data.keys()):
                del data_copy[key]
        return data_copy
