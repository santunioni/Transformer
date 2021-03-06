import re
from typing import Any, Dict, Optional, Pattern, Sequence, Union

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class ValueSanitizerConfig(ExtraHashableModel):
    """
    Use key-pattern to select all keys that is a fullmatch to a RegEx pattern.
    The sub-pattern is used to select parts of the values that should be substituted by the sub_string.
    The string methods are the names of builtin python string methods,
    """

    key_pattern: Pattern
    substitution_pattern: Optional[Pattern]
    sub_string: str = ""
    string_methods: Optional[Union[Sequence[str], str]]


class ValueSanitizer(Transformer[ValueSanitizerConfig]):
    """
    The ValueSanitizer Transformer is able to sanitize values of keys selected. They do that by substitution and
    implementation of string methods.
    """

    def transform(
        self, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Implements the transformer by finding all keys thta match keys_pattern, then for each key implement the
        substitution then the string_methods.
        :param payload: Untransformed Data
        :param metadata: Metadata
        :return: Transformed data
        """
        data_copy = payload.copy()
        for key in filter(
            lambda k: bool(self._config.key_pattern.fullmatch(k)), payload.keys()
        ):
            value = payload[key]
            if self._config.substitution_pattern:
                value = re.sub(
                    self._config.substitution_pattern, self._config.sub_string, value
                )
            if self._config.string_methods is not None:
                if isinstance(self._config.string_methods, list):
                    for string_method_name in self._config.string_methods:
                        value = getattr(str, string_method_name)(value)
                else:
                    value = getattr(str, self._config.string_methods)(value)
            del data_copy[key]
            data_copy[key] = value

        if metadata is None:
            return data_copy

        return data_copy, metadata
