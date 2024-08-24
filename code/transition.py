import pygame
from pygame.sprite import Sprite


class FadeOutTransition(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = pygame.display.get_window_size()
        self.image = pygame.Surface((self.width, self.height * 1.5)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.alpha = 0
        self.image.fill((0, 0, 0, self.alpha))
        self.transitioning = True

    def update(self):
        self.check_for_transition_complete()
        self.image.fill((0, 0, 0, self.alpha))
        if self.alpha <= 240:
            self.alpha += 10

    def check_for_transition_complete(self):
        if self.alpha > 240:
            self.transitioning = False

    def re_update(self):
        self.re_check_for_transition_complete()
        self.image.fill((0, 0, 0, self.alpha))
        if self.alpha > 0:
            self.alpha -= 25

    def re_check_for_transition_complete(self):
        if self.alpha <= 0:
            self.transitioning = True

    def is_transitioning(self):
        return self.transitioning