#! python3
""" Read files from forenames.txt and surnames.txt,
    randomly combines and print LIMIT. v3"""
import sys
import random

LIMIT = 5


def get_forenames_and_surnames():
    forenames = []
    surnames = []
    for names, file in ((forenames, "forenames.txt"),
                        (surnames, "surnames.txt")):
        for name in open(file, encoding='utf8'):
            names.append(name.rstrip())
    return forenames, surnames


if len(sys.argv) != 3:
    print(f"USAGE: {sys.argv[0]} forenames.txt surnames.txt")
    sys.exit(1)

forenames, surnames = get_forenames_and_surnames()

random.seed()
years = list(range(1970, 2020)) * 3
for year, forename, surname in zip(random.sample(years, LIMIT),
                                   random.sample(forenames, LIMIT),
                                   random.sample(surnames, LIMIT)):
    name = forename + " " + surname
    print(f"{name:.<25} {year}")
sys.exit(0)
