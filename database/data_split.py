import os
import shutil
import csv

# S_COLUMNS = ["sprint_id", "sprint_name", "entity_ids"]
# E_COLUMNS = ["entity_id", "area", "status", "priority"]
# H_COLUMNS = ["entity_id", "history_property_name", "history_date", "history_change"]

S_COLUMNS = ["sprint_id", "sprint_name", "sprint_start_date", "sprint_end_date", "entity_ids"]
E_COLUMNS = ["entity_id", "type", "status", "resolution"]
H_COLUMNS = ["entity_id", "history_property_name", "history_date", "history_version", "history_change"]

DATASET_PATH = 'dataset'
NEW_SPRINTS_PATH = f'{DATASET_PATH}/sprints.csv'


def data_split(sprints_path: str, entry_path: str, history_path: str) -> int:
    def parse_set(s: str) -> set[int]:  # TODO move to constants
        return set(map(int, s[1:-1].split(',')))

    # parse sprints file, add ids
    sprint_cnt = 0
    with open(sprints_path, "r", newline='', encoding='utf-8') as s_file:
        s_reader = csv.DictReader(s_file, delimiter=';')

        try:
            os.remove(NEW_SPRINTS_PATH)
        except:
            pass

        with open(NEW_SPRINTS_PATH, "w", newline='', encoding='utf-8') as write_s_file:
            writer_s = csv.writer(write_s_file, delimiter=';')
            writer_s.writerow(S_COLUMNS)
            for s_row in s_reader:
                writer_s.writerow([str(sprint_cnt)] + [value for key, value in s_row.items() if key in S_COLUMNS])
                sprint_cnt += 1

    with open(NEW_SPRINTS_PATH, "r", newline='', encoding='utf-8') as s_file:
        s_reader = csv.DictReader(s_file, delimiter=';')
        for s_row in s_reader:
            sprint_id, set_ids = s_row["sprint_id"], parse_set(s_row["entity_ids"])
            wd = DATASET_PATH + '/' + str(sprint_id)

            try:
                shutil.rmtree(wd)
            except:
                pass
            os.mkdir(wd)

            e_file = open(entry_path, "r", newline='', encoding='utf-8')
            e_reader = csv.DictReader(e_file, delimiter=';')
            write_e_file = open(wd + '/' + "etities.csv", "w", newline='', encoding='utf-8')
            writer_e = csv.writer(write_e_file, delimiter=';')
            writer_e.writerow(E_COLUMNS)
            for e_row in e_reader:
                if int(e_row["entity_id"]) in set_ids:
                    writer_e.writerow([value for key, value in e_row.items() if key in E_COLUMNS])
            write_e_file.close()
            e_file.close()

            h_file = open(history_path, "r", newline='', encoding='utf-8')
            h_reader = csv.DictReader(h_file, delimiter=';')
            write_h_file = open(wd + '/' + "history.csv", "w", newline='', encoding='utf-8')
            writer_h = csv.writer(write_h_file, delimiter=';')
            writer_h.writerow(H_COLUMNS)
            for h_row in h_reader:
                if h_row["entity_id"] == "":
                    continue

                if int(h_row["entity_id"]) in set_ids:
                    writer_h.writerow([value for key, value in h_row.items() if key in H_COLUMNS])
            write_h_file.close()
            h_file.close()

    return sprint_cnt
