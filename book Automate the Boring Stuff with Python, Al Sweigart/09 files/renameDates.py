#! python3
""" My implementation of date file rename;
    renames filenames with American MM-DD-YYYY
    date format to European DD-MM-YYYY. """
import re
import sys
import time
import pathlib

# re;
regex = re.compile(r'(\d\d)-(\d\d)-(\d{4})')

# load files;
current_dir = pathlib.Path.cwd()
folder_content = pathlib.Path(current_dir)

# process each file;
# use re for search and replace;
try:
    for item in folder_content.iterdir():
        if item.is_file():
            directory = item.parent
            old_name = item.name
            new_name = regex.sub(r'\2-\1-\3', item.name)
            item.rename(
                pathlib.Path(directory, new_name)
            )
            time.sleep(0.01)
            print(old_name, "rename to", new_name)
except OSError as err:
    print("ERROR.", err)
    sys.exit(1)

# Done.
sys.exit(0)
