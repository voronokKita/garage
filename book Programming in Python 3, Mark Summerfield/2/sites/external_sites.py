#! python3
""" Reads content of HTML files from the command line,
    displays a list of the websites that are found in the files. v2"""
import sys
import collections


if len(sys.argv) < 2:
    print(f"USAGE: {sys.argv[0]} 1.html [2.html ... n.html]")
    sys.exit(1)

sites = collections.defaultdict(set)
for filename in sys.argv[1:]:
    # Search for pattern in every row:
    for line in open(filename):
        cursor = 0
        shift = 0
        while True:
            site = None
            cursor = line.find("http://", cursor)
            # If pattern found:
            if cursor > -1:
                cursor += len("http://")
                # Shift to the end of pattern;
                for shift in range(cursor, len(line)):
                    if not (line[shift].isalnum() or line[shift] in ".-"):
                        site = line[cursor:shift].lower()
                        break
                # Put the site in dict (sitename:filename.html)
                if site and "." in site:
                    sites[site].add(filename)

                cursor = shift
            else:
                break

for site in sites:
    print(f"{site} is in:")
    for filename in sorted(sites[site], key=str.lower):
        print(f"    {filename}")

sys.exit(0)
