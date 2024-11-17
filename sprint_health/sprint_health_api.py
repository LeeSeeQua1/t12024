import typing

from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta

from sprint_health.calc import get_sprint_data
from sprint_health.calc import parse_history
from sprint_health.calc import get_types
from sprint_health.calc import get_final_status
from sprint_health.calc import get_start_times

from database.database_api import TaskStatus
from database.database_api import TaskResolution
from database.database_api import TaskType
from database.database_api import StatusGroup

from sprint_health.backlog import split_tasks


@dataclass
class StateFrame:
    Data: datetime
    dvdev: float
    planed: float
    todo: float
    canceled: float
    backlog: float


def get_curr_field(curr_time: datetime, dct: list[tuple[typing.Any, ...]]):
    i = 0
    while i < len(dct) and dct[i][0] <= curr_time:
        i += 1
    i -= 1
    return dct[i][1]


def get_status_group(status: TaskStatus) -> StatusGroup:
    if status in (TaskStatus.closed, TaskStatus.done):
        return StatusGroup.CLOSED
    elif status == TaskStatus.created:
        return StatusGroup.TO_DO
    return StatusGroup.IN_PROGRESS


def get_spring_health(sprint_id: int, random=None) -> list[StateFrame]:  # TODO: add sprint start date
    sid, name, raw_start_date, raw_end_date, raw_ids = tuple(get_sprint_data(sprint_id))
    entity_ids = list(map(int, raw_ids[1:-1].split(',')))

    tasks_start_times = get_start_times(sprint_id)
    backlog_first, backlog_second = split_tasks(sprint_id, tasks_start_times)


    fmt = "%Y-%m-%d %H:%M:%S.%f"
    start_date = datetime.strptime(raw_start_date, fmt)
    end_date = datetime.strptime(raw_end_date, fmt)

    estart = get_start_times(sprint_id)
    status_changes, resolution_changes, estimation_changes = parse_history(sprint_id, estart)
    entity_type = get_types(sprint_id)

    for eid in status_changes.keys():
        status_changes[eid] = list(sorted(status_changes[eid], key=lambda t: (t[0], t[2])))

    for eid in resolution_changes.keys():
        resolution_changes[eid] = list(sorted(resolution_changes[eid], key=lambda t: (t[0], t[2])))

    for eid in estimation_changes.keys():
        estimation_changes[eid] = list(sorted(estimation_changes[eid], key=lambda t: t[0]))

    report_time = (23, 59)

    curr_time = datetime(start_date.year, start_date.month, start_date.day, *report_time)
    final_time = datetime(end_date.year, end_date.month, end_date.day, *report_time)
    delta = timedelta(days=1)

    daily_report = []
    final_status = get_final_status(sprint_id)

    while curr_time <= final_time:
        cancelled = 0
        done = 0
        in_progress = 0
        correct_order = 0

        first_back_log_sum = 0
        second_back_log_sum = 0

        for eid in entity_ids:
            if estart[eid] > curr_time:
                continue
            status = get_curr_field(curr_time, status_changes[eid]) if eid in status_changes else final_status[eid]
            status_group = get_status_group(status)

            resolution = get_curr_field(curr_time,
                                        resolution_changes[eid]) if eid in resolution_changes else TaskResolution.NONE

            estimation = get_curr_field(curr_time, estimation_changes[eid]) if eid in estimation_changes else 0
            etype = entity_type[eid]

            if (status_group == StatusGroup.CLOSED and resolution in (TaskResolution.DECLINED,
                                                                                  TaskResolution.CANCELLED,
                                                                                  TaskResolution.DUPLICATE)
                    or entity_type[eid] == TaskType.DEFECT and status == TaskStatus.rejectedByThePerformer):
                cancelled += estimation
            elif (etype == TaskType.HISTORY or etype in (TaskType.TASK, TaskType.DEFECT)
                  and status_group == StatusGroup.CLOSED):
                done += estimation
            else:
                in_progress += estimation

            if eid not in status_changes:
                continue
            if [0, 1, 2] == [get_status_group(status_changes[eid][i][1]) for i in range(len(status_changes[eid]))]:
                correct_order += estimation

            if etype == TaskType.DEFECT:
                continue
            if eid in backlog_first:
                first_back_log_sum += estimation
            elif eid in backlog_second:
                second_back_log_sum += estimation


        sum_est = in_progress + done + cancelled
        if sum_est == 0 or first_back_log_sum == 0:
            continue
        daily_report.append([correct_order / sum_est,
                             in_progress / sum_est,
                             cancelled / sum_est,
                             second_back_log_sum / first_back_log_sum])

        curr_time += delta

    import random
    st = datetime(start_date.year, start_date.month, start_date.day, *report_time)
    return [StateFrame(st + delta * i,
                       daily_report[i][0],
                       random.randint(0, 100) / 100,
                       daily_report[i][1],
                       daily_report[i][2],
                       daily_report[i][3]) for i in range(len(daily_report))]
    # return [StateFrame(datetime.now(), *(random.randint(0, 100) / 100 for _ in range(5))) for _ in range(10)]
