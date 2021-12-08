#! python3
""" spring 2021 """
import random

GRID = [
    ['.', '.', '.', '.', 'o', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'o', 'o', '.', '.', '.'],
    ['.', '.', '.', '.', '.', 'o', 'o', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'o', 'o', '.'],
    ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
    ['.', '.', '.', '.', '.', '.', 'o', 'o', '.'],
    ['.', '.', '.', '.', '.', 'o', 'o', '.', '.'],
    ['.', '.', '.', '.', 'o', 'o', '.', '.', '.'],
    ['.', '.', '.', '.', 'o', '.', '.', '.', '.']
        ]
ARROWS = ['left', 'right', 'up', 'down']

answer = input("Where to point arrow? [left, right, up, down]:\n").lower()
if answer not in ARROWS:
    random.seed()
    answer = random.choice(ARROWS)

if answer == 'right':
    for line in GRID:
        print("".join(line))
elif answer == 'left':
    for line in GRID:
        print("".join(line[::-1]))
elif answer == 'down':
    for i in range(len(GRID)):
        for line in GRID:
            print(line[i], end='')
        print()
else:
    i = -1
    end = len(GRID) * -1
    while i >= end:
        for line in GRID:
            print(line[i], end='')
        print()
        i -= 1
