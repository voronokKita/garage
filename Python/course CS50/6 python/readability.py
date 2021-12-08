#! python3
""" fall 2020 CS50 PSet 6: Readability
    Computes and rate the approximate text difficulty. """
import string


ALPHABET = string.ascii_letters

line = input("Text: ")

index = 0
if line:
    words = len(line.split())
    letters = sum(c in ALPHABET for c in line)
    sentences = line.count('.') + line.count('!') + line.count('?')

    """Coleman-Liau index = 0.0588 * L - 0.296 * S - 15.8"""
    L = (letters / words) * 100.0
    S = (sentences / words) * 100.0

    index = round(0.0588 * L - 0.296 * S - 15.8)

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print("Grade", index)
