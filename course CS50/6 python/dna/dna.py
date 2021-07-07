"""
CS50 PSet 6: DNA
Identifies a person based on their DNA.
"""
import sys
import csv
import string


# Check command line;
if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} data.csv sequence.txt")
    sys.exit(1)

# Read csv data:
with open(sys.argv[1]) as data:
    reader = csv.reader(data)
    database = list(row for row in reader)

    # Extract Short Tandem Repeats;
    STRs = database.pop(0)
    STRs = STRs[1:]

    # Convert to dict with int values.
    database = {lst[0]: list(map(int, lst[1:])) for lst in database}

# Read DNA sequence:
with open(sys.argv[2]) as sequence:
    DNA = sequence.read()
    DNA = DNA[0:-1]

# Couts STRs in DNA funny way:
i = 0
STRs_couts = []
while i < len(STRs):
    # Autoreplase STRs patterns;
    pattern = STRs[i]
    sequence = DNA.replace(pattern, "1")

    # Autoreplase other;
    s = ""
    alphabet = string.ascii_letters
    for c in sequence:
        s += ' ' if c in alphabet else c

    # Generate list of STRs sequences;
    STRs_list = [l for l in s.split(' ') if len(l) > 0]

    # Take longest STR sequence;
    count_max = 0
    for l in STRs_list:
        count_max = len(l) if count_max < len(l) else count_max

    STRs_couts.append(count_max)
    i += 1

# Compare counts with person's from database:
for key in database:
    if database[key] == STRs_couts:
        print(key)
        sys.exit(0)

# If the comparison does not fit.
print("No match")
sys.exit(0)
