import pygame
from game import game
g = game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

