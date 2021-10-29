import logging
from typing import Any, Dict, Optional, Pattern, Sequence

from pydantic import root_validator

from transformer.transformers.abstract import ExtraHashableModel, Transformer

logger = logging.getLogger(__name__)


class AggregateKeyValueConfig(ExtraHashableModel):
    """
    The Keys are optional, and can be used to aggregate all values of these keys.
    The pattern aggregates all values with the pattern into the new key.
    Both can be used at the same time but they cant be both None.
    """

    keys: Optional[Sequence[str]]
    pattern: Optional[Pattern]
    new_key: str

    @root_validator
    def check_if_at_least_one_is_passed(cls, values):
        keys, pattern = values.get("keys"), values.get("pattern")
        assert not (
            keys is None and pattern is None
        ), "Keys and Pattern can't be both None."
        return values


class AggregateKeyValue(Transformer[AggregateKeyValueConfig]):
    """
    This transformer is responsible for aggregating data. Pass a list of keys or a RegEx pattern and the keys
    will be stored inside a list in a new_key.
    Both pattern and Keys list can be used at the same time.
    """

    def transform(
        self, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ):
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
        data_copy = payload.copy()
        value_list = []
        keys_set = set()
        pattern_keys_set = set()
        if self._config.keys is not None:
            keys_set = set(filter(lambda k: k in payload.keys(), self._config.keys))
        if self._config.pattern is not None:
            pattern = self._config.pattern
            pattern_keys_set = set(
                filter(lambda k: bool(pattern.fullmatch(k)), payload.keys())
            )

        for key in set.union(keys_set, pattern_keys_set):
            value_list.append(payload[key])
            del data_copy[key]

        data_copy[self._config.new_key] = value_list

        if metadata is None:
            return data_copy

        return data_copy, metadata
