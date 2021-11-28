#! python3
""" Is this text a haiku?
    Will assume that there are exactly the
    same number of syllables as there are vowels. """
import re

text0 = "Вечер за окном. / Еще один день прожит. / Жизнь скоротечна..."
text1 = "just text"
text2 = "Как вишня расцвела! / Она с коня согнала / И князя-гордеца."
text3 = "На голой ветке / Ворон сидит одиноко... / Осенний вечер!"
text4 = "Тихо, тихо ползи, / Улитка, по склону Фудзи, / Вверх, до самых высот!"
text5 = "Жизнь скоротечна... / Думает ли об этом / Маленький мальчик."
texts = [text0, text1, text2, text3, text4, text5]

ruVowelsRegex = re.compile(r'[аАеЕёЁиИоОуУыЫэЭюЮяЯ]{1}')

for i, text in enumerate(texts):
    result = re.split(r'\s*(/)\s*', text)
    if len(result) < 5:
        print(f"Text {i} is not a haiku. There should be 3 rows.")
        continue

    one = len(ruVowelsRegex.findall(result[0]))
    two = len(ruVowelsRegex.findall(result[2]))
    three = len(ruVowelsRegex.findall(result[4]))
    if one != 5:
        print(f"Text {i} is not a haiku. There should be 5 syllables in 1st row, but it has {one}.")
    elif two != 7:
        print(f"Text {i} is not a haiku. There should be 7 syllables in 2nd row, but it has {two}.")
    elif three != 5:
        print(f"Text {i} is not a haiku. There should be 5 syllables in 3rd row, but it has {three}.")
    else:
        print(f"Text {i} is haiku!")
