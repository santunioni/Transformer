import ujson
from pydantic import BaseModel

from src.the_flash.utils import ujson_dumps


class BaseCommandConfig(BaseModel):

    def __hash__(self):
        return hash(str(self))

    class Config:
        json_dumps = ujson_dumps
        json_loads = ujson.loads
