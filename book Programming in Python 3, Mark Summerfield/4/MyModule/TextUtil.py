#! python3
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
"""
This module provides several string manipulation functions.

>>> shorten("The Crossing", 10)
'The Cro...'
>>> simplify(" some text with spurious whitespace ")
'some text with spurious whitespace'
>>> is_balanced("(Python (is (not (lisp))))")
True
"""
import string


def shorten(text, length=25, end="..."):
    """
    Returns text or a shorten copy of it, with [indicator] appended at the end.
    :param text: str
    :param length: max length of string + indicator
    :param end: appended at the end of the shorten line
    :return: str

    >>> shorten("The Road")
    'The Road'
    >>> shorten("No Country for Old Men", 20)
    'No Country for Ol...'
    >>> shorten("Cities of the Plain", 15, "*")
    'Cities of the *'
    """
    if len(text) > length:
        slice = length - len(end)
        text = text[:slice] + end
    return text


def simplify(text, whitespace=string.whitespace, delete=""):
    r"""
    Returns the text from which extra spaces have been removed.
    :param text: str
    :param whitespace: characters each of which counts as a space character
    :param delete: additional characters to remove from string
    :return: str

    >>> simplify(" this and\n that\t too")
    'this and that too'
    >>> simplify(" Washington D.C.\n")
    'Washington D.C.'
    >>> simplify(" Washington D.C.\n", delete=",;:.")
    'Washington DC'
    >>> simplify(" disemvoweled ", delete="aeiou")
    'dsmvwld'
    """
    result = []
    word = ""
    for char in text:
        if char in delete:
            continue
        elif char in whitespace:
            if word:
                result.append(word)
                word = ""
        else:
            word += char
    if word:
        result.append(word)

    return " ".join(result)


def is_balanced(text, brackets="()[]{}<>"):
    """
    Checks that the parentheses are closed.
    :param text: str
    :param brackets: characters that count as brackets
    :return: bool

    >>> is_balanced("(don't closed brackets")
    False
    >>> is_balanced("don't open brackets}")
    False
    >>> is_balanced("[different brackets>")
    False
    >>> is_balanced("(closed [closed {closed <closed brackets> brackets} brackets] brackets)")
    True
    """
    counts = {}
    left_for_right = {}
    for left, right in zip(brackets[::2], brackets[1::2]):
        assert left != right, "the bracket characters must differ"
        counts[left] = 0
        left_for_right[right] = left
    for c in text:
        if c in counts:
            counts[c] += 1
        elif c in left_for_right:
            left = left_for_right[c]
            if counts[left] == 0:
                return False
            counts[left] -= 1

    return not any(counts.values())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
