# import statements
import pygame
from menu import *
from game import *
from os import path

# game class that controls key inputs and what is displayed on screen
class game():
    # Initilizing screen and menu's
    def __init__(self):
        pygame.init() # initilze pygame
        self.running, self.playing = True, False # is screen displayed, is player playing
        self.up_key, self.down_key, self.start_key, self.back_key, self.right_key, self.left_key = False, False, False, False, False, False # key inputs for menu's
        self.move_f, self.move_b, self.move_l, self.move_r = False, False, False, False # key inputs for characters
        self.mouse_pos = pygame.mouse.get_pos() # get mouse position
        self.left_click = False
        
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
        self.ingame_settings = ingame_settingsMenu(self)
        self.skin_menu = skinMenu(self)
        self.difficulty_menu = difficulty_menu(self)
        self.game_difficulty = "Easy"
        self.controls_menu = controls_menu(self)
        self.pregame = pregame_lobby(self)
        self.game_screen = game_lobby(self)
        self.end_game = end_game(self)
        self.curr_menu = self.main_menu # set default menu to main menu
        self.previous_menu = self.main_menu
        
        # other varibales
        self.task_running = False
        self.user_string = ''
        self.right_password = False
        self.current_level = 0
        self.progress_bar = pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/progress bar.png").convert_alpha(), (848, 50))
        self.progress_bar_rect = pygame.Rect(500, 15, 0, 50)
        self.game_time = 0
        self.game_time_limit = 0
        self.start_time = 0
        self.end_time = 0
        self.time_elapsed = 0
        self.game_completed = True
        self.highscore_filename = "highscore.txt"
        self.highscore = 0
        self.load_highscore()

    def load_highscore(self):
        self.dir = path.dirname(__file__)
        try:
            #try to read the file
            with open(path.join(self.dir, self.highscore_filename), 'r+') as f:
                self.highscore = int(f.read())

        except:
            #create the file
            with open(path.join(self.dir, self.highscore_filename), 'w') as f:
                f.write("10000")
                self.highscore = 10000

    # game class game loop
    def game_loop(self):
        while self.playing:
            self.check_events() # check events
            

            if self.start_key:
                self.playing = False

            if self.curr_menu == self.main_menu:
                self.task_running = False
                self.user_string = ''
                self.right_password = False

            pygame.display.update() # update display
            self.clock.tick(30) # 30 FPS
            self.reset_keys() # reset input back to false unless clicked

    # event checker
    def check_events(self):
        # get and update mouse position
        self.mouse_pos = pygame.mouse.get_pos()
        # Event listener for loop
        for event in pygame.event.get():
            # Quit program
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False

            # key down, updates all keys if pressed
            if event.type == pygame.KEYDOWN and not self.task_running:
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
            
            elif event.type == pygame.KEYDOWN and self.curr_menu != self.pregame and self.curr_menu != self.game_screen:
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

            elif event.type == pygame.KEYDOWN and self.task_running and self.curr_menu == self.pregame:
                if event.key == pygame.K_BACKSPACE and not self.right_password:
                    self.user_string = self.user_string[:-1]
                
                else:
                    if not self.right_password:
                        self.user_string += event.unicode

            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_l = False
                
                if event.key == pygame.K_d:
                    self.move_r = False
                
                if event.key == pygame.K_w:
                    self.move_f = False
                
                if event.key == pygame.K_s:
                    self.move_b = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_click = True
                    self.mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_click = False
                    self.mouse_pos = pygame.mouse.get_pos()

                

    # reset key input
    def reset_keys(self):
        self.start_key, self.back_key, self.right_key, self.left_key, self.up_key, self.down_key, self.left_click = False, False, False, False, False, False, False

    # draw text to screen
    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_task_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.display.blit(text_surface, text_rect)

    



