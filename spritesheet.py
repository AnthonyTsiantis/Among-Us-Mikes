import pygame
import json

class spritesheet():
    def __init__(self, filename, sprite_type):
        self.filename = filename
        self.sprite_type = sprite_type
        if self.sprite_type == "Character":
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()

        if self.sprite_type == "Map":
            self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

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
    
    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image