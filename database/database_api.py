from datetime import datetime
from enum import IntEnum, Enum


class TaskStatus(Enum):
    closed = 0,
    done = 1,
    created = 2,
    inProgress = 3,
    rejectedByThePerformer = 4,
    testing = 5,
    confirmationOfCorrections = 6,
    analysis = 7,
    fixing = 8,
    hold = 9,
    development = 10,
    st = 11,
    verification = 12,
    localization = 13,
    stCompleted = 14,
    readyForDevelopment = 15,
    waiting = 16,
    unknown = 17


class TaskResolution(IntEnum):
    DONE = 0
    DECLINED = 1
    DUPLICATE = 2
    CANCELLED = 3
    NONE = 4


class TaskType(IntEnum):
    TASK = 0,
    SUBTASK = 1,
    DEFECT = 2,
    HISTORY = 3,
    NONE = 4


# def get_task_ids(sprint_id: int) -> list[int]:
#     pass
#
#
# def get_status(task_id: int) -> list[TaskStatus]:
#     pass

def get_tasks_names(sprint_id: int) -> list[str]:
    pass
