import pandas as pd

from constants import SPRINTS_PATH

df_sprints: pd.DataFrame = pd.read_csv(SPRINTS_PATH, sep=';', on_bad_lines='warn', index_col="sprint_name")

SPRINT_ENTRIES: dict[str, set[int]] = {}
for sprint, row in df_sprints.iterrows():
    SPRINT_ENTRIES[sprint] = set(map(int, row["entity_ids"][1:-1].split(',')))
