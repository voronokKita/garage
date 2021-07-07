#! python3
""" Distinguishes strong and weak passwords with re;
    "strong" password's consists of at least 8 letters +
    contains upper and lower case letters +
    contains at least one digit. """
import re

line = ""
while not line:
    line = input("Enter password to check. ")

lower = len(re.findall(r'([a-z])', line))
upper = len(re.findall(r'([A-Z])', line))
chars = lower + upper
digits = len(re.findall(r'([0-9])', line))

if chars >= 8 and lower >= 1 and upper >= 1 and digits >= 1:
    print("Password is OK.")
else:
    print("Password is weak.")
