#! python3

def get_int(message="", field="input", default=None, minimum=None, maximum=None, empty=False):
    """
    :param message: str, to print
    :param field: str, to print errors
    :param default: int, if empty input
    :param minimum: int
    :param maximum: int
    :param empty: bool, allow empty input
    :return: int (or default, or empty)
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
                    raise ValueError(f"{field} may not be empty")

            answer = int(answer)

            if minimum is not None and answer < minimum:
                raise ValueError(f"{field} must have at least {minimum} value")
            elif maximum is not None and answer > maximum:
                raise ValueError(f"{field} must have at most {maximum} value")

            return answer

        except ValueError as err:
            print("ERROR:", err)


if __name__ == "__main__":
    pass
