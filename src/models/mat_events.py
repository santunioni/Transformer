from __future__ import annotations

from pydantic import BaseModel
from src.models.service_config import ServiceConfig


class MatEvent(BaseModel):
    event_trace: str
    mat_id: str
    metadata: dict = {}
    data: dict


class Orquestrable(MatEvent):
    index_in_flow: int


class ServiceLetter(Orquestrable):
    config: ServiceConfig


class ServiceResponse(Orquestrable):
    cancel_flow: bool = False

    @staticmethod
    def from_letter(service_letter: ServiceLetter) -> ServiceResponse:
        return ServiceResponse(
            event_trace=service_letter.event_trace,
            mat_id=service_letter.mat_id,
            index_in_flow=service_letter.index_in_flow,
            data={},
        )
