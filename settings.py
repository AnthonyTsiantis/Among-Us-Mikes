# import statements
import pygame
from menu import *
from game import *

# game class that controls key inputs and what is displayed on screen
class game():
    # Initilizing screen and menu's
    def __init__(self):
        pygame.init() # initilze pygame
        self.running, self.playing = True, False # is screen displayed, is player playing
        self.up_key, self.down_key, self.start_key, self.back_key, self.right_key, self.left_key = False, False, False, False, False, False # key inputs for menu's
        self.move_f, self.move_b, self.move_l, self.move_r = False, False, False, False # key inputs for characters
        self.display_W, self.display_H = 1920, 1080 # screen dimensions
        self.display = pygame.Surface((self.display_W, self.display_H), pygame.SRCALPHA) # create display surface
        self.window = pygame.display.set_mode((self.display_W, self.display_H), pygame.RESIZABLE) # initilize window
        self.font_name = 'Fonts/gameFont.ttf' # game font 
        pygame.display.set_caption("St. Mike's Among Us!") # game caption
        self.icon = pygame.image.load("images/icon.png") # load the game icon
        pygame.display.set_icon(self.icon) # set the icon
        self.clock = pygame.time.Clock() # initilize the game clock
        self.skin = "Black" # default character skin
        
        # initilize all the menu's in menu.py
        self.main_menu = MainMenu(self)
        self.settings = settingsMenu(self)
        self.skin_menu = skinMenu(self)
        self.host_join = host_join_menu(self)
        self.controls_menu = controls_menu(self)
        self.graphics_menu = graphics_menu(self)
        self.pregame = pregame_lobby(self)
        self.game_screen = game_lobby(self)
        self.curr_menu = self.main_menu # set default menu to main menu

    # game class game loop
    def game_loop(self):
        while self.playing:
            self.check_events() # check events

            if self.start_key:
                self.playing = False

            pygame.display.update() # update display
            self.clock.tick(30) # 30 FPS
            self.reset_keys() # reset input back to false unless clicked

    # event checker
    def check_events(self):
        # Event listener for loop
        for event in pygame.event.get():
            # Quit program
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False

            # key down, updates all keys if pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_key = True

                if event.key == pygame.K_BACKSPACE:
                    self.back_key = True

                if event.key == pygame.K_DOWN:
                    self.down_key = True

                if event.key == pygame.K_UP:
                    self.up_key = True
                
                if event.key == pygame.K_RIGHT:
                    self.right_key = True
                
                if event.key == pygame.K_LEFT:
                    self.left_key = True
                
                if event.key == pygame.K_a:
                    self.move_l = True

                if event.key == pygame.K_d:
                    self.move_r = True
                
                if event.key == pygame.K_w:
                    self.move_f = True
                
                if event.key == pygame.K_s:
                    self.move_b = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_l = False
                
                if event.key == pygame.K_d:
                    self.move_r = False
                
                if event.key == pygame.K_w:
                    self.move_f = False
                
                if event.key == pygame.K_s:
                    self.move_b = False
                
                

    # reset key input
    def reset_keys(self):
        self.start_key, self.back_key, self.right_key, self.left_key, self.up_key, self.down_key = False, False, False, False, False, False

    # draw text to screen
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
    



