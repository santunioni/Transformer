import random
import string
from abc import ABC
from typing import Any, Dict, List, Optional, Tuple

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class FlatterConfig(ExtraHashableModel):
    level_separator: str = "."


class _Flatter(Transformer[FlatterConfig], ABC):
    def __init__(self, config: FlatterConfig = FlatterConfig()) -> None:
        super().__init__(config)


class Flatter(_Flatter):
    def transform(
        self, payload: Dict, /, metadata: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        """
        This method is recursive. It flattens the keys inside data.
        A key_1 of dictionary inside a another dict inside a list inside another dict
        will be turn into
        key_3.$[list_index].key_2.key_1
        :param payload:The data tha will be flattened
        :param metadata:
        :return: flattened data.
        """
        new_obj: Dict[str, Any] = {}

        def inspect_and_transform(
            input_value: Any,
            parent_key: str = "",
        ):
            if isinstance(input_value, (list, set)):
                if input_value:
                    for index, value in enumerate(input_value):
                        inspect_and_transform(
                            value,
                            f"{parent_key}[{index}]",
                        )
                else:
                    new_obj[parent_key] = input_value
            elif isinstance(input_value, dict):
                for key, value in input_value.items():
                    inspect_and_transform(
                        value,
                        f"{parent_key}"
                        f"{self._config.level_separator if parent_key else ''}"
                        f"{key}",
                    )
            else:
                new_obj[parent_key] = input_value

        inspect_and_transform(payload)
        return new_obj, metadata or {}


class Unflatter(_Flatter):
    def __init__(self, config: FlatterConfig = FlatterConfig()) -> None:
        super().__init__(config)
        self.__flatter = Flatter()
        # some random char that will never exist in business keys:
        self.__replace_char = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(20)
        )

    def transform(
        self, payload: Dict[str, Any], /, metadata: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        """
        This method transform payloads with flat syntax into a nested object. The unflattering algorithm
        assumes the input is entirely flat, which is why I am calling the Flatter().transform() method on the payload
        before creating the new payload from it.

        Doctest example:
        >>> actual = Unflatter().transform({
        ...     "item[0].subitem[0].key": "value1",
        ...     "item[0].subitem[1].key": "value2",
        ...     "item[1].subitem[0].key": "value3",
        ...     "item[1].subitem[1].key": "value4",
        ...     "item2[0].subitem[0]": "value5",
        ...     "item2[0].subitem[1]": "value6",
        ...     "item2[1][0].key1": "value7",
        ...     "item2[1][1].key2": "value8"
        ... })[0]
        >>> expected = {
        ...     'item': [
        ...         {'subitem': [{'key': 'value1'}, {'key': 'value2'}]},
        ...         {'subitem': [{'key': 'value3'}, {'key': 'value4'}]},
        ...     ],
        ...     "item2": [
        ...         {'subitem': ['value5', 'value6']},
        ...         [{'key1': 'value7'}, {'key2': 'value8'}],
        ...     ],
        ... }
        >>> assert actual == expected
        """
        payload, metadata = self.__flatter.transform(payload, metadata)
        new_obj: Dict = {}
        for key, value in payload.items():  # type: str, Any
            nested = new_obj

            structures = self._get_key_structures(key)

            for count, (index, next_structure) in enumerate(
                zip(structures, structures[1:] + [value]), 1
            ):
                value = (
                    next_structure
                    if count == len(structures)
                    else []
                    if next_structure.isdigit()
                    else {}
                )
                if isinstance(nested, list):
                    index = int(index)
                    while index >= len(nested):
                        nested.append(value)
                elif index not in nested:
                    nested[index] = value
                nested = nested[index]

        return new_obj, metadata

    def _get_key_structures(self, key) -> List[str]:
        """
        Return a list of structures to be iterated over, in order to reconstruct the original dict.

        Doctest examples:

        >>> expected = ['item', '0', 'subitem', '0', 'key']

        >>> actual = Unflatter()._get_key_structures("item[0].subitem[0].key")
        >>> assert actual == expected

        >>> actual = Unflatter(FlatterConfig(level_separator="|"))._get_key_structures("item[0]|subitem[0]|key")
        >>> assert actual == expected
        """
        return list(
            filter(
                bool,
                key.strip(self._config.level_separator)
                .replace("[", self.__replace_char)
                .replace("]", self.__replace_char)
                .replace(self._config.level_separator, self.__replace_char)
                .split(self.__replace_char),
            )
        )


if __name__ == "__main__":
    import doctest

    import flatters  # noqa

    print(doctest.testmod(flatters))
