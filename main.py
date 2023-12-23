import pygame
import sys
import data.helpers.spritesheet as spritesheet
from data.player import Player
from data.enemy import Enemy
from data.interactive import Interactive
from pytmx.util_pygame import load_pygame
from data.helpers.variables import screen, screen_height, screen_width
import data.helpers.variables as variables
import random
from data.helpers.tile import Tile
from data.healthbar import HealthBar
from data.crosshair import Crosshair
import data.helpers.button as button

# main game file, run this to run the game


def play_sound(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)


# playing background music
play_sound("data/assets/sfx/background.wav")

pygame.init()
pygame.display.set_caption("Hollow Key")

# setting player animation
sprite_sheet_image = pygame.image.load(
    "data/assets/spritesheets/player_spritesheet.png").convert_alpha()
sprite_sheet = spritesheet.Spritesheet(sprite_sheet_image)
animation_list = []
animation_steps = [1, 3, 1, 3, 1, 3, 1, 3]
step_counter = 0

# group for later collision check
walls_group = pygame.sprite.Group()

# setting fps
clock = pygame.time.Clock()

# Loading slimes spritesheets for animation
green_slime_image = pygame.image.load(
    "data/assets/spritesheets/green_slime_spritesheet.png").convert_alpha()
blue_slime_image = pygame.image.load(
    "data/assets/spritesheets/blue_slime_spritesheet.png").convert_alpha()
yellow_slime_image = pygame.image.load(
    "data/assets/spritesheets/yellow_slime_spritesheet.png").convert_alpha()
red_slime_image = pygame.image.load(
    "data/assets/spritesheets/red_slime_spritesheet.png").convert_alpha()


# animating player movement
for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(
            step_counter, 16, 19, 2, (0, 0, 0)))
        step_counter += 1
    animation_list.append(temp_img_list)

# initializing player, and passing the needed parameters
player = Player(animation_list, walls_group)

# initializing enemies group
enemies = pygame.sprite.Group()

# health bar for the header
health_bar = HealthBar()

# crosshair for shooting
crosshair = Crosshair()
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# initializing interactive objects
stairs = Interactive("stair")
key = Interactive("key")
extra_bullets = Interactive("bullets")

# bullet list to display on the screen later
bullet_list = []

# initializing fonts
font = pygame.font.SysFont('Comic Sans MS', 25, True)
large_font = pygame.font.SysFont(
    'Comic Sans MS', 60, True)  # just changed size

# setting the light image (lantern like effect)
light = pygame.image.load('data/assets/objects/light.png')


# setting scoped variables
_level = 0  # to indicate if the level changed
menu_state_helper = "main"  # to help display the proper screen
run = True  # to make the game run
slime_img_list = [green_slime_image,
                  # to get random slimes (all the available slimes)
                  blue_slime_image, yellow_slime_image, "red"]

# setting all the needed images

header_img = pygame.image.load("data/assets/objects/header.png")
heart_img = pygame.image.load("data/assets/objects/heart.png")
ground_surf = pygame.image.load(
    "data/assets/menus/ground.png").convert_alpha()
resume_img = pygame.image.load(
    "data/assets/buttons/resume_button.png").convert_alpha()
restart_img = pygame.image.load(
    "data/assets/buttons/restart_button.png").convert_alpha()
help_img = pygame.image.load(
    "data/assets/buttons/help_button.png").convert_alpha()
quit_img = pygame.image.load(
    "data/assets/buttons/quit_button.png").convert_alpha()
start_img = pygame.image.load(
    "data/assets/buttons/start_button.png").convert_alpha()
back_img = pygame.image.load(
    "data/assets/buttons/back_button.png").convert_alpha()
about_img = pygame.image.load(
    "data/assets/buttons/about_button.png").convert_alpha()
about_menu_img = pygame.image.load(
    "data/assets/menus/about_menu.jpg").convert_alpha()
help_menu_img = pygame.image.load(
    "data/assets/menus/help_menu.png").convert_alpha()
main_menu_img = pygame.image.load(
    "data/assets/menus/main_menu.jpg").convert_alpha()
lose_screen_img = pygame.image.load(
    "data/assets/menus/lose_screen.jpg").convert_alpha()
win_screen_img = pygame.image.load(
    "data/assets/menus/win_screen.png").convert_alpha()

# setting all the buttons

resume_button = button.Button(280, 175, resume_img, 1)
restart_button = button.Button(270, 360, restart_img, 1)
start_button = button.Button(275, 250, start_img, 1)
help_button = button.Button(312, 300, help_img, 1)
quit_button = button.Button(312, 425, quit_img, 1)
back_button = button.Button(10, 20, back_img, 1)
about_button = button.Button(275, 350, about_img, 1)

# setting ground image rect (to display on the screen)
ground_rect = ground_surf.get_rect(topleft=(0, 0))

# setting functions


def update_level_walls():
    global _level
    walls_group.empty()
    tmx_data = load_pygame(
        f"data/assets/level_maps/level{variables.level}.tmx")
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():

                # (30) = height of tile, (30) = width of tile
                pos = (x * 30, y * 30)
                Tile(pos=pos, surf=surf, groups=walls_group)
    _level += 1


def lantern_filter():
    filter = pygame.surface.Surface((screen_width, screen_height))
    filter.fill(pygame.Color(255, 255, 255))
    filter.blit(light, (player.rect.center[0] - light.get_width() //
                2, player.rect.center[1] - light.get_height() // 2))
    screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)


def update_header():
    screen.blit(header_img, (0, 0))
    health_bar.hp = variables.remaining_life
    health_bar.draw()
    screen.blit(heart_img, (20, 5))
    bullets_left_text = font.render(
        f"{variables.bullets_left}", True, (108, 73, 56))
    level = font.render(
        f"{variables.level}", True, (108, 73, 56))
    screen.blit(bullets_left_text, (320, 9))
    screen.blit(level, (423, 8))


def restart_game():
    global _level, menu_state_helper
    variables.got_key = False
    variables.level = 1
    variables.bullets_left = 4
    variables.got_bullets = False
    variables.remaining_life = 500
    variables.full_life = 500
    variables.menu_state = "main"
    player.rect.topleft = (30, 30)
    variables.game_paused = False
    _level = 0
    menu_state_helper = "main"


# main game loop
while run:

    # checking for events
    for event in pygame.event.get():
        # quitting (closing the window)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # shooting
        elif event.type == pygame.MOUSEBUTTONDOWN and not variables.game_paused:
            crosshair.shoot(bullet_list, player)

        # esc pauses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                variables.game_paused = True

    # checking if the game is won
    if variables.level == 6:
        variables.game_paused = True
        variables.menu_state = "win"

    # displaying all the screens, but the game
    if variables.game_paused:
        screen.fill((73, 44, 29))
        pygame.mouse.set_visible(True)

        # granting that the player hurting sound wont play if the game is paused (even though it is colliding)
        player.sound.stop()
        player.is_sound_playing = False

        # Pause screen
        if variables.menu_state == "pause":
            help_button.rect.y = 300
            quit_button.rect.y = 425
            if resume_button.draw(screen):
                variables.game_paused = False
            if help_button.draw(screen):
                variables.menu_state = "help"
            if quit_button.draw(screen):
                run = False

        # Help screen
        elif variables.menu_state == "help":
            screen.blit(help_menu_img, (0, 0))
            if back_button.draw(screen):
                variables.menu_state = menu_state_helper

        # About screen
        elif variables.menu_state == "about":
            screen.blit(about_menu_img, (0, 0))
            if back_button.draw(screen):
                variables.menu_state = menu_state_helper

        # Main menu screen
        elif variables.menu_state == "main":
            help_button.rect.y = 450
            quit_button.rect.y = 550
            screen.blit(main_menu_img, (0, 0))
            if quit_button.draw(screen):
                run = False
            if start_button.draw(screen):
                variables.game_paused = False
                variables.menu_state = "pause"
                menu_state_helper = "pause"
            if help_button.draw(screen):
                variables.menu_state = "help"
            if about_button.draw(screen):
                variables.menu_state = "about"

        # Lose screen
        elif variables.menu_state == "lose":
            screen.blit(lose_screen_img, (0, 0))
            last_floor_txt = large_font.render(
                f"{variables.level}", True, (108, 73, 56))
            screen.blit(last_floor_txt, (350, 240))
            quit_button.rect.y = 460
            if restart_button.draw(screen):
                restart_game()
            if quit_button.draw(screen):
                run = False

        # Win screen
        elif variables.menu_state == "win":
            screen.blit(win_screen_img, (0, 0))
            if restart_button.draw(screen):
                restart_game()
            if quit_button.draw(screen):
                run = False

    else:  # game is running

        pygame.mouse.set_visible(False)

        # change level walls and enemies
        if _level != variables.level:
            update_level_walls()
            enemies.empty()
            enemies_qty = variables.level + 2

            # getting random slimes
            for _ in range(enemies_qty):
                slime_img_idx = random.randint(0, len(slime_img_list) - 1)
                slime_img = slime_img_list[slime_img_idx]
                if slime_img == "red":
                    enemies.add(Enemy(red_slime_image, walls_group, True))
                else:
                    enemies.add(Enemy(slime_img, walls_group))

            enemies.add(Enemy(red_slime_image, walls_group, True))

        if _level == variables.level:  # level did not change

            # displaying ground img
            screen.blit(ground_surf, ground_rect)

            # displaying walls
            walls_group.draw(screen)

            # displaying all interactive objects
            stairs.update(player, walls_group)
            key.update(player, walls_group)
            extra_bullets.update(player, walls_group)

            # showing the bullet path
            for bullet in bullet_list:
                pygame.draw.circle(screen, (102, 51, 153), (int(
                    bullet['x']), int(bullet['y'])), 5)
                for enemy in enemies:
                    enemy.detect_collision(bullet, bullet_list)
                for tile in walls_group.sprites():
                    if tile.rect.colliderect(bullet['x'], bullet['y'], 5, 5):
                        if bullet in bullet_list:
                            bullet_list.remove(bullet)

            # updating the enemies position based on the player position
            enemies.update(player.rect.x, player.rect.y)

            # Lantern
            lantern_filter()

            # checking if the player is dead
            if variables.remaining_life <= 0:
                variables.menu_state = "lose"
                variables.game_paused = True

            # updating header (life, floor and bullets)
            update_header()

            # updating the crosshair position based on the mouse
            crosshair_group.update()
            crosshair_group.draw(screen)

            # updating the bullet position
            for bullet in bullet_list:
                bullet['x'] += bullet['dx']
                bullet['y'] += bullet['dy']

            # checking if the player is colliding with any enemy
            player.detect_collision(enemies)

            # updating player position
            player.update()

    # updating the screen
    pygame.display.update()

    # FPS
    clock.tick(60)
