import pygame

# setting some variables that are going to be used in many files

screen_width = 750
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))

got_key = False
level = 1
bullets_left = 4
got_bullets = False
remaining_life = 500
full_life = 500
menu_state = "main"
game_paused = True
