#! python3
""" summer 2020 Print awful poems. Argument == num of lines integer. """
import sys
import random


articles = ['the', 'a', 'her', 'his', 'another']
nouns = ['cat', 'dog', 'man', 'woman', 'boy', 'girl']
verbs = ['sang', 'ran', 'jumped', 'heard', 'hoped']
adverbs = ['loudly', 'quietly', 'well', 'badly', 'politely', 'slowly']
MIN = 1
MAX = 10
DEFAULT = 5

try:
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
        if num > MAX:
            num_of_lines = MAX
        elif num < MIN:
            num_of_lines = MIN
        else:
            num_of_lines = num
    else:
        num_of_lines = DEFAULT
except ValueError:
    num_of_lines = DEFAULT

random.seed()

for i in range(num_of_lines):
    line = f"{random.choice(articles)} {random.choice(nouns)} {random.choice(verbs)}"
    coin = random.randint(0, 1)
    if coin == 1:
        line += " " + random.choice(adverbs)
    print(line)

sys.exit(0)
