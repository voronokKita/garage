#!python3
""" My implementation of Tic-tac-toe game,
    with artificial intelligence!) """
import sys
import random

FIELDS = {
    'top-l': " ", 'top-m': " ", 'top-r': " ",
    'mid-l': " ", 'mid-m': " ", 'mid-r': " ",
    'low-l': " ", 'low-m': " ", 'low-r': " "
}
BOARD = """*********************
     L   M   R
top  {0} | {1} | {2}
    ---+---+---
mid  {3} | {4} | {5}
    ---+---+---
low  {6} | {7} | {8}"""


def showBoard():
    print(BOARD.format(
        FIELDS['top-l'], FIELDS['top-m'], FIELDS['top-r'],
        FIELDS['mid-l'], FIELDS['mid-m'], FIELDS['mid-r'],
        FIELDS['low-l'], FIELDS['low-m'], FIELDS['low-r']
    ))


def winnerCheck(turn):
    top = FIELDS['top-l'] + FIELDS['top-m'] + FIELDS['top-r']
    mid = FIELDS['mid-l'] + FIELDS['mid-m'] + FIELDS['mid-r']
    low = FIELDS['low-l'] + FIELDS['low-m'] + FIELDS['low-r']
    l = FIELDS['top-l'] + FIELDS['mid-l'] + FIELDS['low-l']
    m = FIELDS['top-m'] + FIELDS['mid-m'] + FIELDS['low-m']
    r = FIELDS['top-r'] + FIELDS['mid-r'] + FIELDS['low-r']
    slash = FIELDS['low-l'] + FIELDS['mid-m'] + FIELDS['top-r']
    backslash = FIELDS['top-l'] + FIELDS['mid-m'] + FIELDS['low-r']

    variants = [top, mid, low, l, m, r, slash, backslash]    
    
    pattern = turn * 3    
    winner = None
    for variant in variants:
        if variant == pattern:
            winner = turn
            break
    return winner


showBoard()
print("To play Tic Tac Toe simply input empty field key, like 'mid-l' or 'low-m';")

player = ""
while not player:
    answer = input("Choose your side [X or O]: ").upper()
    player = answer if answer in "XO" else ""
ai = "X" if player == "O" else "O"

random.seed()
turn = 'X'
winner = None
while True:
    empty_fields = [field for field in FIELDS if FIELDS[field] == " "]
    if not empty_fields:
        winner = "TIE!"
        showBoard()
        break
    
    if turn == ai:
        key = random.choice(empty_fields)
        FIELDS[key] = ai
        showBoard()

    elif turn == player:
        while True:
            key = input(f"Where to hit {player}? ").lower()
            if key in empty_fields:
                break
        FIELDS[key] = player

    winner = winnerCheck(turn)
    if winner:
        showBoard()
        break

    turn = 'O' if turn == 'X' else 'X'

print(f"{winner} has won!") if winner != "TIE!" else print(winner)
sys.exit(0)
