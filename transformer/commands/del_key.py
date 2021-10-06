from typing import Literal, Optional, Pattern

from pydantic import root_validator

from ..abstract import Transformer, TransformerConfig


class DeleteKeysConfig(TransformerConfig):
    """
    Keys are a list of keys to be deleted.
    Pattern are a RegEx pattern that will instruct the transformer to delete every key that is a fullmatch to the
    pattern.
    """

    name: Literal["delete-keys"]
    keys: Optional[list[str]]
    pattern: Optional[Pattern]

    @root_validator
    def check_if_at_least_one_is_passed(cls, values):
        keys, pattern = values.get("keys"), values.get("pattern")
        assert not (
            keys is None and pattern is None
        ), "Keys and Pattern can't be both None."
        return values


class DeleteKeys(Transformer):
    """
    This simply delete key-value pairs from the data dict. Its possible to specify the keys directly or to
    pass a Regular Expression (RegEx), every key that is a complete match to the RegEx will be deleted.
    Both can be used at the same time.
    """

    def __init__(self, config: DeleteKeysConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """
        Implements the deletion of key-value pairs.
        :param data: Data that contains the keys that should be deleted.
        :param metadata: Metadata.
        :return: Data without keys.
        """
        data_copy = data.copy()
        if self.__config.keys is not None:
            for key in self.__config.keys:
                try:
                    del data_copy[key]
                except KeyError:
                    pass
        if self.__config.pattern is not None:
            pattern = self.__config.pattern
            for key in filter(lambda k: bool(pattern.fullmatch(k)), data.keys()):
                try:
                    del data_copy[key]
                except KeyError:
                    pass
        return data_copy
