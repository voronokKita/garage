#! python3
""" Download book. """
import sys
import requests

answer = requests.get("https://www.gutenberg.org/cache/epub/1777/pg1777.txt")

answer.raise_for_status()

if answer.status_code == requests.codes.ok:
    with open("RaJ.txt", 'wb') as  File:
        for chunk in answer.iter_content(100000):
            status = File.write(chunk)
            print(status)

sys.exit(0)
