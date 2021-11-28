#! python3
""" Search files for keyword-argument and print words with key. """
import sys

if len(sys.argv) < 3:
    print(f"USAGE: {sys.argv[0]} keyword 1.txt [2.txt ... N.txt]")
    sys.exit(1)

word = sys.argv[1]
for filename in sys.argv[2:]:
    for row, line in enumerate(open(filename), start=1):
        if word in line:
            print(f"{filename}:row {row}:{line.rstrip():.40}")
sys.exit(0)
