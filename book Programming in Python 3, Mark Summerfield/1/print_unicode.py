#! python3
""" Print unicode table by keyword. v2 """
import sys
import unicodedata
import time


def main():
    word = None
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print("USAGE: {script} unicode-keyword".format(script=sys.argv[0]))
            sys.exit(0)

        word = sys.argv[1].lower()

    print_unicode_table(word)
    sys.exit(0)


def print_unicode_table(word):
    print(f"decimal  hex  chr {'name':^40}")
    print(f"------- ----- --- {'-' * 40}")

    code = ord(" ")
    end = sys.maxunicode

    while code < end:
        c = chr(code)
        name = unicodedata.name(c, "*** unknown ***").title()
        if word is None or word in name.lower():
            print(f"{code:7} {code:5X} {code:^3c} {name}")
        code += 1
        time.sleep(0.1)


if __name__ == "__main__":
    main()
