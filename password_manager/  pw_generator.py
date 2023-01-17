import random


class Password:
    def __init__(self):
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u',
                        'v',
                        'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                        'P', 'Q',
                        'R',
                        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        self.letterpw = ""
        self.symbolpw = ""
        self.numberpw = ""

    def generate_password(self):
        for i in range(0, 8):
            letter_input = random.choice(self.letters)
            self.letterpw += letter_input

        for i in range(0, 3):
            symbol_input = random.choice(self.symbols)
            self.symbolpw += symbol_input

        for i in range(0, 2):
            number_input = random.choice(self.numbers)
            self.numberpw += number_input

        pw = self.letterpw + self.symbolpw + self.numberpw
        password = ''.join(random.sample(pw, len(pw)))

        return password
