import pygame
import pygame_gui
import sys
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton
from settings import *
from fonts import f2
from enigma_settings import EnigmaSettings
from enigma import Enigma
from transition import FadeOutTransition

pygame.init()

screen = pygame.display.set_mode((1920, 1080), flags=pygame.SCALED | pygame.RESIZABLE)
# print(screen.get_size())
pygame.display.set_caption("Enigma VCM")
pygame.display.set_icon(pygame.image.load('./graphics/Icon.png'))
clock = pygame.time.Clock()

title = pygame.transform.scale(pygame.image.load('./graphics/Main/1.1.png'), screen.get_size())
image_active = pygame.image.load('./graphics/Buttons/Button_active.png')
image_inactive = pygame.image.load('./graphics/Buttons/Button_inactive.png')


class MainMenu:
    def __init__(self):
        self.transition = FadeOutTransition()
        self.manager = pygame_gui.UIManager((screen.get_size()), './themes/main_menu.json')

        self.enigma_settings = EnigmaSettings(screen)
        self.enigma = Enigma(screen, self.enigma_settings.path, self.enigma_settings.rotors_poss)

        self.version = f2.render(f"Version-{VERSION}", False, WHITE)
        self.by = f2.render(f"Created by {NAME} ", False, WHITE)
        self.created = f2.render("10_07_2023", False, WHITE)
        self.engine = f2.render(f"Engine: {ENGINE}", False, WHITE)

        self.Start_button = UIButton(relative_rect=pygame.Rect((50, 75), (336, 72)),
                                     text="Start",
                                     manager=self.manager,
                                     object_id=ObjectID(class_id="button"))
        self.Patch_panel_button = UIButton(relative_rect=pygame.Rect((50, 175), (336, 72)),
                                           text="Patch panel",
                                           manager=self.manager,
                                           object_id=ObjectID(class_id="button"))
        self.Settings_button = UIButton(relative_rect=pygame.Rect((50, 275), (336, 72)),
                                        text="Settings",
                                        manager=self.manager,
                                        object_id=ObjectID(class_id="button"))
        self.Instruction_button = UIButton(relative_rect=pygame.Rect((50, 375), (336, 72)),
                                           text="Instruction",
                                           manager=self.manager,
                                           object_id=ObjectID(class_id="button"))
        self.Quite_button = UIButton(relative_rect=pygame.Rect((50, 900), (336, 72)),
                                     text="Quite",
                                     manager=self.manager,
                                     object_id=ObjectID(class_id="button"))
        self.Instruction_button.disable()
        self.Patch_panel_button.disable()

    def settings_func(self):
        self.transitioning()
        output = self.enigma_settings.start(self.transition)
        self.transition = next(output)
        output_path = next(output)
        rotors_poss = next(output)
        new_settings = next(output)
        if new_settings:
            self.enigma = Enigma(screen, output_path, rotors_poss)
        self.re_transitioning()

    def render(self):
        screen.blit(self.by, (980, 800))
        screen.blit(self.created, (980, 850))
        screen.blit(self.engine, (980, 900))
        screen.blit(self.version, (980, 950))

    def re_transitioning(self):
        while not self.transition.transitioning:
            time_delta = clock.tick(FPS)
            title_text = screen.blit(title, (0, 0))  # title is an image
            title_text.center = ((1920 / 2), (1080 / 2))
            self.render()
            self.manager.draw_ui(screen)

            self.transition.re_update()
            screen.blit(self.transition.image, (0, 0))

            pygame.time.wait(10)
            self.manager.update(time_delta)
            pygame.display.update()

    def transitioning(self):
        while self.transition.transitioning:
            self.transition.update()
            screen.blit(self.transition.image, (0, 0))

            pygame.time.wait(30)
            pygame.display.update()
            clock.tick(FPS)

    def draw(self):
        time_delta = clock.tick(FPS)
        screen.fill(BLACK)

        title_text = screen.blit(title, (0, 0))  # title is an image
        title_text.center = ((1920 / 2), (1080 / 2))
        self.render()
        self.manager.draw_ui(screen)

        self.manager.update(time_delta)
        pygame.display.update()

    def start(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.Start_button:
                        self.transitioning()
                        self.transition = self.enigma.start(self.transition)
                        self.re_transitioning()
                    elif event.ui_element == self.Settings_button:
                        self.settings_func()
                    elif event.ui_element == self.Quite_button:
                        pygame.quit()
                        sys.exit()

                self.manager.process_events(event)
            self.draw()


main = MainMenu()
main.start()
