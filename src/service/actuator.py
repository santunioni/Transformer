from src.service.abstractions import TransformCommand
from src.service.commands.map_keys import MapKeysConfig, MapKeys
from src.the_flash.models.mat_events import ServiceLetter


CONFIG_TO_COMMAND_DICT = {
    MapKeysConfig.__class__.__name__: MapKeys
}


class CommandActuator:
    """

    """
    def __init__(self):
        """

        """
        self.__commands: list[TransformCommand] = []

    def execute_all(self) -> dict:
        """

        :return:
        """
        # TODO: Falta Implementar!!
        ...

    def configure(self, service_letter: ServiceLetter):
        """

        :param service_letter:
        :return:
        """
        for transform_config in service_letter.config.commands:
            self.__commands.append(
                CONFIG_TO_COMMAND_DICT[transform_config.__class__.__name__](
                    data=service_letter.data,
                    metadata=service_letter.metadata,
                    config=transform_config
                )
            )
