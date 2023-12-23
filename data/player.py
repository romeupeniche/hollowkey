import pygame
import data.helpers.variables as variables


class Player():

    # initializing the player variables
    def __init__(self, animation_list, walls_group):
        self.counter = 0
        self.action = 0
        self.frame = 0
        self.image = animation_list[self.action][self.frame]
        self.animation_list = animation_list
        self.rect = self.image.get_rect()
        self.walls_group = walls_group
        self.sound = pygame.mixer.Sound("data/assets/sfx/player_damage.wav")
        self.sound.set_volume(0.5)
        self.is_sound_playing = False
        self.rect.x = 30
        self.rect.y = 30
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = "RIGHT"
        self.mask = pygame.mask.from_surface(self.image)

        self.level = 1

    # updating player position
    def update(self):
        dx = 0
        dy = 0
        frame_cooldown = 5
        speed = 2
        key = pygame.key.get_pressed()

        # changing player position and its animation based on the pressed key
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.direction = "LEFT"
            dx -= speed
            self.counter += 1
            self.action = 5
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.direction = "RIGHT"
            dx += speed
            self.counter += 1
            self.action = 7
        elif key[pygame.K_UP] or key[pygame.K_w]:
            dy -= speed
            self.counter += 1
            self.direction = "UP"
            self.action = 3
        elif key[pygame.K_DOWN] or key[pygame.K_s]:
            dy += speed
            self.counter += 1
            self.direction = "DOWN"
            self.action = 1
        elif key[pygame.K_f]:
            variables.level = 2

        # if no key is pressed, change the animation to the idle, on the right direction
        elif key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[pygame.K_UP] == False and key[pygame.K_DOWN] == False:
            self.counter = 0
            self.frame = 0
            if self.direction == "LEFT":
                self.action = 4
            elif self.direction == "RIGHT":
                self.action = 6
            elif self.direction == "DOWN":
                self.action = 0
            elif self.direction == "UP":
                self.action = 2

        # handle animation
        if self.counter > frame_cooldown:
            self.counter = 0
            self.frame += 1
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0

        # if level has changed, update player starting position
        if variables.level != self.level:
            self.rect.x = 30
            self.rect.y = 30
            self.level = variables.level

        # if player is colliding with any wall, stop its movement
        for tile in self.walls_group.sprites():
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
        self.rect.x += dx
        self.rect.y += dy

        # then, display on the screen the right frame
        variables.screen.blit(
            self.animation_list[self.action][self.frame], self.rect)

    # if player is colliding with any enemy, decrease its life
    def detect_collision(self, enemies):
        collided_enemies = pygame.sprite.spritecollide(
            self, enemies, False, pygame.sprite.collide_mask)

        for enemy in collided_enemies:
            if not self.is_sound_playing:
                self.sound.play(-1)
                self.is_sound_playing = True
            variables.remaining_life -= 1

            if hasattr(enemy, 'is_red') and enemy.is_red:
                variables.remaining_life -= 2
        if len(collided_enemies) == 0:
            self.sound.stop()
            self.is_sound_playing = False
