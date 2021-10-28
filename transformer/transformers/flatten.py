from typing import Any, Dict, List, Optional, Set, Tuple, Union

from transformer.transformers.abstract import ExtraHashableModel, Transformer


class FlatterConfig(ExtraHashableModel):
    level_separator: str = "."
    array_specification: str = "$[<index>]"


class Flatter(Transformer[FlatterConfig]):
    def __init__(self, config: FlatterConfig = FlatterConfig()) -> None:
        super().__init__(config)

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
        new_obj: Dict[str, Union[str, int, bool, float, None]] = {}

        def inspect_and_transform(
            input_value: Union[List, Set, Dict[str, Any], str, int, bool, float, None],
            parent_key: str = "",
        ):
            if isinstance(input_value, (list, set)):
                for index, value in enumerate(input_value):
                    inspect_and_transform(
                        value,
                        f"{'' if not parent_key else parent_key + self._config.level_separator}"
                        f"{self._config.array_specification.replace('<index>', str(index))}",
                    )
            elif isinstance(input_value, dict):
                for key, value in input_value.items():
                    inspect_and_transform(
                        value,
                        f"{'' if not parent_key else parent_key + self._config.level_separator}"
                        f"{key}",
                    )
            else:
                new_obj[parent_key] = input_value

        inspect_and_transform(payload)
        return new_obj, metadata or {}


class Unflatter(Transformer[FlatterConfig]):
    def __init__(self, config: FlatterConfig = FlatterConfig()) -> None:
        super().__init__(config)

    def transform(
        self, payload: Dict, /, metadata: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        return payload, metadata or {}
