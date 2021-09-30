import re
from typing import Literal, Optional, Pattern, Union

from ..abstract import Transformer, TransformerConfig


class ValueSanitizerConfig(TransformerConfig):
    """
    Use key-pattern to select all keys that is a fullmatch to a RegEx pattern.
    The sub-pattern is used to select parts of the values that should be substituted by the sub_string.
    The string methods are the names of builtin python string methods,
    """
    command_name: Literal["value-sanitizer"]
    key_pattern: Pattern
    substitution_pattern: Optional[Pattern]
    sub_string: str = ''
    string_methods: Optional[Union[list[str], str]]


class ValueSanitizer(Transformer):
    """
    The ValueSanitizer Transformer is able to sanitize values of keys selected. They do that by substitution and
    implementation of string methods.
    """

    def __init__(self, config: ValueSanitizerConfig):
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """
        Implements the transform by finding all keys thta match keys_pattern, then for each key implement the
        substitution then the string_methods.
        :param data: Untransformed Data
        :param metadata: Metadata
        :return: Transformed data
        """
        data_copy = data.copy()
        for key in filter(lambda k: bool(self.__config.key_pattern.fullmatch(k)), data.keys()):
            value = data[key]
            if self.__config.substitution_pattern:
                value = re.sub(self.__config.substitution_pattern, self.__config.sub_string, value)
            if self.__config.string_methods is not None:
                if isinstance(self.__config.string_methods, list):
                    for string_method_name in self.__config.string_methods:
                        value = getattr(str, string_method_name)(value)
                else:
                    value = getattr(str, self.__config.string_methods)(value)
            del data_copy[key]
            data_copy[key] = value
        return data_copy
