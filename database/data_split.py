import os
import shutil
import csv

#hui

SPRINTS_PATH = '../dataset/sprints-Table 1.csv'
ENTRY_PATH = '../dataset/data_for_spb_hakaton_entities1-Table 1.csv'
HISTORY_PATH = '../dataset/history-Table 1.csv'

DATA_PATH = '../dataset'

S_COLUMNS = ["sprint_id", "entity_ids"]
E_COLUMNS = ["entity_id", "status", "priority"]
H_COLUMNS = ["entity_id", "history_property_name", "history_date", "history_change"]


def parse_set(s: str) -> set[int]:  # TODO move to constants
    return set(map(int, s[1:-1].split(',')))


with open(SPRINTS_PATH, "r", newline='') as s_file:
        write_s_file = open(DATA_PATH + "/" + "sprints.csv", "w", newline='')
        writer_s = csv.writer(write_h_file, delimiter=';')







with open(SPRINTS_PATH, "r", newline='') as s_file:
    s_reader = csv.DictReader(s_file, delimiter=';')
    sprint_id = 0
    for s_row in s_reader:
        sprint, set_ids = s_row["sprint_name"], parse_set(s_row["entity_ids"])
        wd = DATA_PATH + '/' + sprint_id

        try:
            shutil.rmtree(wd)
        except:
            pass
        os.mkdir(wd)

        e_file = open(ENTRY_PATH, "r", newline='')
        e_reader = csv.DictReader(e_file, delimiter=';')
        write_e_file = open(wd + '/' + "etities.csv", "w", newline='')
        writer_e = csv.writer(write_e_file, delimiter=';')
        writer_e.writerow(E_COLUMNS)
        for e_row in e_reader:
            if int(e_row["entity_id"]) in set_ids:
                writer_e.writerow([value for key, value in e_row.items() if key in E_COLUMNS])
        write_e_file.close()

        h_file = open(HISTORY_PATH, "r", newline='')
        h_reader = csv.DictReader(h_file, delimiter=';')
        write_h_file = open(wd + '/' + "history.csv", "w", newline='')
        writer_h = csv.writer(write_h_file, delimiter=';')
        writer_h.writerow(H_COLUMNS)
        for h_row in h_reader:
            if h_row["entity_id"] == "":
                continue

            if int(h_row["entity_id"]) in set_ids:
                writer_h.writerow([value for key, value in h_row.items() if key in H_COLUMNS])
        write_h_file.close()

        sprint_id += 1
