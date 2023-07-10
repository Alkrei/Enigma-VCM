import string


class Reflector:
    def __init__(self, disk):
        self.disk = disk

        self.ABC = str(string.ascii_uppercase)
        self.abc = str(string.ascii_lowercase)
        self.alphabet = ''
        print(self.ABC)

    def code(self, letter):
        result_letter = 0
        if letter in self.ABC:
            self.alphabet = self.ABC
        elif letter in self.abc:
            self.alphabet = self.abc

        index = self.alphabet.index(letter) + 1

        for section in self.disk:
            if index == section[0]:
                result_letter = self.alphabet[section[1] - 1]
            if index == section[1]:
                result_letter = self.alphabet[section[0] - 1]

        return result_letter
