#! python3
""" spring 2021
methods:
    pattern = re.compile(?) create regex
    pattern.search(text) search from beginning of string
    pattern.findall(text) return list of patterns
    pattern.match(text) check match's
    pattern.fullmatch(text)
    result.group(i) return match object
    result.groups()
    result.start(i) return beginning index
    result.end(i) return ending index
    re.split(pattern, text)
    re.sub(pattern, replace, text)
    re.finditer(pattern, text) iterator that return match-objects
compiler's flags:
    re.I ignore case
    re.DOTALL include \n in search
    re.VERBOSE extended commentary
    re.ASCII lower variants of symbol's
    re.MULTILINE operators ^ and $ work in each line
symbols:
    . any symbol except \n
    \d is digit
    \w is digit or letter
    \s is spase
    \D \W \S is all except this symbol's
    \b is word border
    \B not borders
    [abc] symbol group
    [^1-9] is all except symbol group
occurrence:
    ? 0 or 1 occurrence
    * 0 or >= more
    + 1 or >= more
    {n} n occurrence
    {n,} n or more
    {,m} from 0 to m
    {n,m} from n to m occurrence
    {n,m}? OR *? OR +? is nogreedy search
    (?:...) non capturing group
positions:
    ^beginning
    the_end$
    (?=...) lookahead assertion
    (?!...) negative lookahead assertion
    (?<=...) lookbehind assertion
    (?<!...) negative lookbehind assertion

(?<=#START#).*?(?=#END#)
^(?:(?!foo)(?!bar).)*?$ - line in text without foo and bar
"""
import re

phoneRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))?              # code?
    (\s|-)?                         # sep?
    \d{3}                           # number digits
    (\s|-)                          # sep
    \d{4}                           # number digits
    (\s*(ext|x|ext.)\s*\d{2,5})?    # addition?
    )''', re.VERBOSE | re.I | re.DOTALL)
number = "Number is 666-999-4242 ext. 777"
result = phoneRegex.search(number)
# groups:
#   0) 666-999-4242 ext. 777
#   1) 666-999-4242 ext. 777
#   2) 666
#   3) -
#   4) -
#   5) ext. 777
#   6) ext.
print(result.groups())

text = "We arrive on 03/25/2018. So you are welcome after 04/01/2018."
print(re.sub(r'(\d\d)/(\d\d)/(\d{4})', r'\2.\1.\3', text))

def repl(match):
    return '>censored(' + str(len(match[0])) + ')<'
text = "Некоторые хорошие слова подозрительны: хор, хоровод, хороводоводовед."
print(re.sub(r'\b[хХxX]\w*', repl, text))

phoneNumRegex = re.compile(r"(\d{3})-(\d{3}-\d{4})")
number = "Number is 666-999-4242 lalala"
result = phoneNumRegex.search(number)
code, num = result.groups()
print(f"Result is ({code}) {num}")

heroRegex = re.compile(r"Batman|Tina Fey")
s = "Batman and Tina Fey."
result = heroRegex.search(s)
print(f"Hero is {result.group()}")

batRegex = re.compile(r"Bat(man|mobile|copter|cat)")
s = "Batmobile lost a wheel"
result = batRegex.search(s)
print("Bat" + result.group(1))

womanRegex = re.compile(r"Bat(wo)?man")
s = "The Adventures of Batman"
result = womanRegex.search(s)
print(result.group())

wowoRegex = re.compile(r"Bat(wo)*man")
s = "Batwowowowowoman"
result = wowoRegex.search(s)
print(result.group())

crossRegex = re.compile(r"Bat(wo)+man")
s = "Batman"
result = crossRegex.search(s)
print("result == None:", result == None)

haRegex = re.compile(r"(HA){,5}")
s = "HAHAHAHA"
result = haRegex.search(s)
print(result.group())

nogreedyRegex = re.compile(r"(HA){1,5}?")
s = "HAHAHAHAHA"
result = nogreedyRegex.search(s)
print(result.group())

numbers = "Number is 666-999-4242 lalala 999-666-4242"
phonesNumRegex = re.compile(r"(\d{3})-(\d{3}-\d{4})")
result = phonesNumRegex.findall(numbers)
print(result)
print(f"Codes {result[0][0]}, {result[1][0]}; numbers {result[0][1]}, {result[1][1]}.")

xmasRegex = re.compile(r"\d+\s\w+")
s = "12 drummers, 11 pipers, 10 lords, 9 ladies, 8 maids, " \
    "7 swans, 6 geese, 5 rings, 4 birds, 3 hens, 2 doves, 1 partridge"
result = xmasRegex.findall(s)
print(*result, sep=", ")

vowelRegex = re.compile(r"[aeiou0-5]")
s = "RoboCop eats baby food. 1234567890"
result = vowelRegex.findall(s)
print(*result)

invertRegex = re.compile(r"[^aeiou0-5 ]")
s = "RoboCop eats baby food. 1234567890"
result = invertRegex.findall(s)
print(*result)

helloRegex = re.compile(r"^Hello(.*?)World!$")
s = "Hello regular expressions World!"
result = helloRegex.search(s)
print(result.group())

spRegex = re.compile(r".*", re.DOTALL)
s = "Serve the public trust.\nProtect the innocent.\nUphold the law."
result = spRegex.search(s)
print(result.group())

caseRegex = re.compile(r"robocop", re.I)
s = "Al, why does your programing book talk about ROBOCOP so much?"
result = caseRegex.search(s)
print(result.group().capitalize(), "protects the innocent.")

agentsRegex = re.compile(r"Agent (\w)\w*")
s = "Agent Alice told Agent Carol that Agent Eve knew Agent Bob was a double agent."
result = agentsRegex.sub(r"\1****", s)
print(result)
