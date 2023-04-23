import random


def GerarCodigo():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    for letter in range(1, 7):
        password_list.append(random.choice(letters))
    
    for symbol in range(1, 3):
        password_list.append(random.choice(symbols))
    
    for number in range(1, 4):
        password_list.append(random.choice(numbers))

    random.shuffle(password_list)

    password = ""

    for char in password_list:
        password += char

    return password