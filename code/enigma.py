import pygame
import copykitten
import sys
import os
from settings import *
from fonts import f2
from rotor import Rotor
from reflector import Reflector
from text_box import TextBox
from buttons import Button
from keyboard import Keyboard
from lang import en_kb, en_ascii
from transition import FadeOutTransition

clock = pygame.time.Clock()

class Enigma:
    def __init__(self, surface, screen, path, rotors_poss):
        self.surface = surface
        self.screen = screen
        self.title = pygame.image.load('./graphics/Enigma/Enigma_VCM.png')
        self.quite = False

        # text
        self.ascii = en_ascii
        self.all_symbols = 0
        self.limit = 1000
        self.limit_color = BLACK
        self.all_symbols_pos = (909, 430)
        self.text = ""

        self.path = path

        # filling
        """self.d_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]
        self.d_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]
        self.d_3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0]"""
        self.d_1 = [5, 14, 21, 2, 22, 15, 16, 18, 9, 20, 7, 12, 1, 11, 8, 0, 13, 10, 19, 17, 4, 3, 24, 25, 6, 23]
        self.d_2 = [9, 19, 23, 12, 4, 16, 22, 2, 15, 1, 20, 5, 17, 10, 21, 18, 25, 11, 0, 13, 7, 24, 14, 8, 3, 6]
        self.d_3 = [25, 9, 3, 5, 15, 6, 23, 20, 0, 2, 22, 1, 24, 18, 17, 10, 16, 8, 11, 19, 21, 14, 12, 7, 4, 13]
        self.ref_d = [(1, 22), (2, 16), (3, 21), (4, 14), (5, 24), (6, 23), (7, 20), (8, 18), (9, 17), (10, 15),
                      (11, 25), (12, 19), (13, 26)]

        # buttons
        self.HideButton = Button(1327, 95, 84, 84, './graphics/Buttons/Hide_Button_inactive.png',
                                  './graphics/Buttons/Hide_Button_active.png', f2, action=lambda: self.hide_func())
        self.TrashButton = Button(1327, 226, 84, 84, './graphics/Buttons/Trash_Button_inactive.png',
                                  './graphics/Buttons/Trash_Button_active.png', f2, action=lambda: self.trash_func())
        self.CopyButton = Button(1458, 95, 84, 84, './graphics/Buttons/Copy_Button_inactive.png',
                                   './graphics/Buttons/Copy_Button_active.png', f2, action=lambda: self.copy_func())
        self.SaveButton = Button(1458, 226, 84, 84, './graphics/Buttons/Save_Button_inactive.png',
                                  './graphics/Buttons/Save_Button_active.png', f2, action=lambda: self.save_func())
        self.QuiteButton = Button(100, 550, 84, 84, './graphics/Buttons/Quite_Button_inactive.png',
                                  './graphics/Buttons/Quite_Button_active.png', f2, action=lambda: self.quite_func())
        self.hide_button_pressed = pygame.image.load("./graphics/Buttons/Hide_Button_pressed.png")

        # Elements
        self.Keyboard = Keyboard(en_kb, self.surface)
        self.FirstRotor = Rotor(rotors_poss[2], self.d_1, (390, 74))
        self.SecondRotor = Rotor(rotors_poss[1], self.d_2, (246, 74))
        self.ThirdRotor = Rotor(rotors_poss[0], self.d_3, (102, 74))
        self.Reflector = Reflector(self.ref_d)
        self.TextBox = TextBox(660, 77)

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
        text = ''
        for line in self.TextBox.cipher_text:
            text = text + line + '\n'
        copykitten.copy(text)

    def trash_func(self):
        for i in self.text:
            if len(self.text) != 0:
                if i in self.ascii:
                    self.FirstRotor.re_switch()
                    if self.FirstRotor.pos == 26:
                        self.SecondRotor.re_switch()
                    if self.ThirdRotor.pos == 26:
                        self.ThirdRotor.re_switch()
        self.all_symbols = 0
        self.TextBox.trash()
        self.text = ""

    def hide_func(self):
        if not self.TextBox.hide_button_activity:
            self.TextBox.hide_button_activity = True
        elif self.TextBox.hide_button_activity:
            self.TextBox.hide_button_activity = False

    def save_func(self):
        if self.path != "" and os.path.exists(self.path):
            i = 1
            save_cycle = True
            while save_cycle:
                if not os.path.exists(f"{self.path}/cipher_{i}.txt"):
                    with open(f"{self.path}/cipher_{i}.txt", "w") as file_obj:
                        for line in self.TextBox.cipher_text:
                            file_obj.write(line + '\n')
                        file_obj.close()
                        save_cycle = False
                else:
                    i += 1
        else:
            pass

    def quite_func(self):
        self.quite = True

    def print_tab(self):
        self.all_symbols += 4
        self.TextBox.update_text("    ", "    ")
        self.text = self.text + "    "

    def print_text(self, event):
        if event.text.lower() in self.ascii:
            self.all_symbols += 1
            result = self.cipher(event.text)
            self.TextBox.update_text(event.text, result)
            self.text = self.text + event.text
            for button in self.Keyboard.all_buttons:
                if button.ltr == result or button.ltr.lower() == result:
                    button.light = True
        else:
            self.all_symbols += 1
            self.TextBox.update_text(event.text, event.text)
            self.text = self.text + event.text

    def print_backspace(self):
        if len(self.text) != 0:
            removed = self.text[-1]
            if removed in self.ascii:
                self.FirstRotor.re_switch()
                if self.FirstRotor.pos == 26:
                    self.SecondRotor.re_switch()
                if self.ThirdRotor.pos == 26:
                    self.ThirdRotor.re_switch()
        self.TextBox.backspace()
        self.text = self.text[:-1]
        if self.all_symbols != 0:
            self.all_symbols -= 1

    def re_transition(self, trns):
        self.quite = False
        while not trns.transitioning:
            self.surface.blit(self.title, (0, 0))  # title is an image
            self.Keyboard.draw()
            self.draw_rotors()
            self.draw_buttons()
            self.TextBox.draw(self.surface)
            all_symbols = f2.render(f"{self.all_symbols}/{self.limit}", False, self.limit_color)
            self.surface.blit(all_symbols, self.all_symbols_pos)
            if self.TextBox.hide_button_activity:
                self.surface.blit(self.hide_button_pressed, (self.HideButton.x, self.HideButton.y))
            self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
            trns.re_update()
            self.screen.blit(trns.image, (0, 0))
            pygame.time.wait(10)
            pygame.display.update()

    def draw_rotors(self):
        self.FirstRotor.draw(self.surface)
        self.SecondRotor.draw(self.surface)
        self.ThirdRotor.draw(self.surface)

    def draw_buttons(self):
        self.HideButton.button(self.surface, self.screen)
        self.TrashButton.button(self.surface, self.screen)
        self.CopyButton.button(self.surface, self.screen)
        self.SaveButton.button(self.surface, self.screen)
        self.QuiteButton.button(self.surface, self.screen)

    def draw(self):
        self.surface.blit(self.title, (0, 0))  # title is an image
        self.Keyboard.draw()
        self.draw_rotors()
        self.draw_buttons()
        self.TextBox.draw(self.surface)
        all_symbols = f2.render(f"{self.all_symbols}/{self.limit}", False, self.limit_color)
        self.surface.blit(all_symbols, self.all_symbols_pos)
        if self.TextBox.hide_button_activity:
            self.surface.blit(self.hide_button_pressed, (self.HideButton.x, self.HideButton.y))
        self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
        pygame.display.update()

    def start(self, self_trns):
        play = True
        self.re_transition(self_trns)
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.TEXTINPUT:
                    self.print_text(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quite_func()
                    elif event.key == pygame.K_BACKSPACE:
                        self.print_backspace()
                    elif event.key == pygame.K_TAB:
                        self.print_tab()
                    elif event.key == pygame.K_RETURN:
                        self.TextBox.enter()
                    elif event.key == pygame.K_UP:
                        self.TextBox.y_change_event(5)
                    elif event.key == pygame.K_DOWN:
                        self.TextBox.y_change_event(-5)

                if event.type == pygame.KEYUP:
                    for button in self.Keyboard.all_buttons:
                        if button.light:
                            button.light = False
                    if event.key == pygame.K_UP:
                        self.TextBox.y_change_event(0)
                    elif event.key == pygame.K_DOWN:
                        self.TextBox.y_change_event(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.TextBox.mouse_button_down(self.surface, self.screen)
                else:
                    self.TextBox.mouse(self.surface, self.screen)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.TextBox.mouse_button_up()

            self.TextBox.update(self.surface, self.screen)
            self.draw()
            if self.quite:
                trns = FadeOutTransition()
                while trns.transitioning:
                    trns.update()
                    self.screen.blit(pygame.transform.scale(self.surface, self.screen.get_rect().size), (0, 0))
                    self.screen.blit(trns.image, (0, 0))
                    pygame.time.wait(30)
                    pygame.display.update()
                    clock.tick(FPS)
                return trns