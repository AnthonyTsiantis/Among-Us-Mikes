# import 
import pygame
from settings import *
from spritesheet import *

# Initilize game
g = game()

# main game loop
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

