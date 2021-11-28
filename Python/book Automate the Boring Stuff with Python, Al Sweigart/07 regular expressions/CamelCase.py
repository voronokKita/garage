#! python3
""" CamelCase -> under_score """
import re

code = """MyVar17 = OtherVar + YetAnother2Var 
TheAnswerToLifeTheUniverseAndEverything = 42"""

def replace(match):
    parts = re.findall(r'([A-Z0-9][a-z]+|[0-9]+)', match[0])
    return "_".join(parts).lower()

code = re.sub(r'[A-Z]\w*', replace, code)
print(code)
