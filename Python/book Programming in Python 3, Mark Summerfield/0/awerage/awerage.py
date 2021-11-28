#! python3
""" Average v2 with median. """
import sys
numbers = []
count = 0
sum = 0
lowest = None
highest = None
median = 0.0

while True:
    try:
        answer = input("enter a number or [Enter] to finish: ")
        if answer:
            number = int(answer)
            count += 1
            sum += number
            numbers.append(number)

            if lowest is None:
                lowest = number
            elif number < lowest:
                lowest = number

            if highest is None:
                highest = number
            elif highest < number:
                highest = number
        else:
            break

    except ValueError as err:
        print(err)
        continue
    except EOFError:
        break

if count:
    # Avoid python sorting:
    sorted = []
    while len(numbers) > 0:
        x = highest + 1
        for num in numbers:
            if num < x:
                x = num
        num = numbers.pop(
            numbers.index(x)
        )
        sorted.append(num)

    # Median
    length = len(sorted)
    if length == 1:
        median = float(sorted[0])
    elif length % 2 == 0:
        i = length // 2
        median = (sorted[i - 1] + sorted[i]) / 2
    else:
        i = (length - 1) // 2
        median = float(sorted[i])

    # Output to user.
    print(sorted)
    print(f"count = {count} sum = {sum} lowest = {lowest} "
          f"highest = {highest} median = {median} mean = {sum / count}")

sys.exit(0)
