from data.helpers.variables import screen, screen_height, screen_width
from random import randint
from data.helpers.spritesheet import Spritesheet
import pygame


class Enemy(pygame.sprite.Sprite):

    # starting enemy variables
    def __init__(self, sprite_sheet_image, walls_group, is_red=False):
        super().__init__()
        self.counter = 0
        self.action = 0
        self.frame = 0
        sprite_sheet = Spritesheet(sprite_sheet_image)
        step_counter = 0
        animation_steps = [3, 3, 3, 3]
        animation_list = []
        self.is_red = is_red
        self.walls_group = walls_group
        if (is_red):
            self.bullets_hit = 0
        for animation in animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(sprite_sheet.get_image(
                    step_counter, 13, 13, 3, (0, 0, 0)))
                step_counter += 1
            animation_list.append(temp_img_list)

        self.image = animation_list[self.action][self.frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_list = animation_list
        self.rect = self.image.get_rect()
        max_x = int(screen_width / 30) - 2
        max_y = int(screen_height / 30) - 2
        new_x = 30 * randint(1, max_x)
        new_y = 30 * randint(1, max_y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # granting that the enemy will not spawn inside the walls
        while True:
            if (self.check_collision(new_x, new_y)):
                new_x = 30 * randint(1, max_x)
                new_y = 30 * randint(1, max_y)
            else:
                break

        self.rect.x = new_x
        self.rect.y = new_y

    # update enemy's position based on the player position (following)

    def update(self, player_x, player_y):
        dx = 0
        dy = 0
        frame_cooldown = 10
        self.counter += 1

        distancex, distancey = player_x - self.rect.x, player_y - self.rect.y

        # this is to avoid the distance to be zero, as it cannot be divided, to avoid errors
        if distancex == 0:
            distancex = 2
        elif distancey == 0:
            distancey = 2

        distance = (distancex ** 2 + distancey ** 2) ** 0.5
        dx += (distancex / distance) * 1.5
        dy += (distancey / distance) * 1.5

        if abs(dx) > abs(dy):
            self.action = 0 if dx > 0 else 1
        else:
            self.action = 2 if dy > 0 else 3

        # handle animation
        if self.counter > frame_cooldown:
            self.counter = 0
            self.frame += 1
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0

        for tile in self.walls_group.sprites():
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
        self.rect.x += dx
        self.rect.y += dy

        screen.blit(self.animation_list[self.action][self.frame], self.rect)

    # if enemy collided with some bullet, kill it (or decrease its life)
    def detect_collision(self, bullet, bullet_list):
        enemy_size_x, enemy_size_y = self.rect.size
        if (
            self.rect.x < bullet['x'] < self.rect.x + enemy_size_x and
            self.rect.y < bullet['y'] < self.rect.y + enemy_size_y
        ):
            if bullet in bullet_list:
                bullet_list.remove(bullet)
                if (self.is_red):
                    if self.bullets_hit == 2:
                        self.kill()
                    else:
                        self.bullets_hit += 1
                else:
                    self.kill()

    # checking if the enemy is colliding with some wall
    def check_collision(self, new_x, new_y):
        for tile in self.walls_group.sprites():
            if tile.rect.colliderect(new_x, new_y, self.width, self.height):
                return True
        return False
