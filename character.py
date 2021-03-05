"""
import pygame
from game import *

class character():
    def __init__(self, character, game):
        self.game = game
        self.character = character
        self.state = "Idle"
        self.xvalue, self.yvalue = self.game.display_W / 2, self.game.display_H / 2

    def move_forward(self):
        self.xvalue -= 10
        self.yvalue -= 10
        print("works")

    def move_backward(self):
        self.xvalue += 10
        self.yvalue += 10

    def move_left(self):
        self.xvalue -= 10

    def move_right(self):
        self.xvalue += 10

    def game_loop(self):
        while self.game.playing:
            self.game.check_events()

            if self.game.move_f:
                move_forward()
            
            if self.game.move_b:
                move_backward()
            
            if self.game.move_l:
                move_left()
            
            if self.game.move_r:
                move_right()
            
            pygame.display.update()
            self.clock.tick(60)
            self.reset_keys()
"""