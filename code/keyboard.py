import pygame
from fonts import f1
from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, letter, pos):
        super().__init__()
        self.image = pygame.image.load("./graphics/Enigma/Key.png")
        self.light_image = pygame.image.load("./graphics/Enigma/LightKey.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.ltr = letter
        self.letter = f1.render(letter, False, GRAY)
        self.light_letter = f1.render(letter, False, WHITE)
        self.light = False


class Keyboard:
    def __init__(self, alphabet, screen):
        self.all_buttons = []
        self.screen = screen
        for letter, pos in alphabet.items():
            button = Button(letter, pos)
            self.all_buttons.append(button)

    def draw(self):
        for button in self.all_buttons:
            if button.light:
                self.screen.blit(button.light_image, button.rect.topleft)
                width = button.light_letter.get_rect().w
                x = (button.image.get_width() / 2) + button.rect.x - (width / 2)
                self.screen.blit(button.light_letter, (x, button.rect.y + (button.light_letter.get_rect().h / 2)))
            else:
                self.screen.blit(button.image, button.rect.topleft)
                width = button.letter.get_rect().w
                x = (button.image.get_width() / 2) + button.rect.x - (width / 2)
                self.screen.blit(button.letter, (x, button.rect.y + (button.letter.get_rect().h / 2)))
