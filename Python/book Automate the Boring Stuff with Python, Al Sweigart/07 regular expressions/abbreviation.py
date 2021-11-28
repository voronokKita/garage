#! python3
""" Output abbreviations in text.
    Output abbreviation of all text words. """
import re
text = """This course of informatics corresponds to the FSES and ABEP,
this is confirmed by FGU FNTS NIISI RAS."""

for result in re.finditer(r'[A-Z]{2,}(?:\s[A-Z]{2,})*', text):
    print(result.group())

print("".join(re.findall(r'\b\w', text)).upper())
