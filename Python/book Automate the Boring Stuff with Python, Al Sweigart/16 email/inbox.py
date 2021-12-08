#! python3
""" spring 2021
Establishes an imap connection to gmail and
allows to select a folder, enter arguments and
read the text from emails. """
import sys
import pyzmail
import imaplib
import imapclient
from pprint import pprint

USAGE = f"USAGE: python3 {sys.argv[0]} account password"

if len(sys.argv) != 3:
    print(USAGE)
    sys.exit(0)
else:
    account = sys.argv[1]
    password = sys.argv[2]

imaplib.MAXLINE = 10000000
connection = imapclient.IMAPClient('imap.gmail.com', ssl=True)
try:
    authentication = connection.login(account, password)
    print(authentication)

    folders = connection.list_folders()
    pprint(folders)

    folder = input("Select folder: ")
    connection.select_folder(folder, readonly=True)

    keys = input("Input arguments separated by comma: ")
    keys = [k.strip() for k in keys.split(",")]
    content = connection.search(keys)
    print(len(content), "UID's found;")

    raw_messages = connection.fetch(content, ['BODY[]'])
except Exception as error:
    print("ERROR.", error)
    sys.exit(1)
else:
    print("Loading complete.")
finally:
    end = connection.logout()
    print("Logout.", *end)

# convert raw messages
messages = []
for key in raw_messages:
    raw_message = raw_messages[key][b'BODY[]']
    message = pyzmail.PyzMessage.factory(raw_message)
    messages.append(message)

for message in messages:
    print("TO", *message.get_addresses('to'), " | ", "FROM", *message.get_addresses('from'))
    if message.text_part is not None:
        byte_text = message.text_part.get_payload()
        encode = message.text_part.charset if message.text_part.charset is not None else 'utf-8'
        print(byte_text.decode(encode), end="\n************\n")
    elif message.html_part is not None:
        byte_text = message.html_part.get_payload()
        encode = message.html_part.charset if message.text_part.charset is not None else 'utf-8'
        print(byte_text.decode(encode), end="\n************\n")
    else:
        print("Text == None", end="\n************\n")

sys.exit(0)
