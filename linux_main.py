from sprint_health.backlog import get_start_date
from database.data_split import data_split


data_split(
    "./dataset/sprints-Table 1.csv",
    "./dataset/data_for_spb_hakaton_entities1-Table 1.csv",
    "./dataset/history-Table 1.csv")

print(get_start_date(0))




print("Linux unsupported")
