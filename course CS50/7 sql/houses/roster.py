#! python3
"""
CS50 PSet 7: Houses roster
Take name of House as argument;
Prints class roster for a given House in alphabetical order.
"""
import cs50
import sys

if len(sys.argv) != 2 or len(sys.argv[1]) > 10:
    print(f"USAGE: python {sys.argv[0]} %HouseName%")
    sys.exit(1)

db = cs50.SQL("sqlite:///students.db")

# Query database for all students in house;
# Students should be ordered by last name, first name.
house = db.execute(
    "SELECT first, middle, last, birth FROM students WHERE house = ? "
    "ORDER BY last ASC, first ASC", sys.argv[1]
)

# Print out, check for None;
for dct in house:
    first = dct['first']
    middle = dct['middle']
    last = dct['last']
    birth = dct['birth']

    middle = " " if middle is None else f" {middle} "

    print(f"{first}{middle}{last}, born {birth}")

sys.exit(0)
