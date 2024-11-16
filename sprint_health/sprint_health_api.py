from dataclasses import dataclass
from datetime import datetime


from sprint_health.calc import get_sprint_data
from sprint_health.calc import parse_history


@dataclass
class StateFrame:
    Data: datetime
    dvdev: float
    planed: float
    todo: float
    canceled: float
    backlog: float


def get_spring_health(sprint_id: int) -> list[StateFrame]:
    sid, name, raw_start_date, raw_end_date, entity_ids = tuple(get_sprint_data(sprint_id))

    fmt = "%Y-%m-%d %H:%M:%S.%f"
    start_date = datetime.strptime(raw_start_date, fmt)
    end_date = datetime.strptime(raw_end_date, fmt)

    print(parse_history(0, start_date))
