from typing import Any, Dict, Optional, Pattern, Sequence, Tuple

from pydantic import root_validator

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class DeleteKeysConfig(ExtraHashableModel):
    """
    Keys are a list of keys to be deleted.
    Pattern are a RegEx pattern that will instruct the transformer to delete every key that is a fullmatch to the
    pattern.
    """

    keys: Optional[Sequence[str]]
    pattern: Optional[Pattern]

    @root_validator
    def check_if_at_least_one_is_passed(cls, values):
        keys, pattern = values.get("keys"), values.get("pattern")
        assert not (
            keys is None and pattern is None
        ), "Keys and Pattern can't be both None."
        return values


class DeleteKeys(Transformer[DeleteKeysConfig]):
    """
    This simply delete key-value pairs from the data dict. Its possible to specify the keys directly or to
    pass a Regular Expression (RegEx), every key that is a complete match to the RegEx will be deleted.
    Both can be used at the same time.
    """

    def transform(
        self, payload: Dict[str, Any], metadata: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        """
        Implements the deletion of key-value pairs.
        :param payload: Data that contains the keys that should be deleted.
        :param metadata: Metadata.
        :return: Data without keys.
        """
        data_copy = payload.copy()
        if self._config.keys is not None:
            for key in self._config.keys:
                try:
                    del data_copy[key]
                except KeyError:
                    pass
        if self._config.pattern is not None:
            pattern = self._config.pattern
            for key in filter(lambda k: bool(pattern.fullmatch(k)), payload.keys()):
                try:
                    del data_copy[key]
                except KeyError:
                    pass
        return data_copy, metadata or {}
