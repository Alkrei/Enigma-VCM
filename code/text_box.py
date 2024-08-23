from fonts import f2
from settings import *
import pygame


class TextBox(object):
    def __init__(self, x, y):
        self.y_axis = 0
        self.change_y = 0

        # box
        self.box = pygame.Surface([600, 251], pygame.SRCALPHA)
        self.height = self.box.get_height()
        self.box_height = self.box.get_height() - 1
        self.box_width = self.box.get_width()
        self.x = x
        self.y = y

        # text
        self.text = [""]
        self.cipher_text = [""]
        self.current_line = 0
        self.hide_button_activity = False

        # bar
        bar_height = int((self.box_height - 40) / (self.height  / (self.box_height * 1.0)))
        self.bar_rect = pygame.Rect(self.box_width - 20, 20, 20, bar_height)
        self.bar_up = pygame.Rect(self.box_width - 20, 0, 20, 20)
        self.bar_down = pygame.Rect(self.box_width - 20, self.box_height - 20, 20, 20)

        self.up_inactive = pygame.image.load('./graphics/Buttons/Up_inactive.png').convert()
        self.down_inactive = pygame.image.load('./graphics/Buttons/Down_inactive.png').convert()
        self.up_active = pygame.image.load('./graphics/Buttons/Up_active.png').convert()
        self.down_active = pygame.image.load('./graphics/Buttons/Down_active.png').convert()

        self.up_image = self.up_inactive
        self.down_image = self.down_inactive

        self.on_bar = False
        self.mouse_diff = 0

    def update(self, surface, screen):
        self.y_axis += self.change_y

        # top and bottom
        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.height) < self.box_height:
            self.y_axis = self.box_height - self.height

        height_diff = self.height - self.box_height

        scroll_length = self.box_height - self.bar_rect.height - 40
        bar_half_lenght = self.bar_rect.height / 2 + 20

        if self.on_bar:
            pos = list(pygame.mouse.get_pos())
            pos[0] = ((pos[0] * surface.get_width()) / screen.get_width()) - 660
            pos[1] = ((pos[1] * surface.get_height()) / screen.get_height()) - 77
            pos = tuple(pos)
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (self.box_height - 20):
                self.bar_rect.bottom = self.box_height - 20
            self.y_axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
        else:
            self.bar_rect.centery = scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght

    def update_text(self, text, cipher_text):
        self.text[self.current_line] = self.text[self.current_line] + text
        self.cipher_text[self.current_line] = self.cipher_text[self.current_line] + cipher_text

    def backspace(self):
        self.text[-1] = self.text[-1][:-1]
        if len(self.text[-1]) == 0:
            if len(self.text) > 1:
                self.text = self.text[:-1]
                self.current_line -= 1
        self.cipher_text[-1] = self.cipher_text[-1][:-1]
        if len(self.cipher_text[-1]) == 0:
            if len(self.cipher_text) > 1:
                self.cipher_text = self.cipher_text[:-1]
                self.current_line -= 1

    def enter(self):
        self.text.append("")
        self.cipher_text.append("")
        self.current_line += 1
        if (self.current_line + 1) * f2.get_height() >= self.height:
            self.height += f2.get_height()
            bar_height = int((self.box_height - 40) / (self.height / (self.box_height * 1.0)))
            self.bar_rect = pygame.Rect(self.box_width - 20, 20, 20, bar_height)

    def trash(self):
        self.text = [""]
        self.cipher_text = [""]
        self.current_line = 0

    def y_change_event(self, count):
        self.change_y = count

    def mouse_button_down(self, surface, screen):
        pos = list(pygame.mouse.get_pos())
        pos[0] = ((pos[0] * surface.get_width()) / screen.get_width()) - 660
        pos[1] = ((pos[1] * surface.get_height()) / screen.get_height()) - 77
        pos = tuple(pos)
        if self.bar_rect.collidepoint(pos):
            self.mouse_diff = pos[1] - self.bar_rect.y
            self.on_bar = True
        elif self.bar_up.collidepoint(pos):
            self.change_y = 5
            self.up_image = self.up_inactive
        elif self.bar_down.collidepoint(pos):
            self.change_y = -5
            self.down_image = self.down_inactive

    def mouse_button_up(self):
        self.change_y = 0
        self.on_bar = False

    def mouse(self, surface, screen):
        pos = list(pygame.mouse.get_pos())
        pos[0] = ((pos[0] * surface.get_width()) / screen.get_width()) - 660
        pos[1] = ((pos[1] * surface.get_height()) / screen.get_height()) - 77
        pos = tuple(pos)
        if self.bar_up.collidepoint(pos):
            self.up_image = self.up_active
        else:
            self.up_image = self.up_inactive

        if self.bar_down.collidepoint(pos):
            self.down_image = self.down_active
        else:
            self.down_image = self.down_inactive

    def display_text(self, text):
        for row, line in enumerate(text):
            rendered_text = f2.render(line, False, (0, 0, 0))
            if rendered_text.get_width() + 32 >= self.box_width - 32 and row == self.current_line:
                self.text.append("")
                self.cipher_text.append("")
                self.current_line += 1
                if (self.current_line + 1) * f2.get_height()  >= self.height:
                    self.height += f2.get_height()
                    bar_height = int((self.box_height - 40) / (self.height / (self.box_height * 1.0)))
                    self.bar_rect = pygame.Rect(self.box_width - 20, 20, 20, bar_height)
            self.box.blit(rendered_text, (10, f2.get_height() * row * 0.75 + self.y_axis))

    def draw(self, screen):
        self.box.fill(PAPER)
        pygame.draw.rect(self.box, BORDERGRAY, self.bar_rect)

        self.box.blit(self.up_image, (self.box_width - 20, 0))
        self.box.blit(self.down_image, (self.box_width - 20, self.box_height - 20))
        if self.hide_button_activity:
            self.display_text(self.text)
        elif not self.hide_button_activity:
            self.display_text(self.cipher_text)
        screen.blit(self.box, (self.x, self.y))