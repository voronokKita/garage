answer = input("What is your name?\n")
if answer.isalpha():
    print('Hello, ', answer, '!', sep='')
else:
    print("Hello, World!")
