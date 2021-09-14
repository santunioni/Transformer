from src.service.abstractions import TransformCommand
from src.service.commands.map_keys import MapKeysConfig, MapKeys
from src.the_flash.models.mat_events import ServiceLetter


CONFIG_TO_COMMAND_DICT = {
    MapKeysConfig.__class__.__name__: MapKeys
}


class CommandActuator:

    def __init__(self):
        self.__commands: list[TransformCommand] = []

    def execute_all(self):
        ...

    def configure(self, service_letter: ServiceLetter):
        for config in service_letter.config.commands:
            self.__commands.append(
                CONFIG_TO_COMMAND_DICT[config.__class__.__name__](
                    receiver=service_letter,
                    config=config
                )
            )
