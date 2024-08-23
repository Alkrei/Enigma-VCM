import pygame
from lang import en_ascii_lower, en_ascii_upper
from fonts import f2
from settings import *
from buttons import Button


class Rotor(object):
    def __init__(self, pos, disk, rect_pos):
        """Потом настройку можно рандомизировать"""
        self.disk = disk
        self.pos = pos
        self.ABC = en_ascii_upper
        self.abc = en_ascii_lower
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
        self.num_pos = (self.rect.x + 25, self.rect.y + 107)
        self.move = False
        self.remove = False

        while self.disk[0] != self.pos:
            if self.pos == 26:
                break
            else:
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
    def __init__(self, rect_pos, pos=1):
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
        self.num_pos = (self.rect.x + 25, self.rect.y + 107)
        self.move = False
        self.remove = False

        # buttons
        self.image_up_active = './graphics/Buttons/Up_Button_active.png'
        self.image_up_inactive = './graphics/Buttons/Up_Button_inactive.png'
        self.image_down_active = './graphics/Buttons/Down_Button_active.png'
        self.image_down_inactive = './graphics/Buttons/Down_Button_inactive.png'
        self.UpButton = Button(self.rect.x + 8, self.rect.topleft[-1] - 32, 64, 64, self.image_up_inactive, self.image_up_active, action=lambda: self.switch())
        self.DownButton = Button(self.rect.x + 8, self.rect.bottomleft[-1] - 32, 64, 64, self.image_down_inactive, self.image_down_active, action=lambda: self.re_switch())

    def draw(self, surface, screen):
        self.animation()
        surface.blit(self.image, self.rect)
        surface.blit(self.num, self.num_pos)
        self.UpButton.button(surface, screen)
        self.DownButton.button(surface, screen)

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