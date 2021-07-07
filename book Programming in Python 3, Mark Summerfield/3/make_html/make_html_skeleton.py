#! python3
"""
Make HTML Skeleton v2;

Enter your name (for copyright): Harold Pinter
Enter copyright year [2008]: 2009
Enter filename: career-synopsis
Enter title: Career Synopsis
Enter description (optional): synopsis of the career of Harold Pinter
Enter a keyword (optional): playwright
Enter a keyword (optional): actor
Enter a keyword (optional): activist
Enter a keyword (optional):
Enter the stylesheet filename (optional): style
Saved skeleton career-synopsis.html
Create another (y/n)? [n]: y
Make HTML Skeleton
Enter your name (for copyright) [Harold Pinter]:
Enter copyright year [2009]:
Enter filename:
Cancelled
Create another (y/n)? [n]: n
"""
import sys
import datetime
import xml.sax.saxutils

COPYRIGHT_TEMPLATE = "Copyright (c) {0} {1}. All rights reserved."
STYLESHEET_TEMPLATE = '<link rel="stylesheet" type="text/css" media="all" href="{0}" />\n'

HTML_TEMPLATE = """<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" \
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
    <title>{title}</title>
    <!-- {copyright} -->
    <meta name="Description" content="{description}" />
    <meta name="Keywords" content="{keywords}" />
    <meta equiv="content-type" content="text/html; charset=utf-8" />
    {stylesheet}\
</head>
<body>

</body>
</html>
"""

class CancelledError(Exception):
    pass


def main():
    information = dict(
        name=None, year=None, filename=None, title=None,
        description=None, keywords=None, stylesheet=None
    )
    while True:
        try:
            print("\nMake HTML Skeleton")
            populate_information(information)
            make_html_skeleton(**information)
        except CancelledError:
            print("Cancelled")

        another = get_string("Create another (y/n)?", default="n").lower()
        if another not in {"y", "yes"}:
            break

    sys.exit(0)


def populate_information(information):
    name = get_string("Enter your name (for copyright)", "name", information["name"])
    if not name:
        raise CancelledError()

    year = get_integer("Enter copyright year", "year", information["year"],
                       2000, datetime.date.today().year + 1, False)
    if not year:
        raise CancelledError()

    filename = get_string("Enter filename", "filename")
    if not filename:
        raise CancelledError()

    if not filename.endswith((".htm", ".html")):
        filename += ".html"

    title = get_string("Enter title", "title")
    if not title:
        raise CancelledError()

    description = get_string("Enter description (optional)")

    keywords = []
    while True:
        key = get_string("Enter a keyword (optional)")
        if key:
            keywords.append(key)
        else:
            break

    stylesheet = get_string("Enter the stylesheet filename (optional)")

    information.update(name=name, year=year, filename=filename,
                       title=title, description=description,
                       keywords=keywords, stylesheet=stylesheet)


def make_html_skeleton(year, name, title, description, keywords, stylesheet, filename):
    c = COPYRIGHT_TEMPLATE.format(year, xml.sax.saxutils.escape(name))
    t = xml.sax.saxutils.escape(title)
    desc = xml.sax.saxutils.escape(description)
    keys = ", ".join([xml.sax.saxutils.escape(k) for k in keywords]) if keywords else ""
    style = (STYLESHEET_TEMPLATE.format(stylesheet) if stylesheet else "")
    html = HTML_TEMPLATE.format(
        title=t, copyright=c, description=desc, keywords=keys, stylesheet=style
    )
    writer = None
    try:
        writer = open(filename, 'w', encoding='utf8')
        writer.write(html)
    except EnvironmentError as err:
        print("ERROR:", err)
        exit(1)
    else:
        print("Saved skeleton", filename)
    finally:
        if writer is not None:
            writer.close()


def get_string(message, name="string", default=None, minimum=0, maximum=None, empty=True):
    """
    :param message: str
    :param name: str ["string"]
    :param default: str [None]
    :param minimum: uint [0]
    :param maximum: uint [None]
    :param empty: bool [True]
    :return: str or ""
    """
    message += ": " if default is None else f" [{default}]: "

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


def get_integer(message, name="integer", default=None, minimum=None,
                maximum=None, allow_zero=True, empty=True):
    """
    :param message: str
    :param name: str ["integer"]
    :param default: int [None]
    :param minimum: int [None]
    :param maximum: int [None]
    :param allow_zero: bool [True]
    :param empty: bool [True]
    :return: int
    """
    message += ": " if default is None else f" [{default}]: "

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
