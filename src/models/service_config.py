from typing import Dict

from pydantic import BaseModel


class ServiceConfig(BaseModel):
    mapping: Dict[str, str] = {}
    preserve_unmapped: bool = True
