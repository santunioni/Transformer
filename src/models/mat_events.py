import time

from pydantic import BaseModel

from src.models.service_config import ServiceConfig


class MatEvent(BaseModel):
    event_trace: str
    mat_identifier: str


class ServiceLetter(MatEvent):
    data: dict
    config: ServiceConfig


class Stats(BaseModel):
    time_start: float
    time_end: float
    duration: float


class ServiceResponse(MatEvent):
    service_identifier: str
    stats: Stats = Stats(time_start=time.perf_counter(), time_end=0, duration=0)
    data: dict = {}
    cancel_flow: bool = False

    def finish_stats(self):
        self.stats.time_end = time.perf_counter()
        self.stats.duration = self.stats.time_end - self.stats.time_start
