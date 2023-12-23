import pygame
import data.helpers.variables as variables
import math

# crosshair for shooting


class Crosshair(pygame.sprite.Sprite):

    # setting all the variables
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/assets/objects/crosshair.png")
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound("data/assets/sfx/gunshot.wav")
        self.empty_gunshot = pygame.mixer.Sound(
            "data/assets/sfx/empty_gunshot.wav")
        self.gunshot.set_volume(0.04)
        self.empty_gunshot.set_volume(0.06)
        self.bullet_speed = 16

    # shooting function
    def shoot(self, bullet_list, player):

        # if it has bullets left, play the sound and get the correct bullet position
        if variables.bullets_left > 0:
            self.gunshot.play()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_size_x, player_size_y = player.rect.size
            angle = math.atan2(mouse_y - (player.rect.y + player_size_y/2),
                               mouse_x - (player.rect.x + player_size_x/2))
            variables.bullets_left -= 1
            bullet_list.append({
                'x': player.rect.x + player_size_x/2,
                'y': player.rect.y + player_size_y/2,
                'dx': self.bullet_speed * math.cos(angle),
                'dy': self.bullet_speed * math.sin(angle)
            })

        # if there is no bullet left
        else:
            self.empty_gunshot.play()

    # update its position to track the mouse
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
