#! python3
""" summer 2020
Scan directory for .list files;
Allow user to create new files;
Allow user to add and dell lines from list files;
Allow to sort lines in order;
Allow to save lines to file.
"""
import sys
import glob


def main():
    saved = True
    name = "a.list"
    list_in_memory = []
    name, saved = list_starter(name, list_in_memory, saved)

    quit_program = False
    while not quit_program:
        output_to_user(name, list_in_memory, saved)
        quit_program, saved = commands(quit_program, name, list_in_memory, saved)

    list_keeper_exit(name, list_in_memory, saved)
    sys.exit(0)


def list_starter(name, list_in_memory, saved):
    """
    Create a list of all files with .lst extension in a directory.
        If no files, prompts the user to create a new one.
    Or, prompts the user to select a file or 0 - create a new one.
        If file selected - scan it's content.
        Fill list_in_memory with lines.
    Put saved flags to False if list is new.
    :return: list name, saved:bool
    """
    files = []
    print("List Keeper scan...")
    files += sorted(glob.glob('*.list', recursive=False))

    # if files not found:
    if len(files) == 0:
        answer = get_string(f"No lists files found. Create new? (y/n)[y]: ", "answer", "yes")
        if answer.lower() in {"y", "yes"}:
            newfile = get_string(f"Enter filename [{name}]: ", "filename", name)
            if not newfile.endswith(".list"):
                newfile += ".list"
            saved = False
            return newfile, saved
        else:
            print("... exiting.")
            sys.exit(0)

    # or found:
    else:
        print("Lists found:")
        for i, file in enumerate(files, start=1):
            print(f"{i}: {file}")

    answer = None
    while answer < 0:
        answer = get_integer("Select number of file to open or type [0] to create new: ",
                             default=0, minimum=0)
        answer = None if answer > len(files) else answer

    # create new file?
    if answer == 0:
        filename = get_string(f"Enter filename[{name}]: ", "filename", name)
        if not filename.endswith(".list"):
            filename += ".list"
        name = filename
        saved = False

    # Open existing file?
    else:
        i = answer - 1
        try:
            name = files[i]
            with open(name) as file:
                list_in_memory += [line.strip() for line in file if line.strip()]

        except IndexError as err:
            print("ERROR:", err)
        except OSError as err:
            print("ERROR:", err)

    return name, saved


def output_to_user(name, list_in_memory, saved):
    """
    Scan list and print to user it's content;
    And print actions that user may take:
    [A]dd [D]elete S[O]rt [S]ave [Q]uit [S]
    """
    output = f"List: {name}"
    if len(list_in_memory) == 0:
        output += "\n«no items are in the list»\n"
    else:
        output += " ({0} item{1})\n".format(
            len(list_in_memory), "s" if len(list_in_memory) > 1 else ""
        )
        for i, ell in enumerate(list_in_memory, start=1):
            output += f"{i}: {ell}\n"

    output += "[A]dd "
    if len(list_in_memory) > 0:
        output += "[D]elete "
        if len(list_in_memory) > 1:
            output += "S[O]rt "
    if saved is False:
        output += "[S]ave "
    output += "[Q]uit "
    output += "[S]: " if saved is False else "[Q]: "

    print(output, end="")


def commands(quit_program, name, list_in_memory, saved):
    """ Interact with user.
        [A]dd [D]elete S[O]rt [S]ave [Q]uit [default]: """
    i = 0
    while True:
        answer = get_string().lower()

        if not answer:
            if saved is False:
                saved = list_writer(name, list_in_memory)
            else:
                quit_program = True

        elif answer in {"a", "ad", "add"}:
            saved = list_renew(list_in_memory, saved)

        elif len(list_in_memory) > 0 and answer in {"d", "dell", "delete"}:
            saved = list_erase(list_in_memory, saved)

        elif len(list_in_memory) > 1 and answer in {"o", "srt", "sort"}:
            saved = list_sort(list_in_memory, saved)

        elif saved is False and answer in {"s", "sv", "save"}:
            saved = list_writer(name, list_in_memory)

        elif answer in {"q", "quit"}:
            quit_program = True

        else:
            if i == 9:
                print("Stop continue.")
                sys.exit(1)
            i += 1
            print("?: ", end="")
            continue
        break

    return quit_program, saved


def list_renew(list_in_memory, saved):
    """ Ask for a new element. Update the list. """
    answer = get_string("Add item: ", "item name")
    if answer:
        list_in_memory.append(answer)
        if saved is True:
            saved = False

    return saved


def list_erase(list_in_memory, saved):
    """ Ask for element number to delete, or 0 (or enter) to cancel. """
    answer = get_integer("Delete item number (or 0 to cancel): ",
                         "item number", default=0, minimum=0)

    if 0 < answer <= len(list_in_memory):
        i = answer - 1
        try:
            list_in_memory.pop(i)
        except IndexError as err:
            print("ERROR:", err)
        if saved is True:
            saved = False

    return saved


def list_sort(list_in_memory, saved):
    answer = get_string("Sort [A]scending or [D]escending: ", "order").lower()
    if answer in {"a", "asc", "ascending"}:
        list_in_memory.sort()
    elif answer in {"d", "desc", "descending"}:
        list_in_memory.sort(reverse=True)
    if saved is True:
        saved = False

    return saved


def list_writer(name, list_in_memory):
    """ Write to file. """
    ell_saved = 0
    try:
        with open(name, 'w') as file:
            for element in list_in_memory:
                print(element, file=file)
                ell_saved += 1
    except OSError as err:
        print("ERROR.", err)

    saved = True
    if len(list_in_memory) > 0:
        print(f"Saved {ell_saved} items to list {name}")
    else:
        print(f"List {name} saved.")
    return saved


def list_keeper_exit(name, list_in_memory, saved):
    """ If there are changes, offer to save before exiting. Write to file. """
    if saved is False:
        answer = get_string(f"Save unsaved changes (y/n)[yes]: ", "answer", "yes").lower()
        if answer in {"y", "yes"}:
            list_writer(name, list_in_memory)


def get_string(message="", name="string", default=None, minimum=0, maximum=None, empty=True):
    """
    :param message: str
    :param name: str ["string"]
    :param default: str [None]
    :param minimum: uint [0]
    :param maximum: uint [None]
    :param empty: bool [True]
    :return: str or ""
    """
    while True:
        try:
            line = input(message)

            if not line:
                if default is not None:
                    return default
                elif empty is True:
                    return ""
                else:
                    raise ValueError(f"{name} may not be empty")

            if len(line) < minimum:
                raise ValueError(f"{name} must have at least {minimum} characters")
            if maximum is not None and len(line) > maximum:
                raise ValueError(f"{name} must have at most {maximum} characters")

            return line

        except ValueError as err:
            print("ERROR:", err)


def get_integer(message="", name="integer", default=None, minimum=None,
                maximum=None, allow_zero=True, empty=False):
    """
    :param message: str
    :param name: str ["integer"]
    :param default: int [None]
    :param minimum: int [None]
    :param maximum: int [None]
    :param allow_zero: bool [True]
    :param empty: bool [False]
    :return: int
    """
    while True:
        try:
            answer = input(message)

            if not answer:
                if default is not None:
                    return default
                elif empty is True:
                    return None
                else:
                    raise ValueError(f"{name} may not be empty")

            answer = int(answer)

            if answer == 0 and allow_zero is False:
                raise ValueError(f"{name} may not be zero")

            if minimum is not None and answer < minimum:
                raise ValueError(f"{name} must have at least {minimum} value")
            elif maximum is not None and answer > maximum:
                raise ValueError(f"{name} must have at most {maximum} value")

            return answer

        except ValueError as err:
            print("ERROR:", err)


if __name__ == '__main__':
    main()
