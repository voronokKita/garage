#! python3
""" CS50 PSet 6: Mario more
    Print two ladders of #hashes. """

height = 0
while height < 1 or height > 8:
    try:
        height = int(input("Height: "))
    except ValueError:
        continue

opening = 2
for layer in range(height):
    bricks = layer + 1
    space = height - bricks
    print(" " * space, "#" * bricks, " " * opening, "#" * bricks, sep='')
