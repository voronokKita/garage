#! python3
""" Bruteforce the password for the pdf file. """
import sys
import PyPDF2
import datetime

start_time = datetime.datetime.now()
pdf = PyPDF2.PdfFileReader(
    open("encryptedminutes.pdf", 'rb')
)

if pdf.isEncrypted:
    words = []
    with open('dictionary.txt') as dictfile:
        words += [word.strip() for word in dictfile.readlines()]
        words += [word.lower() for word in words]
    print("Dictionary loaded at", datetime.datetime.now() - start_time)

    print("Bruteforce initiated...")
    password = None
    for word in words:
        if pdf.decrypt(word):
            password = word
            break

    if password:
        print("Word match:", password)
    else:
        print("None of words has match password.")

print("Time of execution is", datetime.datetime.now() - start_time)
sys.exit(0)
