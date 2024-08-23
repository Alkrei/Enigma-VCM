import pygame
import copykitten
import json
import sys
import os
from copykitten import CopykittenError
from settings import *
from transition import FadeOutTransition
from fonts import f3
from rotor import SettingsRotor
from buttons import Button
from path_input_box import PathInputBox

clock = pygame.time.Clock()

class EnigmaSettings:
    def __init__(self, surface, screen):
        self.surface = surface
        self.screen = screen
        self.title  = pygame.image.load('./graphics/Main/settings.png')
        self.quite = False
        self.new_settings = False

        # jsons
        self.path_filename = "./json/path.json"
        self.rotors_poss_filename = "./json/rotors_poss.json"

        # buttons
        self.image_active = './graphics/Buttons/Button_active.png'
        self.image_inactive = './graphics/Buttons/Button_inactive.png'

        self.SaveButton = Button(564, 900, 336, 72, self.image_inactive, self.image_active, f3, "Save", lambda: self.save_func())
        self.QuiteButton = Button(50, 900, 336, 72, self.image_inactive, self.image_active, f3, "Quite", lambda: self.quite_func())
        self.PathInputBox = PathInputBox()

        # rotors
        with open(self.rotors_poss_filename) as f:
            rotors_poss = json.load(f)
            self.rotors_poss = rotors_poss
            self.base_rotors_poss = self.rotors_poss.copy()

        self.FirstRotor = SettingsRotor((1029, 74), self.rotors_poss[0])
        self.SecondRotor = SettingsRotor((1365, 74), self.rotors_poss[1])
        self.ThirdRotor = SettingsRotor((1701, 74), self.rotors_poss[2])

        # path
        try:
            with open(self.path_filename) as f:
                path = json.load(f)
                self.path = path
        except FileNotFoundError:
            with open(self.path_filename, "w") as f:
                self.path = "./"
                json.dump(self.path, f)

        if os.path.exists(self.path):
            self.PathInputBox.text = self.path
        else:
            pass

    def save_path_func(self):
        if os.path.exists(self.PathInputBox.text):
            self.path = self.PathInputBox.text
            with open(self.path_filename, "w") as f:
                json.dump(self.path, f)
        elif self.PathInputBox.text == "":
            self.path = self.PathInputBox.text
            with open(self.path_filename, "w") as f:
                json.dump(self.path, f)
            self.PathInputBox.set_text("No Directory")
        else:
            self.PathInputBox.set_text("Directory does not exist")

    def save_rotors_poss_func(self):
        with open(self.rotors_poss_filename, "w") as f:
            self.base_rotors_poss = self.rotors_poss.copy()
            json.dump(self.rotors_poss, f)

    def save_func(self):
        self.save_path_func()
        self.save_rotors_poss_func()
        self.new_settings = True

    def quite_func(self):
        self.quite = True

    def re_transition(self, transition):
        self.quite = False
        while not transition.transitioning:
            self.surface.blit(self.title, (0, 0))
            self.s_rotors_draw()
            self.draw_buttons()
            self.PathInputBox.draw(self.surface, self.screen)
            self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
            transition.re_update()
            self.screen.blit(transition.image, (0, 0))
            pygame.time.wait(10)
            pygame.display.update()

    def s_rotors_draw(self):
        self.FirstRotor.draw(self.surface, self.screen)
        self.SecondRotor.draw(self.surface, self.screen)
        self.ThirdRotor.draw(self.surface, self.screen)

        self.rotors_poss[0] = self.FirstRotor.pos
        self.rotors_poss[1] = self.SecondRotor.pos
        self.rotors_poss[2] = self.ThirdRotor.pos

    def draw_buttons(self):
        self.QuiteButton.button(self.surface, self.screen)
        if (self.rotors_poss != self.base_rotors_poss or self.PathInputBox.text != self.path
                or self.PathInputBox.text == "No Directory"
                or self.PathInputBox.text == "Directory does not exist"):
            self.SaveButton.button(self.surface, self.screen)

    def draw(self):
        self.surface.blit(self.title, (0, 0))
        self.s_rotors_draw()
        self.draw_buttons()
        self.PathInputBox.draw(self.surface, self.screen)
        self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
        pygame.display.update()

    def start(self, self_transition):
        self.re_transition(self_transition)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PathInputBox.input_rect.collidepoint(event.pos):
                        self.PathInputBox.active = True
                    else:
                        self.PathInputBox.active = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quite_func()
                    if event.key == pygame.K_BACKSPACE and self.PathInputBox.active:
                        self.PathInputBox.backspace()
                    if (event.key == pygame.K_v) and (event.mod & pygame.KMOD_CTRL) and self.PathInputBox.active:
                        try:
                            self.PathInputBox.update_text(copykitten.paste())
                        except CopykittenError:
                            pass
                if event.type == pygame.TEXTINPUT and self.PathInputBox.active:
                    self.PathInputBox.update_text(event.text)
            self.draw()
            if self.quite:
                transition = FadeOutTransition()
                while transition.transitioning:
                    transition.update()
                    self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
                    self.screen.blit(transition.image, (0, 0))
                    pygame.time.wait(30)
                    pygame.display.update()
                    clock.tick(FPS)
                yield transition
                yield self.new_settings