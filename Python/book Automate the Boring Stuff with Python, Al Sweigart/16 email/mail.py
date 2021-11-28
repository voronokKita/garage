#! python3
""" Mailing from terminal. """
import sys
import smtplib

USAGE = f"USAGE: python3 {sys.argv[0]} account password"

if len(sys.argv) != 3:
    print(USAGE)
    sys.exit(0)
else:
    account = sys.argv[1]
    password = sys.argv[2]

connection = smtplib.SMTP('smtp.gmail.com', 587)
try:
    hello = connection.ehlo()
    print("Hello;", *hello)
    assert hello[0] == 250, "1 hello fail."

    tls = connection.starttls()
    print("TLS;", *tls)
    assert tls[0] == 220, "2 encryption fail."

    authentication = connection.login(account, password)
    print("Login;", *authentication)
    assert authentication[0] == 235, "3 login fail."

    address = input("Enter addressee: ")
    text = input("Enter mail text: ").encode('utf-8')

    result = connection.sendmail(account, address, text)
    if len(result) > 0:
        print("Fail to send mail to this address:", *result)
    else:
        print("Email sent successfully.")
except AssertionError as error:
    print("ERROR", error)
    sys.exit(1)
except Exception as alert:
    print("ALERT", alert)
    sys.exit(1)
else:
    print("Done.")
finally:
    end = connection.quit()
    print("Connection quit.", *end)

sys.exit(0)
