import string
from fonts import f2
from settings import *
import pygame
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton


class Rotor:
    def __init__(self, pos, disk, rect_pos):
        """Потом настройку можно рандомизировать"""
        self.disk = disk
        self.pos = pos
        self.ABC = str(string.ascii_uppercase)
        self.abc = str(string.ascii_lowercase)
        self.alphabet = ''

        self.move_sprites = [pygame.image.load("./graphics/Rotor/Rotor1.png"),
                             pygame.image.load("./graphics/Rotor/Rotor2.png"),
                             pygame.image.load("./graphics/Rotor/Rotor3.png")]
        self.re_move_sprites = [pygame.image.load("./graphics/Rotor/Rotor3.png"),
                                pygame.image.load("./graphics/Rotor/Rotor2.png"),
                                pygame.image.load("./graphics/Rotor/Rotor1.png")]
        self.current_sprite = 0
        self.num = f2.render(f"{self.pos}", False, BLACK)
        self.image = self.move_sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=rect_pos)
        self.num_pos = (self.rect.x + 23, self.rect.y + 112)
        self.move = False
        self.remove = False

        while self.disk[0] != self.pos:
            i = self.disk.pop(-1)
            self.disk.insert(0, i)

    def draw(self, screen):
        self.animation()
        screen.blit(self.image, self.rect)
        screen.blit(self.num, self.num_pos)

    def animation(self):
        if self.move:
            self.current_sprite += 0.5

            if self.current_sprite >= len(self.move_sprites):
                self.move = False
                self.current_sprite = 0
            self.image = self.move_sprites[int(self.current_sprite)]
        elif self.remove:
            self.current_sprite += 0.5

            if self.current_sprite >= len(self.re_move_sprites):
                self.remove = False
                self.current_sprite = 0
            self.image = self.re_move_sprites[int(self.current_sprite)]

    def code(self, letter, reflection=False):
        result_letter = 0

        if letter in self.ABC:
            self.alphabet = self.ABC
        elif letter in self.abc:
            self.alphabet = self.abc

        if not reflection:
            index = self.alphabet.index(letter)
            # print(f"Letter index {index}")
            result_letter = self.alphabet[self.disk[index]]
        else:
            index = self.alphabet.index(letter)
            for section in self.disk:
                if index == section:
                    result_letter = self.alphabet[self.disk.index(section)]
                    # print(self.alphabet.index(result_letter))

        # print(self.disk)
        return result_letter

    def switch(self, order=None):
        if order is None:
            self.pos += 1
            i = self.disk.pop(-1)
            self.disk.insert(0, i)

            if self.pos == 27:
                self.pos = 1
        else:
            if order == 26:
                self.pos += 1
                i = self.disk.pop(-1)
                self.disk.insert(0, i)

                if self.pos == 27:
                    self.pos = 1
        self.num = f2.render(f"{self.pos}", False, BLACK)

        self.move = True

    def re_switch(self, times=1):
        while times != 0:
            self.pos -= 1
            i = self.disk.pop(0)
            self.disk.append(i)

            if self.pos == 0:
                self.pos = 26
            self.num = f2.render(f"{self.pos}", False, BLACK)
            times -= 1

            self.remove = True


class SettingsRotor:
    def __init__(self, rect_pos, manager, pos=1):
        self.pos = pos

        self.move_sprites = [pygame.image.load("./graphics/Rotor/Rotor1.png"),
                             pygame.image.load("./graphics/Rotor/Rotor2.png"),
                             pygame.image.load("./graphics/Rotor/Rotor3.png")]
        self.re_move_sprites = [pygame.image.load("./graphics/Rotor/Rotor3.png"),
                                pygame.image.load("./graphics/Rotor/Rotor2.png"),
                                pygame.image.load("./graphics/Rotor/Rotor1.png")]
        self.current_sprite = 0
        self.num = f2.render(f"{self.pos}", False, BLACK)
        self.image = self.move_sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=rect_pos)
        self.num_pos = (self.rect.x + 23, self.rect.y + 112)
        self.move = False
        self.remove = False
        self.manager = manager

        self.Up_Button = UIButton(relative_rect=pygame.Rect((self.rect.x + 8, self.rect.topleft[-1] - 32), (64, 64)),
                                  manager=self.manager,
                                  text='',
                                  object_id=ObjectID(class_id="up_button"))
        self.Down_Button = UIButton(
                                  relative_rect=pygame.Rect((self.rect.x + 8, self.rect.bottomleft[-1] - 32), (64, 64)),
                                  manager=self.manager,
                                  text='',
                                  object_id=ObjectID(class_id="down_button"))

    def draw(self, screen):
        self.animation()
        screen.blit(self.image, self.rect)
        screen.blit(self.num, self.num_pos)

    def animation(self):
        if self.move:
            self.current_sprite += 0.5

            if self.current_sprite >= len(self.move_sprites):
                self.move = False
                self.current_sprite = 0
            self.image = self.move_sprites[int(self.current_sprite)]
        elif self.remove:
            self.current_sprite += 0.5

            if self.current_sprite >= len(self.re_move_sprites):
                self.remove = False
                self.current_sprite = 0
            self.image = self.re_move_sprites[int(self.current_sprite)]

    def switch(self):
        self.pos += 1

        if self.pos == 27:
            self.pos = 1
        self.num = f2.render(f"{self.pos}", False, BLACK)

        self.move = True

    def re_switch(self, times=1):
        while times != 0:
            self.pos -= 1

            if self.pos == 0:
                self.pos = 26
            self.num = f2.render(f"{self.pos}", False, BLACK)
            times -= 1

            self.remove = True
