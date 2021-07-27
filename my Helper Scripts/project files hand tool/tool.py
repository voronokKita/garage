#!python3
"""
I have a very important project for which I came up with a special file naming structure.
Each file has a date, a four-digit counter, optional 1-3 letters of the category, and a name.
Like:
2021.01.12.0000.file, 2021.01.12.0001.file, 2021.01.12.0002.file, 2021.01.12.0003.aaa.file

I found this clear naming structure very nice. I can always change the structure of the project or even put all the files in one directory, and they all line up in a careful order, no two files can conflict. 

Since the project is huge, it is impossible for me to keep it in order myself. I wrote this tool to automatically check all files, regardless of the directory in which they are located. The script points me to files with incorrect names, brings the names to the standard and fixes the counters in cases where they are messed up or the files have been deleted. 
"""
import re
import sys
import shutil
import pathlib
from time import sleep
from send2trash import send2trash
from collections import defaultdict


SPEED = 1

""" Project structure """
folder = pathlib.Path(__file__).resolve().parent
PROJECT = [
    pathlib.Path(f"{folder}/1 dir"),
    pathlib.Path(f"{folder}/2 dir"),
    pathlib.Path(f"{folder}/3 dir"),
    pathlib.Path(f"{folder}/4 dir"),
    pathlib.Path(f"{folder}/5 dir"),
    pathlib.Path(f"{folder}/6 dir")
]

OLD_FILES = pathlib.Path(f"{folder}/OLD")

PATTERN = re.compile(r'''(
        (\d{4}\.\d\d\.\d\d\.)   # date
        (\d{4})                 # counter
        (\.\w{1,3})?            # categorie
        (\..+)                  # filename (and extention)
    )''', re.VERBOSE)

class FilesLostError(Exception): pass


def main():
    sleep(SPEED)
    project_content = load_files()
    initial_amount = len(project_content)
    print(initial_amount, "files found")
    
    sleep(SPEED)
    errors = check_filenames(project_content)
    if errors:
        print(errors, "incorrect names.")
        sys.exit(1)
    else:
        print("all files have correct name structure")

    OLD_FILES.mkdir()

    sleep(SPEED)
    errors = lower_case(project_content)
    if not errors:
        print("all files are lower case")
    else:
        print(errors, "files ranamed")
        project_content = load_files()
        if len(project_content) != initial_amount:
            raise FilesLostError(f"ERROR. number of files changed! was {initial_amount}, became {len(project_content)}")
    
    sleep(SPEED)
    incorrect_counters = sort_dates(project_content)
    
    if not incorrect_counters:
        print("all counters are correct")
    else:
        print(len(incorrect_counters), "dates have an incorrect counter")
        sleep(SPEED + 1)
        print("overcount:")
        errors = overcount(incorrect_counters)
        print(errors, "files ranamed")
        ranamed_files = load_files()
        if len(ranamed_files) != initial_amount:
            raise FilesLostError(f"ERROR. number of files changed! was {initial_amount}, became {len(ranamed_files)}")

    sleep(SPEED)
    if OLD_FILES.exists():
        send2trash(str(OLD_FILES))
    print("Clear.")
    sys.exit(0)
        

def load_files():
    """ Load paths of files """
    project_content = []    
    for dir in PROJECT:
        assert dir.exists(), "project structure has changed"
        project_content += [item for item in dir.rglob('*') if item.is_file()]
    
    return project_content


def check_filenames(project_content):
    """ Check filenames """
    errors = 0
    for file in project_content:
        if not PATTERN.search(file.name):
            print("<incorrect filename>\t", file)
            errors += 1
            sleep(SPEED / 10)

    return errors
        

def lower_case(project_content):
    """ Check lower case """
    errors = 0
    for file in project_content:
        if not str(file.name).islower():
            print("-to lower case-\t", file.name)

            old_file = pathlib.Path(OLD_FILES, f"{file.name} (capitalised old)")
            shutil.copy(file, old_file)

            new_name = str(file.name).lower()
            file.rename(pathlib.Path(file.parent, new_name))

            errors += 1
            sleep(SPEED / 10)
        
    return errors


def sort_dates(project_content):
    """ Sort files on name and group on date,
        check files counters;
        return dict with incorrect counters """
    date_dictionary = defaultdict(list)

    sorted_files = sorted(project_content, key=lambda file: file.name)

    for file in sorted_files:
        date = PATTERN.findall(file.name)[0][1]
        date_dictionary[date] += [file]

    incorrect_counters = {}
    for date in date_dictionary:
        files = date_dictionary[date]
        for i, file in enumerate(files):
            counter = PATTERN.findall(file.name)[0][2]
            if i != int(counter):
                print(date, "incorrect counters")
                incorrect_counters[date] = files
                sleep(SPEED / 10)
                break
    
    return incorrect_counters


def overcount(incorrect_counters):
    """ Overwrite counters;
        unfortunately the process must be duplicated to avoid conflicts """
    errors = 0
    renamed = []
    for date in incorrect_counters:  
        files = incorrect_counters[date]
        for i, file in enumerate(files):
            old_file = pathlib.Path(OLD_FILES, f"{file.name} (old)")
            shutil.copy(file, old_file)

            parts = PATTERN.findall(file.name)[0][1:]
            file_date = parts[0]
            counter = f"{i:04d}"
            categorie = parts[2]
            filename = parts[3]
            new_name = file_date + counter + categorie + filename
            file = file.rename(pathlib.Path(file.parent, f"{new_name} (new)"))

            renamed.append(file)
            print(new_name)
            errors += 1
            sleep(SPEED / 10)
    
    for file in renamed:
        new_name = str(file.name).replace(" (new)", "")
        file.rename(pathlib.Path(file.parent, new_name))

    return errors


if __name__ == "__main__":
    main()
