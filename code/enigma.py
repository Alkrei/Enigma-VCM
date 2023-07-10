import pygame
import sys
import os
import pygame_gui
import pygame_gui.data
import string
from tkinter import Tk
from pygame_gui.core import ObjectID
from pygame_gui.elements import UITextBox, UIButton
from settings import *
from fonts import f2
from rotor import Rotor
from reflector import Reflector
from keyboard import Keyboard
from lang import en_kb
from transition import FadeOutTransition

clock = pygame.time.Clock()


class Enigma:
    def __init__(self, screen, path, rotors_poss):
        self.screen = screen
        self.ascii = string.ascii_letters
        self.title = pygame.image.load('./graphics/Enigma/Enigma_VCM.png')
        self.input_rect = pygame.Rect(660, 77, 600, 251)
        self.manager = pygame_gui.ui_manager.UIManager((self.screen.get_size()), './themes/enigma.json')
        self.button_manager = pygame_gui.ui_manager.UIManager((self.screen.get_size()), './themes/panel.json')
        self.extra = (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                      pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0)
        self.all_symbols = 0
        self.limit = 1000
        self.limit_color = BLACK
        self.all_symbols_pos = (909, 439)
        self.path = path

        self.cipher_text = ""
        self.text = ""

        """self.d_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]
        self.d_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]
        self.d_3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]"""
        self.d_1 = [5, 14, 21, 2, 22, 15, 16, 18, 9, 20, 7, 12, 1, 11, 8, 0, 13, 10, 19, 17, 4, 3, 24, 25, 6, 23]
        self.d_2 = [9, 19, 23, 12, 4, 16, 22, 2, 15, 1, 20, 5, 17, 10, 21, 18, 25, 11, 0, 13, 7, 24, 14, 8, 3, 6]
        self.d_3 = [25, 9, 3, 5, 15, 6, 23, 20, 0, 2, 22, 1, 24, 18, 17, 10, 16, 8, 11, 19, 21, 14, 12, 7, 4, 13]
        self.ref_d = [(1, 22), (2, 16), (3, 21), (4, 14), (5, 24), (6, 23), (7, 20), (8, 18), (9, 17), (10, 15),
                      (11, 25),
                      (12, 19), (13, 26)]

        self.text_box = UITextBox(relative_rect=pygame.Rect(660, 77, 600, 251),
                                  manager=self.manager,
                                  html_text='',
                                  object_id=ObjectID(class_id="text_box"))
        self.hide_button = UIButton(relative_rect=pygame.Rect((1327, 95), (84, 84)),
                                    manager=self.button_manager,
                                    text='',
                                    object_id=ObjectID(class_id="hide_button"))

        self.trash_button = UIButton(relative_rect=pygame.Rect((1327, 226), (84, 84)),
                                     manager=self.button_manager,
                                     text='',
                                     object_id=ObjectID(class_id="trash_button"))

        self.copy_button = UIButton(relative_rect=pygame.Rect((1458, 95), (84, 84)),
                                    manager=self.button_manager,
                                    text='',
                                    object_id=ObjectID(class_id="copy_button"))

        self.save_button = UIButton(relative_rect=pygame.Rect((1458, 226), (84, 84)),
                                    manager=self.button_manager,
                                    text='',
                                    object_id=ObjectID(class_id="save_button"))

        self.quite_button = UIButton(relative_rect=pygame.Rect((100, 550), (84, 84)),
                                     manager=self.button_manager,
                                     text='',
                                     object_id=ObjectID(class_id="quite_button"))

        self.hide_button_pressed = pygame.image.load("./graphics/Buttons/Hide_Button_pressed.png")
        self.hide_button_activity = False
        self.keyboard = Keyboard(en_kb, self.screen)
        self.FirstRotor = Rotor(rotors_poss[2], self.d_1, (390, 74))
        self.SecondRotor = Rotor(rotors_poss[1], self.d_2, (246, 74))
        self.ThirdRotor = Rotor(rotors_poss[0], self.d_3, (102, 74))
        self.Reflector = Reflector(self.ref_d)

    def create_text_box(self):
        self.text_box = UITextBox(relative_rect=pygame.Rect(660, 77, 600, 251),
                                  manager=self.manager,
                                  html_text='',
                                  object_id=ObjectID(class_id="text_box"))

    def cipher(self, letter):
        self.FirstRotor.switch()
        result_letter = self.FirstRotor.code(letter)
        result_letter = self.SecondRotor.code(result_letter)
        result_letter = self.ThirdRotor.code(result_letter)

        result_letter = self.Reflector.code(result_letter)

        result_letter = self.ThirdRotor.code(result_letter, True)
        result_letter = self.SecondRotor.code(result_letter, True)
        result_letter = self.FirstRotor.code(result_letter, True)

        result = result_letter
        if self.FirstRotor.pos == 1:
            self.SecondRotor.switch()
        if self.SecondRotor.pos == 1 and self.FirstRotor.pos == 1:
            self.ThirdRotor.switch()
        return result

    def copy_func(self):
        c = Tk()
        c.withdraw()
        c.clipboard_clear()
        c.clipboard_append(self.cipher_text)
        c.update()
        c.destroy()

    def backspace_func(self):
        if len(self.text_box.appended_text) != 0:
            removed = self.text_box.appended_text[-1]
            if removed in string.ascii_letters:
                self.FirstRotor.re_switch()
                if self.FirstRotor.pos == 26:
                    self.SecondRotor.re_switch()
                if self.ThirdRotor.pos == 26:
                    self.ThirdRotor.re_switch()
        text = self.text_box.appended_text[:-1]
        self.text_box.kill()
        self.create_text_box()
        self.text_box.append_html_text(text)
        self.text = self.text[:-1]
        self.cipher_text = self.cipher_text[:-1]
        if self.all_symbols != 0:
            self.all_symbols -= 1

    def trash_func(self):
        for i in self.text_box.appended_text:
            if len(self.text_box.appended_text) != 0:
                if i in string.ascii_letters:
                    self.FirstRotor.re_switch()
                    if self.FirstRotor.pos == 26:
                        self.SecondRotor.re_switch()
                    if self.ThirdRotor.pos == 26:
                        self.ThirdRotor.re_switch()
        self.all_symbols = 0
        self.text_box.kill()
        self.create_text_box()
        self.text = ""
        self.cipher_text = ""

    def hide_func(self):
        if not self.hide_button_activity:
            self.hide_button_activity = True
            self.text_box.kill()
            self.create_text_box()
            self.text_box.append_html_text(self.text)
        else:
            self.hide_button_activity = False
            self.text_box.kill()
            self.create_text_box()
            self.text_box.append_html_text(self.cipher_text)

    def save_func(self):
        i = 1
        save_cycle = True
        while save_cycle:
            if not os.path.exists(f"{self.path}/cipher{i}.txt"):
                with open(f"{self.path}/cipher{i}.txt", "w") as file_obj:
                    file_obj.write(self.cipher_text)
                    file_obj.close()
                    save_cycle = False
            else:
                i += 1

    def draw_rotors(self):
        self.FirstRotor.draw(self.screen)
        self.SecondRotor.draw(self.screen)
        self.ThirdRotor.draw(self.screen)

    def draw(self):
        time_delta = clock.tick(FPS)
        self.screen.blit(self.title, (0, 0))  # title is an image
        self.keyboard.draw()
        self.draw_rotors()
        all_symbols = f2.render(f"{self.all_symbols}/{self.limit}", False, self.limit_color)
        self.screen.blit(all_symbols, self.all_symbols_pos)
        self.manager.draw_ui(self.screen)
        self.button_manager.draw_ui(self.screen)
        if self.hide_button_activity:
            self.screen.blit(self.hide_button_pressed, (self.hide_button.rect.x, self.hide_button.rect.y))
        self.manager.update(time_delta)
        self.button_manager.update(time_delta)
        pygame.display.update()

    def re_transition(self, trns):
        while not trns.transitioning:
            time_delta = clock.tick(FPS)
            self.screen.blit(self.title, (0, 0))  # title is an image
            self.keyboard.draw()
            self.manager.draw_ui(self.screen)
            self.button_manager.draw_ui(self.screen)
            if self.hide_button_activity:
                self.screen.blit(self.hide_button_pressed, (self.hide_button.rect.x, self.hide_button.rect.y))
            self.draw_rotors()
            all_symbols = f2.render(f"{self.all_symbols}/{self.limit}", False, self.limit_color)
            self.screen.blit(all_symbols, self.all_symbols_pos)
            trns.re_update()
            self.screen.blit(trns.image, (0, 0))
            pygame.time.wait(10)
            self.manager.update(time_delta)
            self.button_manager.update(time_delta)
            pygame.display.update()

    def start(self, self_trns):
        play = True
        self.re_transition(self_trns)
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.all_symbols < self.limit:
                        if pygame.key.name(
                                event.key) in string.ascii_letters and event.unicode.lower() == pygame.key.name(
                                event.key):
                            self.all_symbols += 1
                            result = self.cipher(event.unicode)
                            if self.hide_button_activity:
                                self.text_box.append_html_text(event.unicode)
                            else:
                                self.text_box.append_html_text(result)
                            self.text = self.text + event.unicode
                            self.cipher_text = self.cipher_text + result
                            for button in self.keyboard.all_buttons:
                                if button.ltr == result or button.ltr.lower() == result:
                                    button.light = True
                        elif event.key in self.extra:
                            self.all_symbols += 1
                            self.text_box.append_html_text(event.unicode)
                            self.text = self.text + event.unicode
                            self.cipher_text = self.cipher_text + event.unicode
                        elif event.key == pygame.K_TAB:
                            self.all_symbols += 4
                            self.text_box.append_html_text("    ")
                            self.text = self.text + "    "
                            self.cipher_text = self.cipher_text + "    "
                            # self.text_box.html_text = self.text_box.html_text + "    "
                        elif event.key == pygame.K_SPACE:
                            self.all_symbols += 1
                            self.text_box.append_html_text(" ")
                            self.text = self.text + " "
                            self.cipher_text = self.cipher_text + " "
                            # self.text_box.html_text = self.text_box.html_text + " "
                    if event.key == pygame.K_ESCAPE:
                        trns = FadeOutTransition()
                        while trns.transitioning:
                            trns.update()
                            self.screen.blit(trns.image, (0, 0))
                            pygame.time.wait(30)
                            pygame.display.update()
                            clock.tick(FPS)
                        return trns
                    elif event.key == pygame.K_BACKSPACE:
                        self.backspace_func()
                    elif event.key == pygame.K_RETURN:
                        print("Enter")
                if event.type == pygame.KEYUP:
                    for button in self.keyboard.all_buttons:
                        if button.light:
                            button.light = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.hide_button:
                        self.hide_func()
                    if event.ui_element == self.trash_button:
                        self.trash_func()
                    if event.ui_element == self.copy_button:
                        self.copy_func()
                    if event.ui_element == self.save_button:
                        self.save_func()
                    if event.ui_element == self.quite_button:
                        trns = FadeOutTransition()
                        while trns.transitioning:
                            trns.update()
                            self.screen.blit(trns.image, (0, 0))
                            pygame.time.wait(30)
                            pygame.display.update()
                            clock.tick(FPS)
                        return trns

                self.manager.process_events(event)
                self.button_manager.process_events(event)
            self.draw()
