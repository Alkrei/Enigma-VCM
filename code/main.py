from importlib.metadata import version

import pygame
import sys
from settings import *
from fonts import f2, f3
from enigma_settings import EnigmaSettings
from enigma import Enigma
from transition import FadeOutTransition
from buttons import Button

pygame.init()

surface = pygame.surface.Surface((1920,1011))
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygame.display.set_caption("Enigma VCM")
pygame.display.set_icon(pygame.image.load('./graphics/Icon.png'))
clock = pygame.time.Clock()

title = pygame.transform.scale(pygame.image.load(f'./graphics/Main/{VERSION}.png'), surface.get_size())

class MainMenu:
    def __init__(self):
        self.transition = FadeOutTransition()

        # Enigma VCM
        self.EnigmaSettings = EnigmaSettings(surface, screen)
        self.Enigma = Enigma(surface, screen, self.EnigmaSettings.path, self.EnigmaSettings.rotors_poss)

        # Info
        self.version = f2.render(f"Version-{VERSION}", False, WHITE)
        self.by = f2.render(f"Created by {NAME} ", False, WHITE)
        self.created = f2.render("10.07.2023", False, WHITE)
        self.engine = f2.render(f"Engine: {ENGINE}", False, WHITE)

        # buttons
        self.image_active = './graphics/Buttons/Button_active.png'
        self.image_inactive = './graphics/Buttons/Button_inactive.png'

        self.StartButton = Button(50, 75, 336, 72, self.image_inactive, self.image_active, f3, "Start", lambda: self.start_func())
        self.PathPanelButton = Button(50, 175, 336, 72, self.image_inactive, self.image_active, f3, "Patch Panel")
        self.SettingsButton = Button(50, 275, 336, 72, self.image_inactive, self.image_active, f3, "Settings", lambda: self.settings_func())
        self.InstructionButton = Button(50, 375, 336, 72, self.image_inactive, self.image_active, f3, "Instruction")
        self.QuiteButton = Button(50, 900, 336, 72, self.image_inactive, self.image_active, f3, "Quite", lambda: self.quite_func())

    def settings_func(self):
        self.transitioning()
        output = self.EnigmaSettings.start(self.transition)
        self.transition = next(output)
        output_path = next(output)
        rotors_poss = next(output)
        new_settings = next(output)
        if new_settings:
            self.Enigma = Enigma(surface, screen, self.EnigmaSettings.path, self.EnigmaSettings.rotors_poss)
        self.re_transitioning()

    def start_func(self):
        self.transitioning()
        self.transition = self.Enigma.start(self.transition)
        self.re_transitioning()

    def quite_func(self):
        pygame.quit()
        sys.exit()

    def render_info(self):
        surface.blit(self.by, (980, 800))
        surface.blit(self.created, (980, 850))
        surface.blit(self.engine, (980, 900))
        surface.blit(self.version, (980, 950))

    def re_transitioning(self):
        while not self.transition.transitioning:
            title_text = surface.blit(title, (0, 0))  # title is an image
            title_text.center = ((1920 / 2), (1080 / 2))
            self.render_info()
            screen.blit(pygame.transform.scale(surface, screen.get_rect().size), (0, 0))
            self.transition.re_update()
            screen.blit(self.transition.image, (0, 0))
            pygame.time.wait(10)
            pygame.display.update()

    def transitioning(self):
        self.render_info()
        while self.transition.transitioning:
            self.transition.update()
            screen.blit(pygame.transform.scale(surface, screen.get_rect().size), (0, 0))
            screen.blit(self.transition.image, (0, 0))
            pygame.time.wait(30)
            pygame.display.update()
            clock.tick(FPS)

    def draw_buttons(self):
        self.QuiteButton.button(surface, screen)
        self.StartButton.button(surface, screen)
        self.PathPanelButton.button(surface, screen)
        self.SettingsButton.button(surface, screen)
        self.InstructionButton.button(surface, screen)

    def draw(self):
        surface.fill(BLACK)
        title_text = surface.blit(title, (0, 0))  # title is an image
        title_text.center = ((1920 / 2), (1080 / 2))
        self.draw_buttons()
        self.render_info()
        screen.blit(pygame.transform.scale(surface, screen.get_rect().size), (0, 0))
        pygame.display.update()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quite_func()
            self.draw()

main = MainMenu()
main.start()