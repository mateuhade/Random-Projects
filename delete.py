import csv
import random

with open("small_data_set.csv", "r") as file:
    reader = csv.DictReader(file)
    original_rows = list(reader)

rows_to_keep = []

for row in original_rows:
    is_erasing = random.randint(0, 1)
    if not is_erasing:
        rows_to_keep.append(row)

with open("small_data_set.csv", "w") as file:
    fieldnames = ["small", "data", "set", "value"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows_to_keep)

    
