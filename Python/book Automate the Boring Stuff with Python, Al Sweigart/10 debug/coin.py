#! python3
""" spring 2021
Flips a coin 10 times, offers to guess the results;
logs the flow of execution. """
import sys
import random
import logging

logging.basicConfig(filename="log.txt", level=logging.DEBUG,
                    format=" %(asctime)s - %(levelname)s - %(message)s")

logging.debug("Start of the execution:")
random.seed()
for coin in range(10):
    result = random.choices(['heads', 'tails', 'edge'], weights=[0.49, 0.49, 0.02])
    result = result[0]
    answer = input(f"Throw {coin + 1}! Heads or tails? ").lower()

    logging.debug(f"iteration {coin}, result == '{result}', answer == '{answer}';")

    if answer == result and result != 'edge':
        print("Correct!")
    elif answer == result and result == 'edge':
        print("You are incredibly lucky!")
    elif answer != result and result != 'edge':
        print("Incorrect!")
    else:
        print("Incorrect. Wow, a coin fell on its edge!")

logging.debug("End of the execution.")
sys.exit(0)
