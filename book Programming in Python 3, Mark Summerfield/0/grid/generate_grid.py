#! python3
""" Ask for number of rows and columns, min and max numbers;
    print grid of random numbers between min and max. """
import random

MIN_RC = 1
NUM_MINIMUM = -1000000
COLUMN_LEN = 10


def main():
    # Get table scale;
    rows = get_int(f"rows[{MIN_RC}]: ", MIN_RC, None)
    columns = get_int(f"columns[{MIN_RC}]: ", MIN_RC, None)

    # Get numbers range;
    default_minimum = 0
    minimum = get_int("minimum (or Enter for 0): ", NUM_MINIMUM, default_minimum)

    default_maximum = 1000 if minimum < 1000 else minimum * 2
    maximum = get_int(f"maximum (or Enter for {str(default_maximum)}): ",
                      minimum, default_maximum)

    # Output to user.
    generate_grid(rows, columns, minimum, maximum)
    exit(0)


def get_int(msg, minimum, default):
    """
    :param msg: str
    :param minimum: uint
    :param default: uint or None
    :return: uint
    """
    while True:
        try:
            line = input(msg)
            if not line and default is not None:
                return default

            num = int(line)
            if num < minimum:
                print("must be >=", minimum)
            else:
                return num
        except ValueError as err:
            print(err)


def generate_grid(rows, columns, minimum, maximum):
    """
    :param rows: int >= 1
    :param columns: int >= 1
    :param minimum: int
    :param maximum: int
    :return: print random numbers grid
    """
    random.seed()
    row = 0
    while row < rows:
        line = ""
        column = 0
        while column < columns:
            num = str(random.randint(minimum, maximum))
            if len(num) < COLUMN_LEN:
                num = ' ' * (COLUMN_LEN - len(num)) + num
            elif len(num) >= COLUMN_LEN:
                num = ' ' + num[0:COLUMN_LEN-1]
            line += num
            column += 1
        print(line)
        row += 1


if __name__ == "__main__":
    main()
