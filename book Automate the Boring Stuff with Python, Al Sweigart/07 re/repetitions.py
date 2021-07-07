#! python3
""" Removing word repetitions. """
import re

text = "A fairly common mistake mistake is unnecessary repetition repetition of a word word. " \
       "Funny, isn't it it? There is no need to spoil the chorus round and round dance."

text = re.sub(r'(\b\w+\b)(\s*)(?=\1)', "", text)
print(text)
