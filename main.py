import pygame
from game import *
g = game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

