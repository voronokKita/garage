#! python3
""" CS50 PSet 6: Credit
    Determines whether a provided credit card number is valid
    according to Luhn’s algorithm. """

MIN = 4000000000000
MAX = 5600000000000000

AMEX_HEADERS = [34, 37]
MACA_HEADERS = [51, 52, 53, 54, 55, 22]
VISA_HEADER = 4

number = None
while not number:
    try:
        number = int(input("Number: "))
    except ValueError:
        continue

# Checking number length and leading digits;
brand = 0
if MIN <= number < MAX:
    s = str(number)
    nu = int(s[:2])

    if nu in AMEX_HEADERS or nu in MACA_HEADERS:
        brand = nu
    else:
        n = int(s[:1])
        if n == VISA_HEADER:
            brand = n

# Run Luhn's test if card is probably valid;
luhn_result = False
if brand > 0:
    """ Luhn’s Algorithm:
    1) Multiply every second-from-last digit by 2,
        sum together products digits of each multiplying.
    2) Add the sum to the sum of the digits that weren’t multiplied by 2.
    3) If the total’s last digit is 0 the number is valid! """
    seconds_sum = 0
    others_sum = 0
    tmp = 0

    # Reverse number
    number = str(number)
    number = number[::-1]

    for digit in range(1, len(number), 2):
        tmp = int(number[digit]) * 2
        if tmp >= 10:
            seconds_sum += tmp % 10
            tmp //= 10
        seconds_sum += tmp

    for digit in range(0, len(number), 2):
        others_sum += int(number[digit])

    luhn_result = True if (seconds_sum + others_sum) % 10 == 0 else False

# Output results.
if brand <= 0 or luhn_result is False:
    print("INVALID")
elif brand in AMEX_HEADERS:
    print("AMEX")
elif brand in MACA_HEADERS:
    print("MASTERCARD")
elif brand == VISA_HEADER:
    print("VISA")
