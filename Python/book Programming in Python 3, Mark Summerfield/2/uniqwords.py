#! python3
"""
Analise txt files in commandline,
Print list of words in files and their counts;
Sorted by value.
v3
"""
import sys
import string
import collections

if len(sys.argv) < 2:
    print(f"USAGE: {sys.argv[0]} 1.txt [2.txt ... n.txt]")
    sys.exit(1)

word = ""
words = collections.defaultdict(int)
strip = string.whitespace + string.punctuation + string.digits + "\"\'"

for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            if word.strip(strip):
                words[word] += 1

for word in sorted(words, key=words.get):
    print(f"'{word}' occurs {words[word]} times")

sys.exit(0)
