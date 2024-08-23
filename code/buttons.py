import pygame
from settings import *


class Button:
    def __init__(self, x, y, w, h, inactive, active, font = None, name = None, action = None, second_action = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = font
        self.name = name
        self.inactive = pygame.image.load(inactive)
        self.active = pygame.image.load(active)
        self.action = action
        self.second_action = second_action

    def button(self, surface, screen):
        mouse = pygame.mouse.get_pos()
        x = (self.x * screen.get_width()) / surface.get_width()
        y = (self.y * screen.get_height()) / surface.get_height()
        w = (self.w * screen.get_width()) / surface.get_width()
        h = (self.h * screen.get_height()) / surface.get_height()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            surface.blit(self.active, (self.x, self.y))
            if self.name is not None:
                text = self.font.render(self.name, False, WHITE)
                text_w, text_h = self.font.size(self.name)
                surface.blit(text, (self.x + (self.w / 2) - (text_w / 2), self.y + (self.h / 4.5)))
            if pygame.mouse.get_pressed()[0] and self.action is not None:
                surface.blit(self.inactive, (self.x, self.y))
            if pygame.mouse.get_just_released()[0] and self.action is not None:
                self.action()
                if self.second_action is not None:
                    self.second_action()
        else:
            surface.blit(self.inactive, (self.x, self.y))
        if self.name is not None:
            text = self.font.render(self.name, False, WHITE)
            text_w, text_h = self.font.size(self.name)
            surface.blit(text, (self.x + (self.w / 2) - (text_w / 2), self.y + (self.h / 4.5)))