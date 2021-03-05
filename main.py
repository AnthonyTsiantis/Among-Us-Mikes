import pygame
from game import *
from spritesheet import *

g = game()

# main game loop
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

