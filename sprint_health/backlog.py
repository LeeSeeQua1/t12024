import csv
from datetime import datetime
from datetime import timedelta


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
