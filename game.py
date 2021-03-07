import pygame
from menu import *

# game class that controls key inputs and what is displayed on screen
class game():
    # Initilizing screen and menu's
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.up_key, self.down_key, self.start_key, self.back_key, self.right_key, self.left_key = False, False, False, False, False, False
        self.no_input = True
        self.display_W, self.display_H = 1920, 1080
        self.display = pygame.Surface((self.display_W, self.display_H))
        self.window = pygame.display.set_mode((self.display_W, self.display_H), pygame.RESIZABLE) # CHANGE THIS TO FULLSCREEN 
        self.font_name = 'Fonts/gameFont.ttf'
        self.fullscreen = False
        pygame.display.set_caption("St. Mike's Among Us!")
        self.icon = pygame.image.load("images/icon.png")
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.skin = "Black"
        self.main_menu = MainMenu(self)
        self.settings = settingsMenu(self)
        self.skin_menu = skinMenu(self)
        self.host_join = host_join_menu(self)
        self.controls_menu = controls_menu(self)
        self.graphics_menu = graphics_menu(self)
        self.pregame = pregame_lobby(self)
        self.curr_menu = self.main_menu
        self.username = "Test"

    # game class game loop
    def game_loop(self):
        while self.playing:
            self.check_events()

            if self.start_key:
                self.playing = False

            pygame.display.update()
            self.clock.tick(60)
            self.reset_keys()

    # event checker
    def check_events(self):
        # Event listener for loop
        for event in pygame.event.get():
            # Quit program
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False

            # key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_key = True
                    self.no_input = False

                if event.key == pygame.K_BACKSPACE:
                    self.back_key = True
                    self.no_input = False

                if event.key == pygame.K_DOWN:
                    self.down_key = True
                    self.no_input = False

                if event.key == pygame.K_UP:
                    self.up_key = True
                    self.no_input = False
                
                if event.key == pygame.K_RIGHT:
                    self.right_key = True
                    self.no_input = False
                
                if event.key == pygame.K_LEFT:
                    self.left_key = True
                    self.no_input = False
                
                if event.key == pygame.K_a:
                    self.left_key = True
                    self.no_input = False
                
                if event.key == pygame.K_d:
                    self.right_key = True
                    self.no_input = False
                
                if event.key == pygame.K_w:
                    self.up_key = True
                    self.no_input = False
                
                if event.key == pygame.K_s:
                    self.down_key = True
                    self.no_input = False
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.down_key = False
                    self.no_input = True

                if event.key == pygame.K_UP:
                    self.up_key = False
                    self.no_input = True
                
                if event.key == pygame.K_RIGHT:
                    self.right_key = False
                    self.no_input = True
                
                if event.key == pygame.K_LEFT:
                    self.left_key = False
                    self.no_input = True
                
                if event.key == pygame.K_a:
                    self.left_key = False
                    self.no_input = True
                
                if event.key == pygame.K_d:
                    self.right_key = False
                    self.no_input = True
                
                if event.key == pygame.K_w:
                    self.up_key = False
                    self.no_input = True
                
                if event.key == pygame.K_s:
                    self.down_key = False
                    self.no_input = True
                
                

    # reset key input
    def reset_keys(self):
        self.start_key, self.back_key = False, False

    # draw text to screen
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
    



