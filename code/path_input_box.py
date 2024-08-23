import pygame
from settings import *
from fonts import f2

class PathInputBox:
    def __init__(self):
        self.input_rect = pygame.rect.Rect(57,57,852,58)
        self.active = False

        # text
        self.text = ""
        self.user_text = ""
        self.text_surface = f2.render(self.user_text,True,WHITE)

    def backspace(self):
        self.text = self.text[:-1]

    def update_text(self, text):
        self.text += text

    def set_text(self, text):
        self.text = text

    def draw(self, surface, screen):
        w = ((self.input_rect.w - 10) * surface.get_width()) / screen.get_width()
        text_w = (f2.size(self.text)[0]* surface.get_width()) / screen.get_width()
        if w <= text_w:
            self.user_text = f"...{self.text[-44:]}"
            self.text_surface = f2.render(self.user_text, True, WHITE)
        else:
            self.user_text = self.text
            self.text_surface = f2.render(self.user_text, True, WHITE)
        if self.active:
            pygame.draw.rect(surface, LIGHTSKYBLUE, self.input_rect, 2)
        elif not self.active:
            pygame.draw.rect(surface, BORDERGRAY, self.input_rect, 2)
        surface.blit(self.text_surface,(self.input_rect.x + 10, self.input_rect.y + 5))