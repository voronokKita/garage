#! python3
""" summer 2020 Read csv and output html table. """
import os
import sys
import stat
import optparse


VERSION = "4"
USAGE = f"USAGE: {sys.argv[0]} (--maxwidth[int] --format[int]) < input.csv > output.html"
DEF_MAX_WIDTH = 100
DEF_FORMAT = 2


def main():
    cell_max_width, numbers_format = process_options()

    # print start
    print("<table border='1'>")

    row_count = 0
    while True:
        try:
            line = input()
            if not line:
                break
            if row_count == 0:
                txt_color = "lightgreen"
            elif row_count % 2:
                txt_color = "white"
            else:
                txt_color = "lightyellow"

            print_line(line, txt_color, cell_max_width, numbers_format)
            row_count += 1

        except EOFError:
            break

    # print end
    print("</table>")
    sys.exit(0)


def process_options():
    """
    Look in argv for maxwidth or format parameters:
    Execute usage help if error, or if find help request,
    Return defaults otherwise.
    v2 with optparse
    v3 with detect terminal
    """
    parser = optparse.OptionParser(version=VERSION, usage=USAGE, description="")
    parser.add_option(
        "-w", "--maxwidth", action='store', type='int', dest='maxwidth',
        help=f"maximum number of characters for string fields [default: {DEF_MAX_WIDTH}]"
    )
    parser.add_option(
        "-f", "--format", action='store', type='int', dest='format',
        help=f"format of numbers [default: .{DEF_FORMAT}f]"
    )
    parser.set_defaults(maxwidth=DEF_MAX_WIDTH, format=DEF_FORMAT)

    # Check for terminal:
    input_mode = os.fstat(
        sys.stdin.fileno()
    ).st_mode
    output_mode = os.fstat(
        sys.stdout.fileno()
    ).st_mode
    if stat.S_ISREG(input_mode) and stat.S_ISREG(output_mode):
        # OK, stdin and stdout is redirected;
        pass
    else:
        # Terminal detected.
        parser.print_help()
        sys.exit(1)

    options, junk = parser.parse_args()
    cell_max_width = options.maxwidth
    numbers_format = options.format
    return cell_max_width, numbers_format


def print_line(line, color, max_width, numformat):
    """
    Input: cvs line
    Output: html table line
    """
    print(f"<tr bgcolor='{color}'>")

    table_fields = extract_fields(line)

    for field in table_fields:
        if not field:
            print("<td></td>")
        else:
            may_number = field.replace(",", ".")
            try:
                x = float(may_number)
                if color == "lightgreen":
                    print(f"<td align='right'>{int(x)}</td>")
                else:
                    x = round(x, numformat) if format else int(round(x))
                    print(f"<td align='right'>{x}</td>")
            except ValueError:
                field = escape_html(field)
                if len(field) <= max_width:
                    print(f"<td>{field}</td>")
                else:
                    print(f"<td>{field[:max_width]} ...</td>")
    print("</tr>")


def extract_fields(line):
    """
    Input: csv line
    Return: list of cells
    """
    table_fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"\'":
            # start of quoted string
            if quote is None:
                quote = c
            # end of quoted string
            elif quote == c:
                quote = None
            # another quote inside quoted string
            else:
                field += c
            continue

        # end of field
        if quote is None and c == ",":
            table_fields.append(field)
            field = ""

        # add character to field
        else:
            field += c

    # add last field to the list
    if field:
        table_fields.append(field)

    return table_fields


def escape_html(text):
    # or xml.sax.saxutils.escape()
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


if __name__ == "__main__":
    main()
