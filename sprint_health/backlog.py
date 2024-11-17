import csv
from datetime import datetime
from datetime import timedelta


def get_start_date(sprint_pid: int) -> dict[int, datetime]:
    dct: dict[int, datetime] = {}
    with open(f"./dataset/{str(sprint_pid)}/etities.csv", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            dct[int(row["entity_id"])] = datetime.strptime(row["create_date"], "%Y-%m-%d %H:%M:%S.%f")
    return dct


def get_sprint_field(sprint_id: int, field: str) -> str:
    with open('./dataset/sprints.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            if int(line['sprint_id']) == sprint_id:
                return line[field]


def get_sprint_start_time(sprint_id: int) -> datetime:
    return datetime.strptime(get_sprint_field(sprint_id, "sprint_start_date"), "%Y-%m-%d %H:%M:%S.%f")


def split_tasks(sprint_id: int, task_times: dict[int, datetime]) -> tuple[set[int], set[int]]:
    bkpoint = get_sprint_start_time(sprint_id) + timedelta(days=2)
    first: set[int] = {key for key, value in task_times.items() if value < bkpoint}
    second: set[int] = {key for key, value in task_times.items() if value >= bkpoint}
    return first, second



#
#
#
#
# import typing
#
# from dataclasses import dataclass
#
# from sprint_health.calc import get_sprint_data
# from sprint_health.calc import parse_history
# from sprint_health.calc import get_types
# from sprint_health.calc import get_final_status
# from sprint_health.calc import get_start_times
#
# from database.database_api import TaskStatus
# from database.database_api import TaskResolution
# from database.database_api import TaskType
#
#
# @dataclass
# class StateFrame:
#     Data: datetime
#     dvdev: float
#     planed: float
#     todo: float
#     canceled: float
#     backlog: float
#
#
# def get_curr_field(curr_time: datetime, dct: list[tuple[typing.Any, ...]]):
#     i = 0
#     while i < len(dct) and dct[i][0] <= curr_time:
#         i += 1
#     i -= 1
#     return dct[i][1]
#
#
# def get_spring_health(sprint_id: int, random=None) -> list[StateFrame]:  # TODO: add sprint start date
#     sid, name, raw_start_date, raw_end_date, raw_ids = tuple(get_sprint_data(sprint_id))
#     entity_ids = list(map(int, raw_ids[1:-1].split(',')))
#
#     tasks_start_times = get_start_times(sprint_id)  # ------------------------------
#     backlog_first, backlog_second = split_tasks(sprint_id, tasks_start_times)  # ------------------------------
#
#     fmt = "%Y-%m-%d %H:%M:%S.%f"
#     start_date = datetime.strptime(raw_start_date, fmt)
#     end_date = datetime.strptime(raw_end_date, fmt)
#
#     estart = get_start_times(sprint_id)
#     status_changes, resolution_changes, estimation_changes = parse_history(sprint_id, estart)
#     entity_type = get_types(sprint_id)
#
#     for eid in status_changes.keys():
#         status_changes[eid] = list(sorted(status_changes[eid], key=lambda t: (t[0], t[2])))
#
#     for eid in resolution_changes.keys():
#         resolution_changes[eid] = list(sorted(resolution_changes[eid], key=lambda t: (t[0], t[2])))
#
#     for eid in estimation_changes.keys():
#         estimation_changes[eid] = list(sorted(estimation_changes[eid], key=lambda t: t[0]))
#
#     report_time = (23, 59)
#
#     curr_time = datetime(start_date.year, start_date.month, start_date.day, *report_time)
#     final_time = datetime(end_date.year, end_date.month, end_date.day, *report_time)
#     delta = timedelta(days=1)
#
#     while curr_time <= final_time:
#         first_back_log_sum = 0
#         second_back_log_sum = 0
#         for eid in entity_ids:
#             estimation = get_curr_field(curr_time, estimation_changes[eid]) if eid in estimation_changes else 0
#             # ------------------------------
#             if curr_time >= tasks_start_times[eid]:
#                 if eid in backlog_first:
#                     first_back_log_sum += estimation
#                 elif eid in backlog_second:
#                     second_back_log_sum += estimation
#
#                 if first_back_log_sum == 0:
#                     first_back_log_sum = 1
#
#                 print(second_back_log_sum / first_back_log_sum)
#             # ------------------------------
#         curr_time += delta
#
#     return []
#
#     #
#     #
#     #
#     #
#     # import random
#     # st = datetime(start_date.year, start_date.month, start_date.day, *report_time)
#     # return [StateFrame(st + delta * i,
#     #                    *(random.randint(0, 100) / 100 for _ in range(2)),
#     #                    *daily_report[i]) for i in range(len(daily_report))]
#     # return [StateFrame(datetime.now(), *(random.randint(0, 100) / 100 for _ in range(5))) for _ in range(10)]
#
#
