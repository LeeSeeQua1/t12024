import csv
from datetime import datetime


def get_start_date(sprint_pid: int) -> dict[int, datetime]:
    dct: dict[int, datetime] = {}
    with open(f"./dataset/{str(sprint_pid)}/etities.csv", "r", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            dct[int(row["entity_id"])] = datetime.strptime(row["create_date"], "%Y-%m-%d %H:%M:%S.%f")
    return dct


