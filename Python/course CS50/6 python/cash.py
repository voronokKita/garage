#! python3
""" CS50 PSet 6: Cash
    Calculates the minimum number of coins required to give a user change. """

answer = 0.0
while answer <= 0:
    try:
        answer = float(input("Change owed: "))
    except ValueError:
        continue

change = round(answer * 100)

coins = 0
while change > 0:
    if change // 25 >= 1:
        change -= 25
        coins += 1

    elif change // 10 >= 1:
        change -= 10
        coins += 1

    elif change // 5 >= 1:
        change -= 5
        coins += 1

    else:
        change -= 1
        coins += 1

print(coins)
