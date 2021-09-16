from typing import Union, Optional, Literal

from pydantic import StrictStr, StrictBool, StrictFloat, StrictInt

from src.service.transform.abstract import Transformer, TransformerConfig


class EmpiricusChangeKeyValueConfig(TransformerConfig):
    command_name: Literal["empiricus-change"]
    key_1: str = 'plan_type'
    key_2: str = 'proposal_status'
    new_value: Optional[Union[StrictStr, list, dict, StrictInt, StrictFloat, StrictBool]] = True


class EmpiricusChangeKeyValue(Transformer):

    def __init__(self, config: EmpiricusChangeKeyValueConfig):
        """"""
        super().__init__(config)
        self.__config = config

    def transform(self, data: dict, metadata: dict) -> dict:
        """

        :return:
        """
        data_copy = data.copy()
        try:
            value_1 = data[self.__config.key_1]
            value_2 = data[self.__config.key_2]
            del data[self.__config.key_1]
            del data[self.__config.key_2]
            new_key_1 = self.__config.key_1 + '_' + value_1.lower()
            new_key_2 = self.__config.key_2 + '_' + value_1.lower()
            data[new_key_1] = self.__config.new_value
            data[new_key_2] = value_2
        except KeyError:
            return data_copy
        finally:
            return data
