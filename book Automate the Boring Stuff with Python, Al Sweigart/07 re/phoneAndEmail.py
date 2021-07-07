#! python3
""" My implementation of phones and emails search script;
    search for re in clipboard."""
import re
import sys
import pyperclip

COUNTRY = "+1"

# 0 regular expressions;
phoneRegex = re.compile(r'''(
    (\d\d\d|\(\d\d\d\))?            # code?
    (\s|-|\.)?                      # sep?
    (\d\d\d)                        # number digits
    (\s|-|\.)                       # sep
    (\d\d\d\d)                      # number digits
    (\s*(ext|x|ext.)\s*(\d{2,5}))?  # addition?
    )''', re.VERBOSE)
    
mailRegex = re.compile(r'''(
    [\w._%+-]+              # name
    @                       # doge
    [\w.-]+                 # domain
    \.\w{2,4}               # end
    )''', re.VERBOSE)

try:
    # input text from a buffer;
    text = pyperclip.paste()

    # search for phones and mails;
    result_phones = phoneRegex.findall(text)
    found_mails = mailRegex.findall(text)

    # preprocess;
    print("Found phones:") if len(result_phones) > 0 else print("Phones not found.")
    found_phones = []
    for phone in result_phones:
        code = phone[1] if phone[1] != "" else "none"
        ext = f" ext.{phone[8]}" if phone[8] != "" else ""
        number = f"{COUNTRY} {code} {phone[3]}-{phone[5]}{ext}"
        found_phones.append(number)
        print("\t", number)

    print("Found mails:") if len(found_mails) > 0 else print("Mails not found.")
    for mail in found_mails:
        print("\t", mail)

    # output;
    output = found_phones + found_mails
    if len(output) > 0:
        pyperclip.copy("\n".join(output))
        print("Copied to clipboard.")

except OSError as err:
    print("ERROR.", err)
    sys.exit(1)

# Done.
sys.exit(0)
