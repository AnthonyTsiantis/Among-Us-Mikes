# imports
import pygame
import json

# this class is responsible for parsing all the spritesheets
class spritesheet():
    def __init__(self, filename, sprite_type):
        self.filename = filename # initilize filename 
        self.sprite_type = sprite_type # initilize sprite type
        self.sprite_sheet = pygame.image.load(filename).convert_alpha() # load .png into memory
        self.meta_data = self.filename.replace('png', 'json') # load .json into memory
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    # function converts and loads the spirte sheets
    def get_sprite(self, x, y, w, h):
        if self.sprite_type == "Character":
            sprite = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
            sprite.blit(self.sprite_sheet, (0,0), (x, y, w, h))
        
        if self.sprite_type == "Map":
            sprite = pygame.Surface((w, h)).convert()
            sprite.fill((0,0,0))
            sprite.set_colorkey((0, 0, 0))
            sprite.blit(self.sprite_sheet, (0,0), (x, y, w, h))
        return sprite
    
    # function parse's the spritesheet for individual image and returns it
    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image