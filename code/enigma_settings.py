import pygame
import json
import sys
import os
import getpass
import platform
import pygame_gui
import pygame_gui.data
from settings import *
from transition import FadeOutTransition
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UITextEntryLine
from fonts import f2
from rotor import SettingsRotor

clock = pygame.time.Clock()


class EnigmaSettings:
    def __init__(self, screen):
        self.screen = screen
        self.surf = pygame.image.load('./graphics/Main/settings.png')
        self.message = f2.render("_If you need to use other lang. or symb. use ctrl-v_", False, WHITE)
        self.second_message = f2.render("_VCM will be restarted after save_", False, WHITE)
        self.message_pos = (70, 300)
        self.second_message_pos = (70, 350)

        self.path_filename = "./json/path.json"
        self.rotors_poss_filename = "./json/rotors_poss.json"
        self.new_settings = False

        self.manager = pygame_gui.ui_manager.UIManager((self.screen.get_size()), './themes/enigma_settings.json')
        self.rotor_manager = pygame_gui.UIManager((screen.get_size()), './themes/settings_rotor.json')
        self.button_manager = pygame_gui.ui_manager.UIManager((self.screen.get_size()),
                                                              './themes/enigma_settings_buttons.json')

        self.save_button = UIButton(relative_rect=pygame.Rect((564, 900), (336, 72)),
                                    manager=self.button_manager,
                                    text='Save',
                                    object_id=ObjectID(class_id="button"))
        self.quite_button = UIButton(relative_rect=pygame.Rect((50, 900), (336, 72)),
                                     text="Quite",
                                     manager=self.button_manager,
                                     object_id=ObjectID(class_id="button"))
        with open(self.rotors_poss_filename) as f:
            rotors_poss = json.load(f)
            self.rotors_poss = rotors_poss
            self.base_rotors_poss = self.rotors_poss.copy()

        self.FirstRotor = SettingsRotor((1029, 74), self.rotor_manager, self.rotors_poss[0])
        self.SecondRotor = SettingsRotor((1365, 74), self.rotor_manager, self.rotors_poss[1])
        self.ThirdRotor = SettingsRotor((1701, 74), self.rotor_manager, self.rotors_poss[2])

        self.username = getpass.getuser()
        self.type_os = platform.system()
        try:
            with open(self.path_filename) as f:
                path = json.load(f)
                self.path = path
        except FileNotFoundError:
            self.path = ""
            """ if self.type_os == "Linux":
                user_downloads_path = "Загрузки"
                default_path_d = "/home/" + self.username + "/" + user_downloads_path + "/"
                self.path = default_path_d
            elif self.type_os == "Windows":
                user_downloads_path = "Downloads"
                default_path_d_win = r"C:/Users/" + self.username + r"/" + user_downloads_path + r"/"
                self.path = default_path_d_win
            else:"""
        self.file_path = UITextEntryLine(relative_rect=pygame.Rect((50, 75), (841, 72)),
                                         manager=self.manager,
                                         object_id=ObjectID(class_id="text_entry_line"))
        if os.path.exists(self.path):
            try:
                self.file_path.set_text(self.path)
            except TypeError:
                self.file_path.set_text("Not visible symbols")
        elif self.file_path.text == "":
            self.path = self.file_path.text
            self.file_path.set_text("No Directory")
        else:
            try:
                with open(self.path_filename) as f:
                    path = json.load(f)
                    self.path = path
            except FileNotFoundError:
                with open(self.path_filename, "w") as f:
                    self.path = ""
                    json.dump(self.path, f)

    def s_rotors_draw(self):
        self.FirstRotor.draw(self.screen)
        self.SecondRotor.draw(self.screen)
        self.ThirdRotor.draw(self.screen)

    def check_save_button(self):
        if self.rotors_poss != self.base_rotors_poss:
            self.save_button.enable()
        elif os.path.exists(
                self.path) and self.file_path.text == self.path or self.file_path.text == "Default Downloads" \
                or self.file_path.text == "No Directory":
            self.save_button.disable()
        else:
            self.save_button.enable()

    def save_path_func(self):
        if os.path.exists(self.file_path.text):
            self.path = self.file_path.text
            try:
                with open(self.path_filename, "w") as f:
                    json.dump(self.path, f)
            except FileNotFoundError:
                with open(self.path_filename, "w") as f:
                    json.dump(self.path, f)
        elif self.file_path.text == "":
            self.path = self.file_path.text
            try:
                with open(self.path_filename, "w") as f:
                    json.dump(self.path, f)
            except FileNotFoundError:
                with open(self.path_filename, "w") as f:
                    json.dump(self.path, f)
            self.file_path.set_text("No Directory")
        else:
            print("Error")

    def save_rotors_poss_func(self):
        with open(self.rotors_poss_filename, "w") as f:
            self.base_rotors_poss = self.rotors_poss.copy()
            json.dump(self.rotors_poss, f)

    def re_transition(self, transition):
        while not transition.transitioning:
            time_delta = clock.tick(FPS)
            self.screen.blit(self.surf, (0, 0))
            self.screen.blit(self.message, self.message_pos)
            self.screen.blit(self.second_message, self.second_message_pos)
            self.check_save_button()
            self.s_rotors_draw()
            self.button_manager.draw_ui(self.screen)
            self.rotor_manager.draw_ui(self.screen)
            self.manager.draw_ui(self.screen)
            transition.re_update()
            self.screen.blit(transition.image, (0, 0))
            pygame.time.wait(10)
            self.button_manager.update(time_delta)
            self.rotor_manager.update(time_delta)
            self.manager.update(time_delta)
            pygame.display.update()

    def draw(self):
        time_delta = clock.tick(FPS)
        self.screen.blit(self.surf, (0, 0))
        self.screen.blit(self.message, self.message_pos)
        self.screen.blit(self.second_message, self.second_message_pos)
        self.s_rotors_draw()
        self.button_manager.draw_ui(self.screen)
        self.manager.draw_ui(self.screen)
        self.rotor_manager.draw_ui(self.screen)
        self.button_manager.update(time_delta)
        self.rotor_manager.update(time_delta)
        try:
            self.manager.update(time_delta)
        except TypeError:
            self.file_path.set_text("Not visible symbols")
        pygame.display.update()

    def start(self, self_transition):
        play = True
        self.re_transition(self_transition)
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.save_button:
                        self.save_path_func()
                        self.save_rotors_poss_func()
                        self.new_settings = True
                    elif event.ui_element == self.quite_button:
                        transition = FadeOutTransition()
                        while transition.transitioning:
                            transition.update()
                            self.screen.blit(transition.image, (0, 0))
                            pygame.time.wait(30)
                            pygame.display.update()
                            clock.tick(FPS)
                        yield transition
                        yield self.path
                        yield self.rotors_poss
                        yield self.new_settings
                    elif event.ui_element == self.FirstRotor.Up_Button:
                        self.FirstRotor.switch()
                        self.rotors_poss[0] = self.FirstRotor.pos
                    elif event.ui_element == self.FirstRotor.Down_Button:
                        self.FirstRotor.re_switch()
                        self.rotors_poss[0] = self.FirstRotor.pos

                    elif event.ui_element == self.SecondRotor.Up_Button:
                        self.SecondRotor.switch()
                        self.rotors_poss[1] = self.SecondRotor.pos
                    elif event.ui_element == self.SecondRotor.Down_Button:
                        self.SecondRotor.re_switch()
                        self.rotors_poss[1] = self.SecondRotor.pos

                    elif event.ui_element == self.ThirdRotor.Up_Button:
                        self.ThirdRotor.switch()
                        self.rotors_poss[2] = self.ThirdRotor.pos
                    elif event.ui_element == self.ThirdRotor.Down_Button:
                        self.ThirdRotor.re_switch()
                        self.rotors_poss[2] = self.ThirdRotor.pos
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        transition = FadeOutTransition()
                        while transition.transitioning:
                            transition.update()
                            self.screen.blit(transition.image, (0, 0))
                            pygame.time.wait(30)
                            pygame.display.update()
                            clock.tick(FPS)
                        yield transition
                        yield self.path
                        yield self.rotors_poss
                        yield self.new_settings
                self.check_save_button()
                self.button_manager.process_events(event)
                self.rotor_manager.process_events(event)
                try:
                    self.manager.process_events(event)
                except TypeError:
                    self.file_path.set_text("Not visible symbols")
            self.draw()
