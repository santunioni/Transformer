from typing import Any, Dict, List, Optional, Tuple, Union

from transformer.transformers.abstract import ExtraHashableModel, Transformer
from transformer.transformers.flatten import Flatter, Unflatter


class MapKeysConfig(ExtraHashableModel):
    """
    This is the configuration for the MapKeys transformer.
    In order to call this transformer pass the name "map-keys" and a mapping dict.
    """

    mapping: Dict[str, str]
    preserve_unmapped: bool = True
    ignore_missing_data: bool = True


class MapKeys(Transformer[MapKeysConfig]):
    """
    The MapKeys is a complete dict re-designer.
    It lets you rename the keys and also restructure the entire dict. Creating new nested data where there wasn't
    and also flattening data that was previously nested is possible, all that preserving the data from the input
    dictionary.
    """

    def __init__(self, config: MapKeysConfig) -> None:
        super().__init__(config)
        self.__flatter = Flatter()
        self.__unflatter = Unflatter()

    def transform(
        self, payload: Dict, /, metadata: Optional[Dict] = None
    ) -> Tuple[Dict, Dict]:
        """
        The mapping is done in 4 major steps:

        1. Flattens the data.
        2. Metadata Replacers:
            Some key mapping parameters are specified in the metadata. Keys that have placeholders like
            ${metadata_key} will be substituted by values on the specified metadata key.
        3. Map Data.
                In this moment the keys of the mapping inside config match the keys of the flat payload. That is, the
            payload and self._config.mapping have matching keys. Maybe not all keys in payload are in
            self._config.mapping, in which case we choose what to do with those extra keys with the config
            self._config.preserve_unmapped. If the opposite happens, the self._config.mapping have keys not present
            in the payload, the configuration self._config.ignore_missing_data chooses what should be done.
        4. Unflattens the data.
        :return: transformed and restructured data.
        """
        if metadata is None:
            metadata = {}

        flat_data, metadata = self.__flatter.transform(payload, metadata)
        translated_dict: dict = {}

        for map_key, map_value in self._config.mapping.items():

            if self._config.ignore_missing_data and map_key not in flat_data.keys():
                continue

            for meta_key, meta_value in metadata.items():
                map_key = map_key.replace("@{" + meta_key + "}", str(meta_value))
                map_value = map_value.replace("@{" + meta_key + "}", str(meta_value))

            if map_key in flat_data:
                commands = map_value.split(".")
                translated_dict = MapKeys.__map_data(
                    translated_dict, commands, flat_data[map_key]
                )

        if self._config.preserve_unmapped:
            for unmapped_key in set(flat_data.keys() - self._config.mapping.keys()):
                translated_dict[unmapped_key] = flat_data[unmapped_key]

        return self.__unflatter.transform(translated_dict, metadata)

    @staticmethod
    def __map_data(
        current_structure: Union[Dict, List], command_list: List[str], value: Any
    ):
        """
        This method is recursive. It reads the values from the mapping
        in order to build the new data structure.

        The command_list specifies the structure. It can be something like ['key_1', '$[1]', 'key_2'].
        The function works by building recursively the structure.
        In the last example it would use the passed current_structure (a filled or empty dict) to build key_1 inside
        this dict, them create a list inside it, them another dict on the second position (the first is filled with
        None) and them put key_2 inside this dict, the value is specified in the value parameter.

        At each structure it builds (a dict or list) the command_list shrinks by one. Until the last command where
        the value from the parameter is put inside the structure.

        :param current_structure: Can be a list or a dict.
        :param command_list: The list of transformers, the current and next command are important.
        :param value: The value that will be passed at the last command.
        :return: Return the built structure for this command list incorporated into the passed initial structure.
        """
        command = command_list[0]
        new_command_list = command_list[1:]

        if "$[" not in command and isinstance(current_structure, Dict):
            if len(command_list) == 1:
                current_structure[command] = value
                return current_structure
            if "$[" not in command_list[1]:
                next_structure = (
                    current_structure[command]
                    if command in current_structure.keys()
                    else {}
                )
            else:
                index = int(command_list[1].replace("$[", "").replace("]", ""))
                next_structure = MapKeys.__create_big_enough_list(
                    index, current_structure.get(command)
                )

            current_structure[command] = MapKeys.__map_data(
                next_structure, new_command_list, value
            )
        else:
            index = int(command.replace("$[", "").replace("]", ""))
            if len(command_list) == 1:
                current_structure[index] = value
                return current_structure
            if "$[" not in command_list[1]:
                next_structure = (
                    current_structure[index]
                    if current_structure[index] is not None
                    else {}
                )
            else:
                next_structure = MapKeys.__create_big_enough_list(
                    index, current_structure[index]
                )
            current_structure[index] = MapKeys.__map_data(
                next_structure, new_command_list, value
            )

        return current_structure

    @staticmethod
    def __create_big_enough_list(index: int, list_to_write: Optional[List[Any]]):
        """
        It gets a list structure in list_to_write and them puts its values in the correct indexes in a list
        of length given by index. But only if the index is greater than the length list_to_write, otherwise it simply
        returns list_to_write. The index list is populated with None in the places where its not populated by
        list_to_write.
        :param index:
        :param list_to_write:
        :return:
        """
        list_to_be_overwritten = [None for i in range(0, index + 1)]
        if list_to_write is None:
            return list_to_be_overwritten

        if len(list_to_be_overwritten) > len(list_to_write):
            for c_index, value in enumerate(list_to_write):
                list_to_be_overwritten[c_index] = value
            return list_to_be_overwritten

        return list_to_write
