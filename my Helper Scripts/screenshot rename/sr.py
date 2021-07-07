#! python3
"""
Rename screenshots and other pictures in script folder.
0) ask parameters
1) look for files in ./
2) rename
"""
import sys
import time
import pathlib
import collections

VERSION = '3'
MODES = ['none', 'vlc', 'numbers']
PICTURES_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tga")
Files = collections.namedtuple("File", "path modified created")


def main():
    # User options;
    rename, number, mode = parameters()

    # List folder and sort;
    files = []
    scan_directory(files, mode)

    # Process files (print to user);
    print("Process:")
    process(rename, number, files)
    
    # Done.
    print("Process successful.")
    sys.exit(0)


def parameters():
    """ Get filenames and start number """
    print(f"Screenshots and pictures rename v{VERSION}")

    filename = ""
    while not filename:
        filename = input("\twhat will be the name of files? ")

    number = None
    while not number:
        try:
            number = int(input("\tcount from where? "))
        except ValueError:
            continue

    m = ", ".join(MODES)
    while True:
        mode = input(f"\tmode[{m}]? ").lower()
        if mode and mode in MODES:
            break

    return filename, number, mode


def scan_directory(files, mode):
    """ Scan directory; fill list of files """

    folder_content = pathlib.Path('./')
    for item in folder_content.iterdir():
        if not item.is_file() or not item.name.endswith(PICTURES_FORMATS):
            continue

        file_modified = None
        file_created = None

        if mode == 'none':
            t = time.localtime(
                item.stat().st_mtime
            )
            file_modified = time.strftime('%Y-%m-%d %H:%M:%S', t)
        elif mode == 'vlc' or mode == 'numbers':
            # LIKE vlcsnap-2021-03-15-21h55m55s651.png OR scr001
            filename = item.stem
            file_created = filename

        file = Files(item, file_modified, file_created)
        files.append(file)

    # Sort:
    if mode == 'vlc' or mode == 'numbers':
        files.sort(key=lambda f: f[2])
    else:
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
