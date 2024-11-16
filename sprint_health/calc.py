import datetime as dt

import csv

from database.database_api import TaskStatus
from database.database_api import ResolutionStatus

PATH = '../dataset/'


def get_sprint_data(sprint_id: int):
    with open(PATH + 'sprints.csv', 'r', encoding='utf-8') as f:
        line = f.readline()
        line = f.readline()
        while line != '':
            sid, name, start_date, end_date, entity_ids = line.split(';')
            if int(sid) == sprint_id:
                return sid, name, start_date, end_date, entity_ids
            print(sprint_id, name, start_date, end_date, entity_ids)
            line = f.readline()


def get_task_status(raw_status: str) -> TaskStatus:  # TODO: fix
    try:
        return TaskStatus[raw_status]
    except KeyError:
        return TaskStatus.unknown


def get_resolution_status(raw_resolution: str) -> ResolutionStatus:
    if raw_resolution == 'Готово':
        return ResolutionStatus.DONE
    elif raw_resolution == 'Отклонено':
        return ResolutionStatus.DECLINED
    elif raw_resolution == 'Дубликат':
        return ResolutionStatus.DUPLICATE
    elif raw_resolution == 'Отменен инициатором':
        return ResolutionStatus.CANCELLED
    return ResolutionStatus.NONE


def parse_history(sprint_id: int):
    sid, name, raw_start_date, raw_end_date, entity_ids = get_sprint_data(sprint_id)

    fmt = "%Y-%m-%d %H:%M:%S.%f"
    start_date = dt.datetime.strptime(raw_start_date, fmt)

    fmt = "%m/%d/%y %H:%M"

    status_changes: dict[int, list[tuple[dt.datetime, TaskStatus]]] = {}
    resolution_changes: dict[int, list[tuple[dt.datetime, ResolutionStatus]]] = {}
    with open(PATH + str(sprint_id) + '/history.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for i, line in enumerate(reader):
            if i == 0:
                continue

            raw_entity_id, property_name, raw_date, change = line.values()
            entity_id = int(raw_entity_id)

            if property_name == 'Статус':
                before, after = change.split('->')
                time_of_change = dt.datetime.strptime(raw_date, fmt)

                if entity_id not in status_changes:
                    status_changes[entity_id] = [(start_date, get_task_status(before.strip()))]

                status_changes[entity_id].append((time_of_change, get_task_status(after.strip())))

            if property_name == 'Резолюция':
                lst = change.split('->')
                if len(lst) == 1:
                    resolution_changes[entity_id] = [(start_date, ResolutionStatus.NONE)]
                else:
                    if entity_id not in resolution_changes:
                        resolution_changes[entity_id] = [(start_date, get_resolution_status(before))]
                    time_of_change = dt.datetime.strptime(raw_date, fmt)
                    resolution_changes[entity_id].append((time_of_change, get_resolution_status(after.strip())))

    return status_changes, resolution_changes


st_changes, res_changes = parse_history(0)

test_id = 4502897
print(st_changes[test_id])
print(res_changes[test_id])
