#! python3
""" spring 2021
Saves and loads pieces of text from/to the clipboard. """
import sys
import shelve
import pyperclip

USAGE = f"Usage:\n" \
        f"python3 {sys.argv[0]} save <keyword>   - Saves clipboard to keyword.\n" \
        f"python3 {sys.argv[0]} <keyword>        - Loads keyword to clipboard.\n" \
        f"python3 {sys.argv[0]} list             - Loads all keywords to clipboard.\n" \
        f"python3 {sys.argv[0]} delete <keyword> - Delete keyword from storage.\n" \
        f"python3 {sys.argv[0]} delete           - Cleans up storage."

with shelve.open('mcb') as MCB:

    if len(sys.argv) == 3 and sys.argv[1] == "save":
        key = sys.argv[2]
        MCB[key] = pyperclip.paste()
        print("Saved.")

    elif len(sys.argv) == 2 and sys.argv[1] == "list":
        keys = str(list(MCB.keys()))
        pyperclip.copy(keys)
        print(keys)

    elif len(sys.argv) == 3 and sys.argv[1] == "delete":
        key = sys.argv[2]
        msg = f"{sys.argv[2]} deleted." if MCB.pop(key, "none") != "none" else "Not found."
        print(msg)

    elif len(sys.argv) == 2 and sys.argv[1] == "delete":
        MCB.clear()
        print("Cleared.")

    elif sys.argv[1] in MCB:
        key = sys.argv[1]
        text = MCB[key]
        pyperclip.copy(text)
        print("Copied to the clipboard:\n", text)

    else:
        print(USAGE)
        sys.exit(1)

sys.exit(0)
