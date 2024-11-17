import datetime
import datetime as dt

import csv
import json

from database.database_api import TaskStatus
from database.database_api import TaskResolution
from database.database_api import TaskType

PATH = './dataset/'


def get_sprint_data(sprint_id: int):
    with open(PATH + 'sprints.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            if int(line['sprint_id']) == sprint_id:
                return line.values()


def get_task_status(raw_status: str) -> TaskStatus:  # TODO: fix
    try:
        return TaskStatus[raw_status.strip()]
    except KeyError:
        return TaskStatus.unknown


def get_task_resolution(raw_resolution: str) -> TaskResolution:
    raw_resolution = raw_resolution.strip()
    if raw_resolution == 'Готово':
        return TaskResolution.DONE
    elif raw_resolution == 'Отклонено':
        return TaskResolution.DECLINED
    elif raw_resolution == 'Дубликат':
        return TaskResolution.DUPLICATE
    elif raw_resolution == 'Отменен инициатором':
        return TaskResolution.CANCELLED
    return TaskResolution.NONE


def get_task_type(raw_type: str) -> TaskType:
    raw_type = raw_type.strip()
    if raw_type == 'Задача':
        return TaskType.TASK
    elif raw_type == 'Подзадача':
        return TaskType.SUBTASK
    elif raw_type == 'Дефект':
        return TaskType.DEFECT
    elif raw_type == 'История':
        return TaskType.HISTORY
    return TaskType.NONE


def parse_history(sprint_id: int, start_date: datetime.datetime):
    fmt = "%m/%d/%y %H:%M"

    status_changes: dict[int, list[tuple[dt.datetime, TaskStatus, float]]] = {}
    resolution_changes: dict[int, list[tuple[dt.datetime, TaskResolution, float]]] = {}
    estimation_changes: dict[int, list[tuple[dt.datetime, int]]] = {}
    with open(PATH + str(sprint_id) + '/history.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            raw_entity_id, property_name, raw_date, raw_version, change = line.values()
            entity_id = int(raw_entity_id)
            version = float(raw_version)

            if property_name == 'Статус':
                before, after = change.split('->')
                time_of_change = dt.datetime.strptime(raw_date, fmt)

                if entity_id not in status_changes:
                    status_changes[entity_id] = [(start_date, get_task_status(before), 0)]

                status_changes[entity_id].append((time_of_change, get_task_status(after), version))

            elif property_name == 'Резолюция':
                lst = change.split('->')
                if len(lst) == 1:  # TODO: fix
                    resolution_changes[entity_id] = [(start_date, TaskResolution.NONE, 0)]
                else:
                    before, after = lst[0], lst[1]
                    if entity_id not in resolution_changes:
                        resolution_changes[entity_id] = [(start_date, get_task_resolution(before), 0)]
                    time_of_change = dt.datetime.strptime(raw_date, fmt)
                    resolution_changes[entity_id].append((time_of_change, get_task_resolution(after), version))

            elif property_name == 'Учет рабочего времени':
                lst = change.split('->')
                if len(lst) == 1:  # TODO: fix
                    estimation_changes[entity_id] = [(start_date, 0)]
                else:
                    if entity_id not in estimation_changes:
                        estimation_changes[entity_id] = [(start_date, 0)]
                    time_of_change = dt.datetime.strptime(raw_date, fmt)
                    dct = json.loads(lst[1])
                    estimation_changes[entity_id].append((time_of_change, int(dct['spent'])))

    return status_changes, resolution_changes, estimation_changes


def get_types(sprint_id: int):
    task_types: dict[int, TaskType] = {}
    with open(PATH + str(sprint_id) + '/etities.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            task_types[int(line['entity_id'])] = get_task_type(line['type'])
    return task_types


def get_final_status(sprint_id: int):
    final_status: dict[int, TaskStatus] = {}
    with open(PATH + str(sprint_id) + '/etities.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            final_status[int(line['entity_id'])] = get_task_status(line['status'])
    return final_status
