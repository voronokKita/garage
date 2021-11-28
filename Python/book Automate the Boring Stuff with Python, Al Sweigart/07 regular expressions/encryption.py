#! python3
""" Replace each number with its cube. """
import re

text = "12 units of equipment were purchased at 410.37 rubles."

def replace(match):
    num = float(match[0]) if "." in match[0] else int(match[0])
    return str(num * num * num)

result = re.sub(r'\b\d+(\.\d+)?\b', replace, text)
print(result)
