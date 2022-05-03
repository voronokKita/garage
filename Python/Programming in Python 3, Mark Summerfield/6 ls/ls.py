#! python3
""" summer 2020
Unix ls command analogue.
Scan directories for files with parameters:
-H, --hidden        show hidden files
-m, --modified      show last modified date/time
-r, --recursive     recurse into subdirectories
-s, --sizes         show sizes
-o[str], --order[str]   order by [str]
        [str]: 'name' or 'n', 'modified' or 'm', 'size' or 's'
"""
import sys
import time
import pathlib
import optparse
import collections
from hurry import filesize

VERSION = '1'
USAGE = f"USAGE: {sys.argv[0]} (options) [path1 path2 ... pathN]"
Files = collections.namedtuple("File", "name modified size hidden")


def main():
    files = []
    options, arguments = arguments_work()

    scan_directories(options, arguments, files)
    if len(files) == 0:
        print("No files found.")
        sys.exit(0)

    sorted_files = sort_order(files, options)

    print_to_user(sorted_files, options)
    sys.exit(0)


def arguments_work():
    """ Scan and filter user options. """
    parser = optparse.OptionParser(
        version=VERSION, usage=USAGE,
        description="The paths are optional; if not given ./ is used."
    )
    parser.add_option(
        '-H', '--hidden', action='store_true', dest='hidden',
        help="show hidden files [default: off]"
    )
    parser.add_option(
        '-m', '--modified', action='store_true', dest='modified',
        help="show last modified date/time [default: off]"
    )
    parser.add_option(
        '-r', '--recursive', action='store_true', dest='recursive',
        help="recurse into subdirectories [default: off]"
    )
    parser.add_option(
        '-s', '--sizes', action='store_true', dest='sizes',
        help="show sizes [default: off]"
    )
    parser.add_option(
        '-o', '--order', action='store', dest='order',
        choices=['name', 'n', 'modified', 'm', 'size', 's'],
        help="order by ('name' or 'n', 'modified' or 'm', 'size' or 's') [default: name]"
    )
    parser.set_defaults(hidden=False, modified=False, recursive=False, sizes=False, order='name')

    options, arguments = parser.parse_args()
    return options, arguments


def scan_directories(options, arguments, files):
    """ Scan directories with options. Fill list of files. """
    paths = []
    if len(arguments) == 0:
        paths.append(".")
    else:
        for i in range(len(arguments)):
            paths.append(arguments[i])

    path = 0
    while True:
        if path >= len(paths):
            break

        folder_content = pathlib.Path(paths[path])

        for item in folder_content.iterdir():
            if item.is_file():
                if item.name.startswith('.'):
                    if options.hidden is True:
                        file_hidden = True
                    else:
                        continue
                else:
                    file_hidden = False

                file_name = item.name
                file_modified = item.stat().st_mtime
                file_size = item.stat().st_size

                file = Files(file_name, file_modified, file_size, file_hidden)
                files.append(file)

            elif item.is_dir() and options.recursive is True:
                if item.name.startswith('.') and options.hidden is True:
                    pass
                else:
                    new_dir_path = pathlib.Path(item).absolute()
                    paths.append(new_dir_path)

        path += 1


def sort_order(list_to_sort, options):
    # file = Files("name modified size hidden")
    if options.order in {'name', 'n'}:
        mode = 0
    elif options.order in {'modified', 'm'}:
        mode = 1
    elif options.order in {'size', 's'}:
        mode = 2

    files = sorted(list_to_sort, key=lambda file: file[mode])
    return files


def print_to_user(files, options):
    """ like: '2021-01-14 16:43:27 200K test.py (hidden)' """
    modwidth = 21
    sizewidth = 6

    for file in files:
        name = file.name
        file_modified = ""
        file_size = ""
        file_hidden = ""

        if options.modified is True:
            t = time.localtime(file.modified)
            t = time.strftime('%Y-%m-%d %H:%M:%S', t)
            file_modified = f"{t:<{modwidth}}"
        if options.sizes is True:
            s = filesize.size(file.size)
            file_size = f"{s:<{sizewidth}}"
        if file.hidden is True:
            file_hidden = " (hidden)"

        print(f"{file_modified}{file_size}{name}{file_hidden}")


if __name__ == "__main__":
    main()
