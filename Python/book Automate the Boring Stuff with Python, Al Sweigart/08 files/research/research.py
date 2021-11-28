#! python3
""" Asks the user for a regular expression,
    opens all csv files in a folder
    searches them for a re
    and output the result. """
import re
import sys
import csv
import time
import pathlib

# search directory for csv files;
current_dir = pathlib.Path.cwd()
folder_content = pathlib.Path(current_dir)
files = []
for item in folder_content.iterdir():
    if item.is_file() and item.name.endswith('.csv'):
        files.append(item)
else:
    time.sleep(0.5)
    if len(files) == 0:
        print("Nothing to regular express about :(")
        sys.exit(0)
    else:
        print(f"{len(files)} files found;")
time.sleep(1)

# ask for re to search, create spell;
regular_expression = input("Construct your regular expression: ")
regex = re.compile(regular_expression)
time.sleep(0.5)
print("Casting your spell...")
time.sleep(2)

# get text from a files;
# cast regular expression and collect successful results in a dictionary;
# {'filename result-num, row-num:': 'result'}
results = {}
result_num = 1
for file in files:
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row, content in enumerate(reader):
            text = ", ".join(content)
            findings = regex.findall(text)  # list of strings or tuples
            if len(findings) > 0:
                key = f"{file.name} {result_num}, row {row}:"
                results[key] = findings
                result_num += 1

# output;
if len(results) > 0:
    print("Done!")
    time.sleep(1)
    print("The results of your magic construction:")
    time.sleep(2)
    for key in results:
        print(key, results[key])
        time.sleep(0.01)
else:
    print("Magic had no effect.")

# Done.
sys.exit(0)
