#! python3
"""
Read data from users.txt, and generate nicknames.
Print sorted table of users, like
"Montgomery, Albert L... (1601) almontgo"
v1 summer 2020
v2 print users in 2 columns
"""
import sys
import collections

ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)
User = collections.namedtuple("User", "nickname forename middlename surname id")


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print(f"USAGE: {sys.argv[0]} users.txt")
        sys.exit(1)

    users = {}
    nicknames = set()

    for line in open(sys.argv[1], encoding='utf8'):
        line = line.rstrip()
        if line:
            user = process_line(line, nicknames)

            key = (user.surname.lower(), user.forename.lower(), user.id)
            users[key] = user

    print_users(users)
    sys.exit(0)


def process_line(line, nicknames):
    fields = line.split(":")
    nickname = generate_nickname(fields, nicknames)
    user = User(
        nickname, fields[FORENAME], fields[MIDDLENAME], fields[SURNAME], fields[ID]
    )
    return user


def generate_nickname(fields, nicknames):
    nickname = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] +
                 fields[SURNAME]).replace("-", "").replace("\'", ""))

    original_nickname = nickname = nickname[:8].lower()

    count = 1
    while nickname in nicknames:
        nickname = f"{original_nickname}{count}"
        count += 1

    nicknames.add(nickname)
    return nickname


def print_users(users):
    """
    generate name, max 19 char + '.'
    print headers in 2 columns
    print users in 2 columns
    print new headers every 64 row
    """
    namewidth = 20
    idwidth = 6
    nicknamewidth = 9
    new_header = 64

    a = f"{'Name':{namewidth}} {'ID':{idwidth}} {'Username':{nicknamewidth}}"
    b = f"{'':-<{namewidth}} {'':-<{idwidth}} {'':-<{nicknamewidth}}"
    header = f"{a}\t{a}\n"\
             f"{b}\t{b}"
    print(header)

    row = 0
    new_row_flag = False
    for key in sorted(users):
        if row == new_header:
            print(f"\n{header}")
            row = 0

        user = users[key]
        name = f"{user.surname}, {user.forename}"

        if user.middlename and len(name) < namewidth - 2:
            name += f" {user.middlename[0]}"

        if len(name) > namewidth - 1:
            name = name[:namewidth-1]

        print(f"{name:.<{namewidth}} ({user.id:{idwidth-4}}) "
              f"{user.nickname:{nicknamewidth}}", end='')

        if new_row_flag is True:
            print()
            row += 1
            new_row_flag = False
        else:
            print('\t', end='')
            new_row_flag = True

    if new_row_flag is True:
        print()


if __name__ == '__main__':
    main()
