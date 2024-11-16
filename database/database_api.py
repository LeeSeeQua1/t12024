from datetime import datetime
from enum import IntEnum


class TaskStatus(IntEnum):
    TO_DO = 0
    IN_PROGRESS = 2
    CLOSED = 3
    CANCELLED = 4
    OTHER = 5


def get_task_ids(sprint_id: int) -> list[int]:
    pass


def get_status(task_id: int, data: datetime) -> TaskStatus:
    pass
