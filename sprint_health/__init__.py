from database import *
from dataclasses import dataclass


@dataclass(frozen=True)
class SprintHealth:
    correct_order: int
    good_planning: int
    to_do_percentage: int
    cancelled_percentage: int
    backlog: int


def get_sprint_health(sprint_id: int, time: datetime) -> SprintHealth:
    for task_id in get_task_ids(sprint_id):
        pass
