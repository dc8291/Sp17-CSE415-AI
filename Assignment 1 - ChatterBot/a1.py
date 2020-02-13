def four_x_cubed_plus_1(x):
    return 4 * x ** 3 + 1


def mystery_code(x, num):
    lists = list(x)
    num = num % 33
    final = ""
    for letter in lists:
        if letter.islower():
            asciicode = ord(letter) - num
            if asciicode > 90:
                asciicode = asciicode - 90 + 64
            letter = chr(asciicode)
        elif letter.isupper():
            asciicode = ord(letter) + 64 - num
            if asciicode > 122:
                asciicode = asciicode - 122 + 96
            letter = chr(asciicode)
        final += letter
    return final


def quintuples(x):
    index = 0
    final = []
    num = len(x) // 5
    for n in range(num):
        final.append(x[index: index + 5])
        index += 5
    if not (len(x) % 5 == 0):
        final.append(x[index:])
    return final


def past_tense(words):
    final = []
    dictionary = {'have': 'had', 'be': 'was', 'eat': 'ate', 'go': 'went'}
    vowels = ['a', 'e', 'i', 'o', 'u']
    for word in words:
        if word in dictionary:
            word = dictionary[word]
        elif word.endswith("e"):
            word += "d"
        elif word.endswith("y"):
            lists = list(word)
            lists[-1] = "i"
            word = "".join(lists) + "ed"
        elif word[-2] in vowels and not word[-3] in vowels and not (word.endswith("y")) and not (word.endswith("w")):
            word += word[len(word) - 1] + "ed"
        else:
            word += "ed"
        final.append(word)
    return final


print("""Calling four_x_cubed_plus_1(x)....
      x = 2
      Result: """
      + str(four_x_cubed_plus_1(2)) +
      "\n      Answer: 33")
print("""Calling mystery_code()....
      String = "abc Iz th1s Secure? n0, no, 9!"
      Key = 17
      Result: """
      + mystery_code("abc Iz th1s Secure? n0, no, 9!", 17) +
      "\n      Answer: PQR xO IW1H hTRJGT? C0, CD, 9!")
print("""Calling quintuples(x)....
      x = [2, 5, 1.5, 100, 3, 8, 7, 1, 1, 0, -2, -5]
      Result = """
      + str(quintuples([2, 5, 1.5, 100, 3, 8, 7, 1, 1, 0, -2, -5]))
      + "\n      Answer: [[2, 5, 1.5, 100, 3], [8, 7, 1, 1, 0], [-2, -5]]")
print("""Calling past_tense(x)....
      x = ['program', 'debug', 'execute', 'crash', 'repeat', 'eat']
      Result = """
      + str(past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat']))
      + "\n      Answer: ['programmed', 'debugged', 'executed', 'crashed', 'repeated', 'ate']")

