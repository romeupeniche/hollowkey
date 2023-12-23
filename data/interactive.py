import pygame
from data.helpers.variables import screen, screen_height, screen_width
from random import randint
import data.helpers.variables as variables


class Interactive():

    # initializing variables
    def __init__(self, type):
        self.walls_group = []
        self.sound = pygame.mixer.Sound(
            f"data/assets/sfx/{type}.wav")
        self.image = pygame.image.load(
            f"data/assets/objects/{type}.png")

        self.sound.set_volume(0.1)
        if (type == "key"):  # the key sound is a little too low - need to adjust the volume for it
            self.sound.set_volume(0.3)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.type = type
        self.walls_group_length = 0
        self.got_bullets = False

    # update object's new position
    def update(self, playerrect, walls_group):
        self.walls_group = walls_group

        # checking if the level has changed, therefore the walls had changed as well
        if len(self.walls_group) != self.walls_group_length:
            self.spawn_position(walls_group)
            self.walls_group_length = len(self.walls_group)

        # checking the types and its own functions
        if self.type == "bullets":
            if self.rect.colliderect(playerrect) and not variables.got_bullets:
                self.sound.play()
                variables.got_bullets = True
                _bullets = randint(1, 4)
                variables.bullets_left += _bullets
            else:
                if not variables.got_bullets:
                    screen.blit(self.image, self.rect)
        else:
            if (variables.got_key and self.type == "stair") or (not variables.got_key and self.type == "key"):
                if self.rect.colliderect(playerrect):
                    self.sound.play()
                    if variables.got_key and self.type == "stair":
                        variables.level += 1
                        variables.got_bullets = False

                    variables.got_key = not variables.got_key
                else:
                    screen.blit(self.image, self.rect)

    # getting a new position
    def spawn_position(self, walls_group):
        max_x = int(screen_width / 30) - 2
        max_y = int(screen_height / 30) - 2

        checking = True

        # loop to check if the object is inside any wall
        while checking:
            detected = False
            new_x = 30 * randint(1, max_x)
            new_y = 30 * randint(1, max_y)

            self.rect.topleft = (new_x, new_y)

            for wall in walls_group.sprites():
                if self.rect.colliderect(wall.rect):
                    detected = True
            if not detected:
                break
            else:
                continue
