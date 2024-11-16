# from .database import *
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StateFrame:
    Data: datetime
    dvdev: float
    planed: float
    todo: float
    canceled: float
    backlog: float


def get_spring_health(sprint_id: int) -> list[StateFrame]:
    pass
