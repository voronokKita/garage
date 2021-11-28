#! python3
""" My implementation of simple password manager; 
    with lot of exceptions. """
import os
import sys
import csv
import pyperclip
from getpass import getpass
from base64 import b64encode, b64decode

USAGE = f"Usage: python3 {sys.argv[0]} to enter new account data into csv;\n"\
        f"OR python3 {sys.argv[0]} [site name] to see associated account name " \
        f"and receive password in to clipboard;"

# trying to connect to a datafile,
# better to use pathlib onward;
CSV = os.path.dirname(os.path.realpath(sys.argv[0]))
CSV += "\\" if sys.platform.startswith("win") else "/"
CSV += "data.csv"
if not os.path.exists(CSV):
    try:
        with open(CSV, 'w') as datafile:
            header = ['site', 'account', 'password']
            csv.writer(datafile).writerow(header)
    except OSError as err:
        print("ERROR 1", err)
        sys.exit(1)


if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"] or len(sys.argv) > 2:
    print(USAGE)
    sys.exit(0)


# if script is run without an argument;
elif len(sys.argv) == 1:
    site = ""
    while len(site) < 2:
        site = input(r"Enter site name: ")
    
    # check datafile;
    try:
        with open(CSV, 'r') as datafile:
            reader = csv.DictReader(datafile)
            for row in reader:
                if row['site'] == site:
                    print(f"Site {site} found in datafile; aborted.")
                    sys.exit(2)
    except OSError as err:
        print("ERROR 2", err)
        sys.exit(2)
    
    account = None
    while not account:
        account = b64encode(
            getpass("Enter account name: ").encode('UTF-8')
        )

    password = None
    while not password:
        password = b64encode(
            getpass("Enter account password: ").encode('UTF-8')
        )
    
    # save to csv;
    try:
        with open(CSV, 'a') as datafile:        
            csv.writer(datafile).writerow(
                [site, account.decode('UTF-8'), password.decode('UTF-8')]
            )
    except OSError as err:
        print("ERROR 3", err)
        sys.exit(3)
    
    print("Data encrypted and stored.")
    sys.exit(0)


# if script is run with an argument;
elif len(sys.argv) == 2:
    site = sys.argv[1]
    account = ""
    password = ""   
    found = False
    datafile = open(CSV, 'r')
    try:
        reader = csv.DictReader(datafile)
        for row in reader:
            if row['site'] == site:
                found = True
                account = row['account']
                password = row['password']
                break
    except OSError as err:
        print(f"ERROR 4", err)
        sys.exit(4)
    else:
        if not found:
            print(f"No site with name {site} presented in datafile.")
            sys.exit(4)
    finally:
        datafile.close()
        
    print(f"Account name is {b64decode(account).decode('UTF-8')}")
    
    try:
        pyperclip.copy(
            b64decode(password).decode('UTF-8')
        )
    except OSError as err:
        print("ERROR 5", err)
        sys.exit(5)
        
    print("The password was copied into the clipboard successfully.")
    sys.exit(0)
