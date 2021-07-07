#! python3
""" Input user argument digits and
    print them like a big numeric symbols. """
import sys

Zero = ["  ***  ",
        " *   * ",
        "*     *",
        "*     *",
        "*     *",
        " *   * ",
        "  ***  "]
One = [" * ",
       "** ",
       " * ",
       " * ",
       " * ",
       " * ",
       "***"]
Two = [" *** ",
       "*   *",
       "*   *",
       "   * ",
       "  *  ",
       " *   ",
       "*****"]
Three = [" **** ",
         "*    *",
         "     *",
         "  *** ",
         "     *",
         "*    *",
         " **** "]
Four = ["   *  ",
        "  **  ",
        " * *  ",
        "*  *  ",
        "******",
        "   *  ",
        "   *  "]
Five = ["*******",
        "*      ",
        "* ***  ",
        "*    * ",
        "      *",
        "*    * ",
        " ****  "]
Six = ["    *",
       "   * ",
       "  *  ",
       " **  ",
       "*   *",
       "*   *",
       " *** "]
Seven = ["*****",
         "    *",
         "   * ",
         "  *  ",
         " *   ",
         "*    ",
         "*    "]
Eight = [" *** ",
         "*   *",
         "*   *",
         " *** ",
         "*   *",
         "*   *",
         " *** "]
Nine = [" *** ",
        "*   *",
        "*   *",
        "  ** ",
        "  *  ",
        " *   ",
        "*    "]
DIGITS = [Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine]
DIGITS_HIGHT = 7

try:
    argument_digits = sys.argv[1]

    y = 0
    while y < DIGITS_HIGHT:
        output_line = ""
        x = 0
        while x < len(argument_digits):
            number = int(argument_digits[x])
            digit = DIGITS[number]
            for c in digit[y]:
                output_line += str(number) if c == "*" else " "
            output_line += "   "
            x += 1
        print(output_line)
        y += 1
except IndexError:
    print(f"usage: {sys.argv[0]} <number>")
    sys.exit(1)
except ValueError as err:
    print(err, "in", sys.argv[1])
    sys.exit(2)

sys.exit(0)
