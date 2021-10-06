import logging
from typing import Literal, Optional, Pattern

from pydantic import root_validator

from ..abstract import Transformer, TransformerConfig

logger = logging.getLogger(__name__)


class AggregateKeyValueConfig(TransformerConfig):
    """
    The Keys are optional, and can be used to aggregate all values of these keys.
    The pattern aggregates all values with the pattern into the new key.
    Both can be used at the same time but they cant be both None.
    """

    name: Literal["aggregate-keys"]
    keys: Optional[list[str]]
    pattern: Optional[Pattern]
    new_key: str

    @root_validator
    def check_if_at_least_one_is_passed(cls, values):
        keys, pattern = values.get("keys"), values.get("pattern")
        assert not (
            keys is None and pattern is None
        ), "Keys and Pattern can't be both None."
        return values


class AggregateKeyValue(Transformer):
    """
    This transformer is responsible for aggregating data. Pass a list of keys or a RegEx pattern and the keys
    will be stored inside a list in a new_key.
    Both pattern and Keys list can be used at the same time.
    """

    def __init__(self, config: AggregateKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """
        new_key: emails
        pattern: ^(email_).
        or
        keys: ['email_1', 'email_2', 'email_3']

        turns this:
        {
            "email_1": "a@g.com,
            "email_2": "b@g.com",
            "email_3": "c@g.com"
        }

        into this:

        {
            emails: ["a@g.com", "b@g.com", "c@g.com"]
        }

        :return:
        """
        data_copy = data.copy()
        value_list = []
        keys_set = set()
        pattern_keys_set = set()
        if self.__config.keys is not None:
            keys_set = set(filter(lambda k: k in data.keys(), self.__config.keys))
        if self.__config.pattern is not None:
            pattern = self.__config.pattern
            pattern_keys_set = set(
                filter(lambda k: bool(pattern.fullmatch(k)), data.keys())
            )

        for key in set.union(keys_set, pattern_keys_set):
            value_list.append(data[key])
            del data_copy[key]

        data_copy[self.__config.new_key] = value_list
        return data_copy
