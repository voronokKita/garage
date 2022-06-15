#! python3
"""
Rename screenshots and other pictures in a script folder.

v1 fall 2020
refactor in winter 2022
"""
import sys
import time
import pathlib
import collections

VERSION = '2'
MODES = ['modified', 'name']
PICTURES_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tga")
Files = collections.namedtuple("File", "path sort_key")


def main():
    rename, number, mode = parameters()

    files = []
    scan_directory(files, mode)

    print("Process:")
    process(rename, number, files)

    print("Process successful.")
    sys.exit(0)


def parameters():
    """ Get filenames and start number """
    print(f"Screenshots and pictures rename v{VERSION}")

    new_filename = None
    while not new_filename:
        new_filename = input("\twhat will be the name of files? ")

    number = -1
    while number < 0:
        try:
            number = int(input("\tcount from where? "))
        except ValueError:
            continue

    mode = None
    m = ", ".join(MODES)
    while True:
        mode = input(f"\tmode[{m}]? ").lower()
        if mode and mode in MODES:
            break

    return new_filename, number, mode


def scan_directory(files, mode):
    """ Scan directory; fill list of files """

    folder_content = pathlib.Path('./')
    for item in folder_content.iterdir():
        if not item.is_file() or not item.name.endswith(PICTURES_FORMATS):
            continue

        sort_key = None

        if mode == 'modified':
            t = time.localtime(
                item.stat().st_mtime
            )
            sort_key = time.strftime('%Y-%m-%d %H:%M:%S', t)

        elif mode == 'name':
            # LIKE vlcsnap-2021-03-15-21h55m55s651.png OR scr001
            sort_key = item.stem

        file = Files(item, sort_key)
        files.append(file)

    files.sort(key=lambda f: f[1])


def process(rename, number, files):
    """ Rename files with parameters """
    i = 0
    for file in files:
        num = f" {number:03}"
        extension = file.path.suffix
        new_filename = rename + num + extension

        print(f"{i}: RENAME {file.path.name} TO {new_filename}")
        file.path.rename(
            pathlib.Path(file.path.parent, new_filename)
        )
        time.sleep(0.1)
        number += 1
        i += 1


if __name__ == "__main__":
    main()
