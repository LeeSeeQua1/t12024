import datetime
import datetime as dt

import csv

from database.database_api import TaskStatus
from database.database_api import ResolutionStatus

PATH = './dataset/'


def get_sprint_data(sprint_id: int):
    with open(PATH + 'sprints.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for i, line in enumerate(reader):
            print(line['sprint_id'])
            if int(line['sprint_id']) == sprint_id:
                return line.values()


def get_task_status(raw_status: str) -> TaskStatus:  # TODO: fix
    try:
        return TaskStatus[raw_status.strip()]
    except KeyError:
        return TaskStatus.unknown


def get_resolution_status(raw_resolution: str) -> ResolutionStatus:
    raw_resolution = raw_resolution.strip()
    if raw_resolution == 'Готово':
        return ResolutionStatus.DONE
    elif raw_resolution == 'Отклонено':
        return ResolutionStatus.DECLINED
    elif raw_resolution == 'Дубликат':
        return ResolutionStatus.DUPLICATE
    elif raw_resolution == 'Отменен инициатором':
        return ResolutionStatus.CANCELLED
    return ResolutionStatus.NONE


def parse_history(sprint_id: int, start_date: datetime.datetime):
    fmt = "%m/%d/%y %H:%M"

    status_changes: dict[int, list[tuple[dt.datetime, TaskStatus, float]]] = {}
    resolution_changes: dict[int, list[tuple[dt.datetime, ResolutionStatus, float]]] = {}
    estimation_changes: dict[int, list[tuple[dt.datetime, int]]] = {}
    with open(PATH + str(sprint_id) + '/history.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for i, line in enumerate(reader):
            if i == 0:
                continue

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
                if len(lst) == 1:
                    resolution_changes[entity_id] = [(start_date, ResolutionStatus.NONE, 0)]
                else:
                    before, after = lst[0], lst[1]
                    if entity_id not in resolution_changes:
                        resolution_changes[entity_id] = [(start_date, get_resolution_status(before), 0)]
                    time_of_change = dt.datetime.strptime(raw_date, fmt)
                    resolution_changes[entity_id].append((time_of_change, get_resolution_status(after), version))

            elif property_name == 'Учет рабочего времени':
                lst = change.split('->')
                print(lst)
                if len(lst) == 1:
                    estimation_changes[entity_id] = [(start_date, 0)]
                else:
                    if entity_id not in estimation_changes:
                        estimation_changes[entity_id] = [(start_date, 0)]
                    time_of_change = dt.datetime.strptime(raw_date, fmt)
                    print(type(lst[0]))
                    estimation_changes[entity_id].append((time_of_change, 0))

    return status_changes, resolution_changes
