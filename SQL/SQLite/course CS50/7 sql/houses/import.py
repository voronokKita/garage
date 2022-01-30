#! python3
"""
fall 2020 CS50 PSet 7: Houses import
Import student data from a CSV spreadsheet;
Insert each student into a students.db database.
"""
import cs50
import sys
import csv


if len(sys.argv) != 2:
    print(f"USAGE: python {sys.argv[0]} characters.csv")
    sys.exit(1)

db = cs50.SQL("sqlite:///students.db")

with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)

    # For each row parse name, house and int(date)
    for dct in reader:
        name = dct['name'].split()
        house = dct['house']
        birth = int(dct['birth'])

        # 'None' for student's who don't have middle name
        if len(name) == 2:
            first = name[0]
            middle = None
            last = name[1]
        elif len(name) == 3:
            first = name[0]
            middle = name[1]
            last = name[2]

        db.execute(
            "INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
            first, middle, last, house, birth
        )

sys.exit(0)
