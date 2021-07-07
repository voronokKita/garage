#! python3
""" Replace time patterns in the text. """
import re

text = """Dear! If you don’t return your suitcase by 09:00, then at 09:00:01 I’m not responsible for myself!
PS. With a ratio of 25:50, everything is fine!"""

dateRegex = re.compile(r'[0-2][0-9](?::[0-5][0-9]){1,2}')
result = dateRegex.sub("TBD", text, count=2)
print(result)
