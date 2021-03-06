import re
from typing import Any, Dict, Mapping, Optional

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class AddKeyValuesConfig(ExtraHashableModel):
    """The key_values dict is a dict of key-value pairs to be added to the data"""

    key_values: Mapping


class AddKeyValues(Transformer[AddKeyValuesConfig]):
    """
    This Transform is able to add key-value pairs to the data. The pairs are passed inside a dict and they will be
    incorporated into the data.
    The non triviality of this transformer comes from the possibility of passing pairs that uses values of other pairs
    in the existing data or metadata.
    For Example:
    data = {'data_key_1': 'data_value_1'}
    metadata = {'meta_1': 'meta_value_1'}
    key_values = {
                    'key_2': 'value_2',
                    'new_key_${data_key_1}': ${data_key_1}_@{meta_1}
                    }

    The Transform output will be:

    data = {
            'data_key_1': 'data_value_1',
            'key_2': 'value_2',
            'new_key_data_value_1: data_value_1_meta_value_1
        }

    Only keys that map to strings can be passed. The strings are passed with .lower() method.
    """

    def transform(
        self, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add the key values to the data.
        First the keys in key_values are replaced then its values (if they are strings).
        They are stored in another dict which is merged with data dict.
        :param payload: the data that shall be transformed.
        :param metadata: metadata.
        :return: the transformed data
        """
        replaced_key_value_dict = {}
        for key, value in self._config.key_values.items():
            if any(map(key.__contains__, ("${", "@{"))):
                key = AddKeyValues._replace_key_placeholders_with_values(
                    key, payload, metadata
                )
            if isinstance(value, str) and any(map(value.__contains__, ("${", "@{"))):
                value = AddKeyValues._replace_key_placeholders_with_values(
                    value, payload, metadata
                )
            replaced_key_value_dict[key] = value

        payload.update(replaced_key_value_dict)
        if metadata is None:
            return payload

        return payload, metadata

    @staticmethod
    def _replace_key_placeholders_with_values(
        string: str, data: Dict[str, Any], metadata: Optional[Dict[str, Any]]
    ) -> str:
        """
        Implements the actual substitution of placeholders to values.
        Placeholders inside ${} seek their values in the current data.
        While placeholders inside @{} seek their values in the current metadata.
        :param string: string with placeholders
        :param data: data that will be transformed.
        :param metadata: metadata.
        :return: replaced string.
        """
        keys = re.findall("\\${(.+?)}", string)
        metadata_keys = re.findall("@{(.+?)}", string)
        for key in keys:
            string = string.replace("${" + key + "}", str(data[key]).lower())
        if metadata is not None:
            for key in metadata_keys:
                string = string.replace("@{" + key + "}", str(metadata[key]).lower())
        return string
