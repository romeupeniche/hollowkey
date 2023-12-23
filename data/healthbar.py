import pygame
import data.helpers.variables as variables

# health bar displayed on the header


class HealthBar():
    def __init__(self):
        self.x = 40
        self.y = 15
        self.w = 200
        self.h = 20
        self.hp = variables.full_life
        self.max_hp = variables.full_life

    def draw(self):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(variables.screen, "red",
                         (self.x, self.y, self.w, self.h))
        pygame.draw.rect(variables.screen, "green",
                         (self.x, self.y, self.w * ratio, self.h))
