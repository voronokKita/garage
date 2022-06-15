#! python3

def get_str(message="", field="input", default=None, minimum=0, maximum=None, empty=True):
    """
    :param message: str, to print
    :param field: str, to print errors
    :param default: str, if empty input
    :param minimum: uint, length
    :param maximum: uint, length
    :param empty: bool, allow empty input
    :return: str (or default, or empty)
    """
    while True:
        try:
            line = input(message)

            if not line:
                if default is not None:
                    return default
                if empty is True:
                    return ""
                else:
                    raise ValueError(f"{field} may not be empty")

            if len(line) < minimum:
                raise ValueError(f"{field} must have at least {minimum} characters")
            if maximum is not None and len(line) > maximum:
                raise ValueError(f"{field} must have at most {maximum} characters")

            return line

        except ValueError as err:
            print("ERROR:", err)


if __name__ == "__main__":
    pass
