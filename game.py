# import statments
import pygame
from pygame.locals import *
from spritesheet import *
from menu import *
import math
import random
import time

# Pregame lobby
class pregame_lobby(menu):
    # initilize lobby
    def __init__(self, game):
        menu.__init__(self, game)
        self.load_sprites()
        self.status = "idle_r"
        self.walk_counter = 0
        self.rocket_counter = 0
        self.frame_index = 0
        self.playerx = 800
        self.playery = 240
        self.input = False
        self.spawned = False
        self.spawn_counter = 0
        self.spawn_index = 0
        self.boxx, self.boxy = 725, 450
        self.moved_left = False
        self.current_task = "ID CARD"
        self.player_hitbox = pygame.Rect(self.playerx, self.playery, 50, 77)
        self.level_textx, self.level_texty = 125, 75
        self.computer_textx, self.computer_texty = 425, 800
        self.computer_password = ['PASSWORD123', 'IMPOSTOR123', 'CREWMATE123', 'DOUBLEBLUE123']
        self.computer_password = self.computer_password[random.randint(0,3)]
        self.computer_key = random.randint(1, 25)
        self.encrypted_password = self.caesar_ciper(self.computer_password, self.computer_key)
        self.wrong_password = False
        self.counter = 0
        self.begin_folder_animation = False
        self.folder_animation_counter = 0
        self.begin_upload = False
        self.first_folder = False
        self.close_files = False
        self.folder_progress = 0
        self.upload_progress_rect = pygame.Rect(440, 700, 0, 60)
    
    def load_sprites(self):
        self.stars = pygame.image.load("images/background/game/pregame/stars.png")
        
        self.id_card = pygame.transform.scale(pygame.image.load("images/tasks/Enter Id Code/admin_Card.png"), (50, 30))
        self.id_card_rect = pygame.Rect(1025, 260, 50, 30)
        
        self.door_button = pygame.transform.scale(pygame.image.load("images/background/game/buttons/door_button.png").convert_alpha(), (100, 100))
        self.door_button.set_alpha(128)
        
        self.map_button =  pygame.transform.scale(pygame.image.load("images/background/game/buttons/map_button.png").convert_alpha(), (100, 100))
        
        self.settings_button =  pygame.transform.scale(pygame.image.load("images/background/game/buttons/settings_button.png").convert_alpha(), (100, 100))
        self.settings_button_rect = pygame.Rect(1800, 25, 100, 100)
        
        self.use_button =  pygame.transform.scale(pygame.image.load("images/background/game/buttons/use_button.png").convert_alpha(), (213, 212))
        self.use_button_rect = pygame.Rect(1700, 850, 213, 212)
        self.use_button_alpha_value = 128
        self.use_button.set_alpha(self.use_button_alpha_value)

        Spritesheet = spritesheet("images/background/game/pregame/spritesheet.png", "Character")
        self.box = Spritesheet.parse_sprite('box.png',)
        self.ship = Spritesheet.parse_sprite('ship.png')
        self.front = Spritesheet.parse_sprite('front.png')
        
        self.computers = [Spritesheet.parse_sprite('computer1.png'), Spritesheet.parse_sprite('computer2.png')]
        self.computer_rect = pygame.Rect(740, 440, 80, 71)

        self.computer_screen = pygame.transform.scale(pygame.image.load("images/tasks/computer task/screen.png").convert_alpha(), (1200, 841))
        self.computer_text_box = pygame.transform.scale(pygame.image.load("images/tasks/computer task/text box.png").convert_alpha(), (1024, 115))
        self.computer_enter_button = pygame.transform.scale(pygame.image.load("images/tasks/computer task/enter button.png").convert_alpha(), (250, 123))
        self.computer_enter_button.set_alpha(128)
        
        self.rocket = [Spritesheet.parse_sprite('rocket1.png'), Spritesheet.parse_sprite('rocket2.png'), Spritesheet.parse_sprite('rocket3.png'), Spritesheet.parse_sprite('rocket4.png'), Spritesheet.parse_sprite('rocket5.png'), Spritesheet.parse_sprite('rocket6.png')]
        self.left_rocket = []
        for rocket in self.rocket:
            self.left_rocket.append(pygame.transform.rotate(rocket, 23))

        self.admin_wallet = pygame.image.load("images/tasks/Enter Id Code/admin_Wallet.png").convert_alpha()
        self.enterID_panel = pygame.transform.scale(pygame.image.load("images/tasks/Enter Id Code/enterID_panel.png").convert_alpha(), (750, 748))

        self.upload_base = pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/base.png").convert_alpha(), (1200, 841))
        self.files = pygame.image.load("images/tasks/Upload Data/files.png").convert_alpha()
        self.filesx, self.filesy = 475, 275
        self.folder_animation = []

        for i in range(1, 6):
            self.folder_animation.append(pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/folder" + str(i) + ".png").convert_alpha(), (275, 163)))

        self.folder_animation[2] = pygame.transform.scale(self.folder_animation[2], (300, 163))
        self.folder_animation[3] = pygame.transform.scale(self.folder_animation[3], (325, 163))
        self.folder_animation[4] = pygame.transform.scale(self.folder_animation[4], (325, 163))
        self.folder_upload_button = pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/upload.png").convert_alpha(), (200, 62))
        self.folder_progress_bar = pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/progress bar.png").convert_alpha(), (1017, 60))
        
    # game loop
    def display_menu(self):
        self.run_display = True
        self.get_character()
        if self.game.previous_menu == self.game.difficulty_menu:
            self.reset()
            
        
        while self.run_display:
            self.player_hitbox = pygame.Rect(self.playerx, self.playery, 50, 77)
            
            if self.frame_index == 5:
                self.frame_index = 0
                self.rocket_counter = (self.rocket_counter + 1) % len(self.rocket)
            
            self.game.check_events()
            

            if self.spawned:
                self.check_input()

            self.game.display.blit(self.stars, (0, 0))
            self.game.display.blit(self.ship, (320, 10))
            self.game.display.blit(pygame.transform.scale(self.front, (640, 361)), (612, 646))
            self.game.display.blit(self.box, (self.boxx, self.boxy))
            self.game.display.blit(self.computers[0], (740, 440))
            self.game.display.blit(self.left_rocket[self.rocket_counter], (340, 707))
            self.game.display.blit(self.rocket[self.rocket_counter], (1326, 736))

            if not self.spawned and self.spawn_index % 6 == 0:
                self.spawn_counter = (self.spawn_counter + 1) % len(self.spawn_in)
                if self.spawn_counter == 13:
                    self.playery += 5
                    self.spawned = True
            
            if not self.spawned:
                if self.spawn_counter > 6:
                    self.playerx += 1
                    self.game.display.blit(pygame.transform.scale(self.spawn_in[self.spawn_counter], (50, 77)), (self.playerx, self.playery))
                else:
                    self.game.display.blit(pygame.transform.scale(self.spawn_in[self.spawn_counter], (50, 77)), (self.playerx, self.playery - 10))
            
            self.check_status()

            self.frame_index += 1
            
            if not self.spawned:
                self.spawn_index += 1


            self.buttons()
            self.blit_tasks()
            self.blit_screen()
        
    def reset(self):
        self.spawned = False
        self.current_task = "ID CARD"
        self.game.task_running = False
        self.playerx = 800
        self.playery = 240
        self.id_card = pygame.transform.scale(pygame.image.load("images/tasks/Enter Id Code/admin_Card.png"), (50, 30))
        self.game.right_password = False
        self.counter = 0
        self.begin_upload = False
        self.first_folder = False
        self.close_files = False
        self.folder_progress = 0
        self.upload_progress_rect = pygame.Rect(440, 700, 0, 60)
        self.current_task = "ID CARD"
        


    # menu and gameplay buttons
    def buttons(self):
        self.game.display.blit(self.settings_button, (1800, 25))
        self.game.display.blit(self.use_button, (1700, 850))
        self.progress_bar()
        if self.settings_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
            self.game.curr_menu = self.game.ingame_settings
            self.run_display = False
    
    def progress_bar(self):
        self.game.display.blit(self.game.progress_bar, (500, 15))
        self.game.progress_bar_rect.width = self.game.current_level * 94
        pygame.draw.rect(self.game.display, (0, 255, 0), self.game.progress_bar_rect)
        self.game.draw_text("Game Progress", 50, 600, 40, (255, 255, 255))
    
    def id_card_task(self):
        if pygame.Rect.colliderect(self.player_hitbox, self.id_card_rect):
            self.game.display.blit(self.id_card, (1025, 260))
            pygame.draw.rect(self.game.display, (0, 255, 0), self.id_card_rect, 2)
            self.use_button.set_alpha(255)
            
            if self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                self.current_task = "UNLOCK COMPUTER"
                self.use_button.set_alpha(128)

        else: 
            self.game.display.blit(self.id_card, (1025, 260))
            pygame.draw.rect(self.game.display, (255, 255, 0), self.id_card_rect, 2)
            self.use_button.set_alpha(128)


    def unlock_computer(self):
        if not self.game.task_running:
            pygame.draw.rect(self.game.display, (255, 255, 0), self.computer_rect, 2)
            self.use_button.set_alpha(128)
        
        else:
            self.id_card = pygame.transform.scale(pygame.image.load("images/tasks/Enter Id Code/admin_Card.png"), (350, 213))
            self.game.display.blit(self.computer_screen, (350, 100))
            self.game.display.blit(self.computer_text_box, (407, 775))
            self.game.display.blit(self.id_card, (25, 500))
            
            self.game.draw_task_text(str(self.computer_key), 100, 290, 510, (0, 0, 0))
            self.game.draw_task_text("Auto Pilot Computer", 150, 500, 200, (0, 0, 0))
            self.game.draw_task_text("The password is encryted with a caesar cypher:", 65, 450, 400, (0, 0, 0))
            self.game.draw_text(self.encrypted_password, 225, 900, 650, (0, 0, 0))

            if self.game.user_string == '' and not self.wrong_password and not self.game.right_password:
                self.game.draw_task_text("*User input will be displayed here*", 50, 425, 815, (0, 0, 0))

            elif self.game.user_string == '' and self.wrong_password and not self.game.right_password:
                self.game.draw_task_text("WRONG PASSWORD: Re-enter password", 50, 425, 815, (255, 0, 0))

            if self.game.right_password:
                if self.counter < 20 or self.counter > 40:
                    self.game.draw_task_text("Password Accepted!", 50, 425, 815, (0, 255, 0))
                self.counter += 1

            if self.counter >= 60:
                self.current_task = "UPLOAD DATA"
                self.counter = 0

            if len(self.game.user_string) == len(self.computer_password):
                self.computer_enter_button.set_alpha(255)
                if self.computer_enter_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                    if self.game.user_string.upper() == self.computer_password:
                        self.wrong_password = False
                        self.game.right_password = True
                        self.game.user_string = ''
                    else:
                        self.game.user_string = ''
                        self.wrong_password = True 
            
            else:
                self.computer_enter_button.set_alpha(128)
        

            self.game.draw_task_text(self.game.user_string, 75, self.computer_textx, self.computer_texty, (0, 0, 0))
            self.computer_enter_button_rect = self.game.display.blit(self.computer_enter_button, (1190, 770))
            
        
        if pygame.Rect.colliderect(self.player_hitbox, self.computer_rect) and not self.game.task_running:
            self.use_button.set_alpha(255)
            pygame.draw.rect(self.game.display, (0, 255, 0), self.computer_rect, 2)
            
            if self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                self.game.task_running = True
                self.use_button.set_alpha(128)

    def caesar_ciper(self, password, key):
        result = ''
        for i in range(len(password)):
            char = password[i]
            if char.isalpha():
                # Encrypt uppercase characters in plain text
                if (char.isupper()):
                    result += chr((ord(char) + key - 65) % 26 + 65)
            else:
                result += str(int(char) + key)
        return result

    def upload_autopilot(self):
        self.game.display.blit(self.upload_base, (350, 100))
        self.game.draw_text("Upload Auto-Pilot Software", 90, 950, 225)
        self.game.draw_text("Computer", 75, 610, 600)
        self.game.draw_text("Ship", 75, 1285, 600)
        self.game.display.blit(pygame.transform.scale(self.files, (300, 236)), (self.filesx, self.filesy))
        self.game.display.blit(self.folder_animation[self.folder_animation_counter], (482, 375))
        self.game.display.blit(self.folder_animation[self.folder_animation_counter], (1150, 375))
        self.game.display.blit(self.folder_upload_button, (850, 550))
        upload_button_rect = pygame.Rect(850, 550, 200, 62)
        self.game.draw_text("Upload Progress", 60, 950, 675)
        self.upload_progress_rect.width = self.folder_progress * 44 # Final form(440, 700, 1017, 60)
        self.game.display.blit(self.folder_progress_bar, (440, 700))
        pygame.draw.rect(self.game.display, (0, 255, 0), self.upload_progress_rect)
        

        if not self.begin_upload:
            pygame.draw.rect(self.game.display, (255, 255, 0), upload_button_rect, 5)

        else:
            pygame.draw.rect(self.game.display, (0, 255, 0), upload_button_rect, 5)
        
        if upload_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
            self.begin_upload = True
        
        
        if self.counter % 25 == 0 and self.begin_upload and not self.first_folder:
            self.folder_animation_counter += 1
            self.folder_progress += 1
            
            if self.folder_animation_counter < 4:
                pass
            else:
                self.first_folder = True
                self.counter = 0

        elif self.counter % 25 == 0 and self.begin_upload and self.first_folder and not self.close_files:
                self.filesx += 50
                self.folder_progress += 1
                if self.filesx > 1150:
                    self.close_files = True

        elif self.counter % 25 == 0 and self.begin_upload and self.first_folder and self.close_files:
            self.folder_animation_counter -= 1
            self.folder_progress += 1
            if self.folder_animation_counter >= 0:
                pass
            else:
                self.upload_progress_rect.right = 1017
                self.current_task = "TURN ON POWER REACTOR"
                self.counter = 0
                self.begin_upload = False
                self.game.task_running = False
        
        self.counter += 1


    def blit_tasks(self):
        if self.current_task == "ID CARD":
            self.game.current_level = 1
            self.id_card_task()
            self.game.draw_text("Level 1", 100, self.level_textx, self.level_texty, (255, 255, 255))
            self.game.draw_text("Collect the ID Card", 50, self.level_textx + 25, self.level_texty + 100, (255, 255, 255))

        elif self.current_task == "UNLOCK COMPUTER":
            self.game.current_level = 2
            self.unlock_computer()
            self.game.draw_text("Level 2", 100, self.level_textx, self.level_texty, (255, 255, 255))
            self.game.draw_text("Unlock the Computer", 50, self.level_textx + 25, self.level_texty + 100, (255, 255, 255))

        elif self.current_task == "UPLOAD DATA":
            self.game.current_level = 3
            self.upload_autopilot()
            self.game.draw_text("Level 3", 100, self.level_textx, self.level_texty, (255, 255, 255))
            self.game.draw_text("Upload the ", 50, self.level_textx - 15, self.level_texty + 75, (255, 255, 255))
            self.game.draw_text("Autopilot software", 50, self.level_textx + 25, self.level_texty + 125, (255, 255, 255))

        elif self.current_task == "TURN ON POWER REACTOR":
            self.current_task = "ID CARD"
            self.run_display = False
            self.game.curr_menu = self.game.game_screen


    # get the character from the spritesheet
    def get_character(self):
        Spritesheet = spritesheet("images/characters/"+ self.game.skin + "/" + self.game.skin + "_character_spritesheet.png", "Character")
        self.idle = [Spritesheet.parse_sprite('idle1.png'), Spritesheet.parse_sprite('idle2.png')]
        self.walk = []
        for i in range(12): 
            self.walk.append(Spritesheet.parse_sprite('walk' + str(i + 1) + '.png'))
        
        self.spawn_in = []
        for i in range(14):
            self.spawn_in.append(Spritesheet.parse_sprite('spawn-in' + str(i + 1) + '.png'))
    
    # detemines map boundaries returning a boolean value if out of bounds
    def map_boundaries(self):
        out_of_bounds = False
        top_left_angle = (-0.5 * self.playerx) + 630 # formula for slope of the top left side
        top_right_angle = (0.4 * self.playerx) - 175 # formula for slope of the top right side
        bottom_right_angle = (-1.1 * self.playerx) + 1822 # formula for slope of the bottom right side
        bottom_left_angle  = (0.9 * self.playerx) - 39

        # Top straight
        if self.playerx > 800 and self.playery < 230 and self.playerx < 1000:
            out_of_bounds = True

        # Top left angle
        elif (self.playery - top_left_angle) < 0:
            out_of_bounds = True
        
        # Top right angle
        elif (self.playery - top_right_angle) < 0:
            out_of_bounds = True

        # Right side straight    
        elif self.playerx > 1160 and self.playery > 275 and self.playery < 545:
            out_of_bounds = True
        
        # Bottom Right side
        elif (self.playery - bottom_right_angle) > 0:
            out_of_bounds = True
        
        # Bottom straight
        elif self.playerx < 1110 and self.playerx > 710 and self.playery > 601:
            out_of_bounds = True

        # Bottom left side
        elif (self.playery - bottom_left_angle) > 0:
            out_of_bounds = True

        # left side
        elif self.playerx < 660 and self.playery > 300 and self.playery < 555:
            out_of_bounds = True

        return out_of_bounds

    # detemines if the player inteferes with the box 
    def box_collision(self):
        if self.playerx > 682 and self.playerx < 820 and self.playery > 380 and self.playery < 532:
            return True
        else:
            return False
    
    # adjusts player sprite if input is detected
    def check_status(self):
        if self.status == "idle_r" and self.spawned:
                self.game.display.blit(pygame.transform.scale(self.idle[0], (50, 77)), (self.playerx, self.playery))

        if self.status == "idle_l" and self.spawned:
            self.game.display.blit(pygame.transform.scale(self.idle[1], (50, 77)), (self.playerx, self.playery))
        
        if self.status == "walking_r" and self.spawned:
            self.game.display.blit(pygame.transform.scale(self.walk[self.walk_counter], (50, 77)), (self.playerx, self.playery))
            self.walk_counter = (self.walk_counter + 1) % len(self.walk)
        
        if self.status == "walking_l" and self.spawned:
            self.game.display.blit(pygame.transform.flip(pygame.transform.scale(self.walk[self.walk_counter], (50, 77)), True, False), (self.playerx, self.playery))
            self.walk_counter = (self.walk_counter + 1) % len(self.walk)

    # checks game input and moves player
    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        
        if self.game.start_key:
            self.run_display = False
            self.game.curr_menu = self.game.game_screen
        
        if self.game.move_f and not self.game.task_running:
            if not self.box_collision() or not self.map_boundaries():
                self.playery -= 7
                self.status = "walking_r"
                self.input = True
                self.moved_left = False
            
            while self.box_collision() or self.map_boundaries():
                    if self.box_collision():
                        self.playery += 1

                    if self.map_boundaries():
                        if self.playery < 300 and self.playerx < 800 and self.playerx < 1000:
                            self.playery += 1
                            self.playerx += 1

                        elif self.playery < 300 and self.playerx >= 1000:
                            self.playery += 1
                            self.playerx -= 1
                        
                        elif self.playerx <= 710 and self.playerx > 660 and self.playery > 555:
                            self.playerx += 1
                            self.playery -= 1

                        else:
                            self.playery += 1
        
        if self.game.move_b and not self.game.task_running:
            if self.box_collision() or self.map_boundaries():
                pass
            else:
                self.input = True
                self.playery += 7
                self.status = "walking_l"
                self.moved_left = True
            
            while self.box_collision() or self.map_boundaries():
                if self.box_collision():
                    self.playery -= 1

                if self.map_boundaries():
                    if self.playery >= 545 and self.playerx > 1110:
                        self.playery -= 1
                        self.playerx -= 1
                    
                    elif self.playerx <= 1110 and self.playerx > 710 and self.playery > 601:
                        self.playery -= 1

                    elif self.playerx <= 710 and self.playery > 555:
                        self.playerx += 1
                        self.playery -= 1
                    
                    else:
                        self.playery -= 1
                           
        if self.game.move_r and not self.game.task_running:
            if self.box_collision() or self.map_boundaries():
                pass
            else:   
                self.input = True
                self.playerx += 7
                self.status = "walking_r"
                self.moved_left = False

            while self.box_collision() or self.map_boundaries():
                if self.box_collision():
                    self.playerx -= 1
                
                if self.map_boundaries():
                    if self.playery < 545 and self.playery > 300 and self.playerx > 1160:
                        self.playerx -= 1

                    elif self.playery <= 300 and self.playerx >= 1000:
                        self.playery += 1
                        self.playerx -= 1
                    
                    elif self.playery >= 545 and self.playerx > 1110:
                        self.playery -= 1
                        self.playerx -= 1
                    
                    else:
                        self.playerx -= 1
        
        if self.game.move_l and not self.game.task_running:
            if not self.box_collision() or not self.map_boundaries():
                self.input = True
                self.playerx -= 7
                self.status = "walking_l"
                self.moved_left = True
            
            while self.box_collision() or self.map_boundaries():
                if self.box_collision():
                    self.playerx += 1

                elif self.map_boundaries(): 
                    if self.playerx < 800 and self.playery < 300:
                        self.playery += 1
                        self.playerx += 1 
                    
                    elif self.playerx <= 710 and self.playery >= 555:
                        self.playery -= 1
                        self.playerx += 1
                    
                    elif self.playerx < 660 and self.playery >= 300 and self.playery < 555:
                        self.playerx += 1
                    
                    else:
                        self.playerx += 1

                    
        
        if not self.game.move_l and not self.game.move_r and not self.game.move_f and not self.game.move_b:
            self.input = False
        
        if not self.input:
            if self.moved_left:
                self.status = "idle_l"
            else:
                self.status = "idle_r"


# the game lobby class
class game_lobby(pregame_lobby):
    # initlize the class
    def __init__(self, game):
        menu.__init__(self, game)
        pregame_lobby.__init__(self, game)
        self.load_sprites()
        self.status = "idle_r"
        self.playerx, self.playery = (910, 463)
        self.scrollx, self.scrolly = (0, 0)
        self.walk_counter = 0
        self.spawn_coords = [(145, 13), (-6, -75), (-158, 13), (-6, 133)]
        rand_coords = self.spawn_coords[random.randint(0,3)]
        self.scrollx, self.scrolly = rand_coords
        self.spawned = False
        self.screen_index = 0
        self.oxygen_index = 0
        self.comms_index = 0
        self.engine_index = 0
        self.engine_bolt_index = 0
        self.engine_puff_index = 0
        self.medbay_scan_index = 0
        self.security_screen_index = 0
        self.security_server_index = 0
        self.animation_index = 0
        self.idle_left = False 
        self.border_color = (255, 0, 0, 0) # change final value to 100 to see boundaries 
        self.player_hitbox = pygame.Rect(self.playerx, self.playery, 50, 77)
        self.show_fuel = True
        self.power_task = "REACTORS"
        self.fuel_task_rect = None
        self.engine_fuel_rect = pygame.Rect(500, 200, 614, 580)
        self.fueled = False
        self.powered = False 
        self.initiate_scan = False
        self.current_task = "TURN ON POWER REACTOR"

        self.background()

    # loads all the sprites into memory
    def load_sprites(self):
        self.stars = pygame.image.load("images/background/game/pregame/stars.png")
        self.cafeteria = pygame.image.load("images/background/game/game_map/cafeteria/Cafeteria.png")
        self.cafeteria_hallway_left = pygame.image.load("images/background/game/game_map/cafeteria/Cafeteria_Upper_Engine_Medbay_Hallway.png") 
        
        weapons_spritesheet = spritesheet("images/background/game/game_map/weapons/weapons.png", "Character")
        self.cafeteria_weapons_hallway = weapons_spritesheet.parse_sprite('hallway.png')
        self.weapons_chair = weapons_spritesheet.parse_sprite('chair.png')
        self.weapons_box = weapons_spritesheet.parse_sprite('box.png')
        self.weapons_base = []
        for i in range(9):
            self.weapons_base.append(weapons_spritesheet.parse_sprite('base' + str(i + 1) + '.png'))
        
        self.weapons_screen = []
        for i in range(22):
            self.weapons_screen.append(weapons_spritesheet.parse_sprite('screen' + str(i + 1) + '.png'))

        self.weapons_task = [weapons_spritesheet.parse_sprite('task1.png'), weapons_spritesheet.parse_sprite('task2.png')]

        self.weapons_gun = []
        for i in range(25):
            self.weapons_gun.append(weapons_spritesheet.parse_sprite('gun' + str(i + 1) + '.png'))
        
        self.O2_nav_weap_hallway = pygame.image.load("images/background/game/game_map/weapons_navigation_hallway/O2_Navigation_Shields_Hallway.png").convert_alpha()
        self.O2_nav_weap_task = pygame.image.load("images/background/game/game_map/weapons_navigation_hallway/O2_Navigation_Shields_task.png").convert_alpha()
        oxygen_spritesheet = spritesheet("images/background/game/game_map/oxygen/oxygen_spritesheet.png", "Character")
        self.oxygen = oxygen_spritesheet.parse_sprite('oxygen.png')

        self.oxygen_fans = []
        for i in range(5):
            self.oxygen_fans.append(oxygen_spritesheet.parse_sprite('fan' + str(i + 1) + '.png'))
        
        self.oxygen_fans_closed = oxygen_spritesheet.parse_sprite('fans_closed.png')
        self.oxygen_vent = oxygen_spritesheet.parse_sprite('task1.png')
        self.oxygen_task1 = oxygen_spritesheet.parse_sprite('task2.png')
        self.oxygen_task2 = oxygen_spritesheet.parse_sprite('task3.png')
        self.oxygen_plant = oxygen_spritesheet.parse_sprite('plant.png')

        nav_spritesheet = spritesheet("images/background/game/game_map/nav/nav_spritesheet.png", "Character")
        self.nav1 = nav_spritesheet.parse_sprite('nav1.png')
        self.nav2 = nav_spritesheet.parse_sprite('nav2.png')
        self.nav3 = nav_spritesheet.parse_sprite('nav3.png')
        self.console1 = nav_spritesheet.parse_sprite('console1.png')
        self.console2 = nav_spritesheet.parse_sprite('console2.png')
        self.chair1 = nav_spritesheet.parse_sprite('chair1.png')
        self.chair2 = nav_spritesheet.parse_sprite('chair2.png')
        self.chair3 = nav_spritesheet.parse_sprite('chair3.png')
        self.nav_box = nav_spritesheet.parse_sprite('box.png')
        self.nav_task1 = nav_spritesheet.parse_sprite('task1.png')
        self.nav_task2 = nav_spritesheet.parse_sprite('task2.png')

        shield_spritesheet = spritesheet("images/background/game/game_map/shields/shield_spritesheet.png", "Character")
        self.shield_light = shield_spritesheet.parse_sprite('light.png')
        self.shield_mic = shield_spritesheet.parse_sprite('mic.png')
        self.shield_rail1 = shield_spritesheet.parse_sprite('rail1.png')
        self.shield_rail2 = shield_spritesheet.parse_sprite('rail2.png')
        self.shield_rail3 = shield_spritesheet.parse_sprite('rail3.png')
        self.shield_rail4 = shield_spritesheet.parse_sprite('rail4.png')
        self.shield1 = shield_spritesheet.parse_sprite('shield1.png')
        self.shield2 = shield_spritesheet.parse_sprite('shield2.png')
        self.shield3 = shield_spritesheet.parse_sprite('shield3.png')

        admin_spritesheet = spritesheet("images/background/game/game_map/admin/admin_spritesheet.png", "Character")
        self.admin_base1 = admin_spritesheet.parse_sprite('base1.png')
        self.admin_base2 = admin_spritesheet.parse_sprite('base2.png')
        self.admin_base3 = admin_spritesheet.parse_sprite('base3.png')
        self.admin_chairs = admin_spritesheet.parse_sprite('chairs.png')
        self.admin_hallway = admin_spritesheet.parse_sprite('hallway.png')
        self.admin_screen1 = admin_spritesheet.parse_sprite('screen1.png')
        self.admin_screen2 = admin_spritesheet.parse_sprite('screen2.png')
        self.admin_table1 = admin_spritesheet.parse_sprite('table1.png')
        self.admin_table2 = admin_spritesheet.parse_sprite('table2.png')
        self.admin_table3 = admin_spritesheet.parse_sprite('table3.png')
        self.admin_table4 = admin_spritesheet.parse_sprite('table4.png')
        self.admin_task1 = admin_spritesheet.parse_sprite('task.png')
        self.admin_task2 = admin_spritesheet.parse_sprite('task2.png')
        self.admin_vent = admin_spritesheet.parse_sprite('vent.png')

        storage_spritesheet = spritesheet("images/background/game/game_map/Storage/spritesheet.png", "Character")
        self.storage_base = storage_spritesheet.parse_sprite('base.png')
        self.storage_bins = storage_spritesheet.parse_sprite('bins.png')
        self.storage_bin = storage_spritesheet.parse_sprite('bin.png')
        self.storage_fuel = storage_spritesheet.parse_sprite('fuel.png')
        self.storage_task1 = storage_spritesheet.parse_sprite('task1.png')
        self.storage_task2 = storage_spritesheet.parse_sprite('task2.png')

        self.storage_shield_hallway = pygame.image.load("images/background/game/game_map/storage_shield/storage_shield_hallway.png")

        comms_spritesheet = spritesheet("images/background/game/game_map/comms/spritesheet.png", "Character")
        self.comms_base1 = comms_spritesheet.parse_sprite('base1.png')
        self.comms_base2 = comms_spritesheet.parse_sprite('base2.png')
        self.comms_base3 = comms_spritesheet.parse_sprite('base3.png')
        self.comms_base4 = comms_spritesheet.parse_sprite('base4.png')
        self.comms_base5 = comms_spritesheet.parse_sprite('base5.png')
        self.comms_base6 = comms_spritesheet.parse_sprite('base6.png')
        self.comms_base7 = comms_spritesheet.parse_sprite('base7.png')
        self.comms_task = self.storage_task2
        self.comms_tape = []
        for i in range(1, 6):
            self.comms_tape.append(comms_spritesheet.parse_sprite('tape' + str(i) + '.png'))

        electrical_spritesheet = spritesheet("images/background/game/game_map/electrical/spritesheet.png", "Character")
        self.elec_base1 = electrical_spritesheet.parse_sprite('base1.png')
        self.elec_base2 = electrical_spritesheet.parse_sprite('base2.png')
        self.elec_door1 = electrical_spritesheet.parse_sprite('door1.png')
        self.elec_door2 = electrical_spritesheet.parse_sprite('door2.png')
        self.elec_wire1 = electrical_spritesheet.parse_sprite('wire1.png')
        self.elec_wire2 = electrical_spritesheet.parse_sprite('wire2.png')
        self.elec_task1 = electrical_spritesheet.parse_sprite('task1.png')
        self.elec_task2 = self.comms_task

        engine_spritesheet = spritesheet("images/background/game/game_map/engines/spritesheet.png", "Character")
        self.lower_engine_base = engine_spritesheet.parse_sprite('lower_engine.png')
        self.upper_engine_base = engine_spritesheet.parse_sprite('upper_engine.png')
        
        self.engine_base = []
        self.engine_puff = []
        self.engine_bolt = []
        for i in range(1, 13):
            if i < 5:
                self.engine_base.append(engine_spritesheet.parse_sprite('engine' + str(i) + '.png'))
                self.engine_puff.append(engine_spritesheet.parse_sprite('puff' + str(i) + '.png'))
                self.engine_bolt.append(engine_spritesheet.parse_sprite('bolt' + str(i) + '.png'))
            elif i < 9:
                self.engine_puff.append(engine_spritesheet.parse_sprite('puff' + str(i) + '.png'))
                self.engine_bolt.append(engine_spritesheet.parse_sprite('bolt' + str(i) + '.png'))
            
            else:
                self.engine_bolt.append(engine_spritesheet.parse_sprite('bolt' + str(i) + '.png'))

        self.engine_rail1 = engine_spritesheet.parse_sprite('rail1.png')
        self.engine_rail2 = engine_spritesheet.parse_sprite('rail2.png')
        self.engine_task1 = engine_spritesheet.parse_sprite('task1.png')
        self.engine_task2 = engine_spritesheet.parse_sprite('task2.png')
        self.engine_task3 = engine_spritesheet.parse_sprite('task4.png')
        self.engines_reactor_security_hallway = pygame.image.load("images/background/game/game_map/reactor_security_engine_hallway/Reactor_Security_Engines_Hallway.png")

        medbay_spritesheet = spritesheet("images/background/game/game_map/medbay/spritesheet.png", "Character")
        self.medbay_base1 = medbay_spritesheet.parse_sprite('base1.png')
        self.medbay_base2 = medbay_spritesheet.parse_sprite('base2.png')
        self.medbay_base3 = medbay_spritesheet.parse_sprite('base3.png')

        self.medbay_scan = []
        for i in range(1, 4):
            self.medbay_scan.append(medbay_spritesheet.parse_sprite('scan' + str(i) + '.png'))

        security_spritesheet = spritesheet("images/background/game/game_map/security/spritesheet.png", "Character")
        self.security_base1 = security_spritesheet.parse_sprite('base1.png')
        self.security_chair = security_spritesheet.parse_sprite('chair.png')
        self.security_screen = [security_spritesheet.parse_sprite('screen1.png'), security_spritesheet.parse_sprite('screen2.png')]
        self.security_wire = security_spritesheet.parse_sprite('wire.png')
        self.security_task = security_spritesheet.parse_sprite('task.png')

        self.security_server = []
        for i in range(1, 6):
            self.security_server.append(security_spritesheet.parse_sprite('server' + str(i) + '.png'))


        reactor_spritesheet = spritesheet("images/background/game/game_map/reactor/spritesheet.png", "Character")
        self.reactor_base1 = reactor_spritesheet.parse_sprite('base1.png')
        self.reactor_base2 = reactor_spritesheet.parse_sprite('base2.png')
        self.reactor_base5 = reactor_spritesheet.parse_sprite('base5.png')
        self.reactor_base3 = reactor_spritesheet.parse_sprite('base3.png')
        self.reactor_base4 = reactor_spritesheet.parse_sprite('base4.png')
        self.reactor_part1 = reactor_spritesheet.parse_sprite('reactor1.png')
        self.reactor_part2 = reactor_spritesheet.parse_sprite('reactor2.png')
        self.reactor_part3 = reactor_spritesheet.parse_sprite('reactor3.png')
        self.reactor_part4 = reactor_spritesheet.parse_sprite('reactor4.png')
        self.reactor_part5 = reactor_spritesheet.parse_sprite('reactor5.png')
        self.reactor_part6 = reactor_spritesheet.parse_sprite('reactor6.png')
        self.reactor_part7 = reactor_spritesheet.parse_sprite('reactor7.png')
        self.reactor_part8 = reactor_spritesheet.parse_sprite('reactor8.png')
        self.reactor_part9 = reactor_spritesheet.parse_sprite('reactor9.png')
        self.reactor_part10 = reactor_spritesheet.parse_sprite('reactor10.png')
        self.reactor_part11 = reactor_spritesheet.parse_sprite('reactor11.png')
        self.reactor_part12 = reactor_spritesheet.parse_sprite('reactor12.png')
        self.reactor_part13 = reactor_spritesheet.parse_sprite('reactor13.png')
        self.reactor_part14 = reactor_spritesheet.parse_sprite('reactor14.png')
        self.reactor_part15 = reactor_spritesheet.parse_sprite('reactor15.png')
        self.reactor_task1 = reactor_spritesheet.parse_sprite('task1.png')
        self.reactor_task2 = reactor_spritesheet.parse_sprite('task2.png')
        self.reactor_task3 = reactor_spritesheet.parse_sprite('task3.png')

        self.settings_button =  pygame.transform.scale(pygame.image.load("images/background/game/buttons/settings_button.png").convert_alpha(), (100, 100))
        self.settings_button_rect = pygame.Rect(1800, 25, 100, 100)
        
        self.use_button =  pygame.transform.scale(pygame.image.load("images/background/game/buttons/use_button.png").convert_alpha(), (213, 212))
        self.use_button_rect = pygame.Rect(1700, 850, 213, 212)
        self.use_button_alpha_value = 128
        self.use_button.set_alpha(self.use_button_alpha_value)

        self.calibrate_base = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/base.png").convert_alpha(), (900, 900))
        self.calibrate_colour = "YELLOW"
        self.calibrate_rotate = 25
        self.calibrate_yellow_spinner = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/yellow_spinner.png").convert_alpha(), (248, 235))
        self.calibrate_blue_spinner = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/blue_spinner.png").convert_alpha(), (248, 235))
        self.calibrate_light_blue_spinner = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/light_blue spinner.png").convert_alpha(), (248, 235)) 
        self.calibrate_wire1 = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/wire1.png").convert_alpha(), (103, 58)) 
        self.calibrate_gauge = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/gauge.png").convert_alpha(), (245, 58)) 
        self.calibrate_gauge_t = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/gague_transparent.png").convert_alpha(), (245, 58)) 
        self.calibrate_button = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/button.png").convert_alpha(), (143, 50)) 
        self.calibrate_wire2 = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/wire2.png").convert_alpha(), (103, 58)) 
        self.calibrate_wire3 = pygame.transform.scale(pygame.image.load("images/tasks/Calibrate Distributor/wire3.png").convert_alpha(), (103, 58)) 


        self.fuel_base1 = pygame.transform.scale(pygame.image.load("images/tasks/Fuel Engines/base1.png").convert_alpha(), (614, 900)) 
        self.fuel_base2 = pygame.transform.scale(pygame.image.load("images/tasks/Fuel Engines/base2.png").convert_alpha(), (221, 221)) 
        self.fuel_button = pygame.transform.scale(pygame.image.load("images/tasks/Fuel Engines/button.png").convert_alpha(), (137, 139)) 
        self.fuel_wires = pygame.transform.scale(pygame.image.load("images/tasks/Fuel Engines/wires.png").convert_alpha(), (101, 94)) 

        self.medbay_base_bottom = pygame.transform.scale(pygame.image.load("images/tasks/Submite Scan/base_bottom.png").convert_alpha(), (907, 277)) 
        self.medbay_base_top = pygame.transform.scale(pygame.image.load("images/tasks/Submite Scan/base_top.png").convert_alpha(), (907, 322)) 
        self.medbay_wire = pygame.transform.scale(pygame.image.load("images/tasks/Submite Scan/wire.png").convert_alpha(), (131, 653)) 
        
        self.upload_base = pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/base.png").convert_alpha(), (1200, 841))
        self.files = pygame.image.load("images/tasks/Upload Data/files.png").convert_alpha()
        self.filesx, self.filesy = 475, 275
        self.folder_animation = []

        for i in range(1, 6):
            self.folder_animation.append(pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/folder" + str(i) + ".png").convert_alpha(), (275, 163)))

        self.folder_animation[2] = pygame.transform.scale(self.folder_animation[2], (300, 163))
        self.folder_animation[3] = pygame.transform.scale(self.folder_animation[3], (325, 163))
        self.folder_animation[4] = pygame.transform.scale(self.folder_animation[4], (325, 163))
        self.folder_upload_button = pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/upload.png").convert_alpha(), (200, 62))
        self.folder_progress_bar = pygame.transform.scale(pygame.image.load("images/tasks/Upload Data/progress bar.png").convert_alpha(), (1017, 60))


    def reset(self):
        self.current_task = "TURN ON POWER REACTOR"
        self.game.task_running = False

    # game loop
    def display_menu(self):
        self.run_display = True
        pregame_lobby.get_character(self)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.background()
            self.animation_index = (self.animation_index + 1) % 3

            if not self.spawned:
                self.spawn()
            
            if self.animation_index == 0:
                if self.powered:
                    self.screen_index = (self.screen_index + 1) % len(self.weapons_screen)
                    self.oxygen_index = (self.oxygen_index + 1) % len(self.oxygen_fans)
                    self.comms_index = (self.comms_index + 1) % len(self.comms_tape)
                    self.security_screen_index = (self.security_screen_index + 1) % len(self.security_screen)
                    self.security_server_index = (self.security_server_index + 1) % len(self.security_server)
                    self.medbay_scan_index = (self.medbay_scan_index + 1) % len(self.medbay_scan)

                    if self.fueled:
                        self.engine_index = (self.engine_index + 1) % len(self.engine_base)
                        self.engine_bolt_index = (self.engine_bolt_index + 1) % len(self.engine_bolt)
                        self.engine_puff_index = (self.engine_puff_index + 1) % len(self.engine_puff)
            
            self.buttons()
            if not self.game.task_running:
                self.blit_tasks()

            self.check_status()
            
            if self.game.task_running:
                self.blit_tasks()

            self.blit_screen()

    # menu and gameplay buttons
    def buttons(self):
        self.game.display.blit(self.settings_button, (1800, 25))
        self.game.display.blit(self.use_button, (1700, 850))
        self.progress_bar()
        if self.settings_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
            self.game.curr_menu = self.game.ingame_settings
            self.run_display = False

    def progress_bar(self):
        self.game.display.blit(self.game.progress_bar, (500, 15))
        self.game.progress_bar_rect.width = self.game.current_level * 94
        pygame.draw.rect(self.game.display, (0, 255, 0), self.game.progress_bar_rect)
        if self.game.current_level <= 2:
            self.game.draw_text("Game Progress", 50, 610, 45, (0, 0, 0))
        else:
            self.game.draw_text("Game Progress", 50, 610, 45, (255, 255, 255))

    def calibrate_task(self):
        self.calibrate_rotate = (self.calibrate_rotate + 2) % 360
        self.game.display.blit(self.calibrate_base, (500, 50))

        if self.calibrate_colour == "YELLOW":
            # Yellow spinner
            rotated_image = pygame.transform.rotate(self.calibrate_yellow_spinner, self.calibrate_rotate)
            new_rect = rotated_image.get_rect(center = self.calibrate_yellow_spinner.get_rect(topleft = (575, 105)).center)
            
            self.game.display.blit(self.calibrate_gauge, (1105, 150))
            random_int = random.randint(0, 50)
            pygame.draw.rect(self.game.display, (255, 255, 0), (1105, 150, random_int, 58))
            self.game.display.blit(self.calibrate_button, (1150, 250))
            self.calibrate_button_rect = pygame.Rect(1150, 250, 143, 50)
            pygame.draw.rect(self.game.display, (255, 255, 0), self.calibrate_button_rect, 2) # button rect

            if self.calibrate_rotate < 10 or self.calibrate_rotate > 350:
                self.game.display.blit(self.calibrate_wire1, (795, 195))
                pygame.draw.rect(self.game.display, (255, 255, 0), (1105, 150, 240, 58)) # gauge rect
                pygame.draw.rect(self.game.display, (0, 255, 0), self.calibrate_button_rect, 2) # button rect
                if self.calibrate_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                    self.calibrate_colour = "BLUE"
                    self.calibrate_rotate = 70
                    rotated_image = pygame.transform.rotate(self.calibrate_yellow_spinner, self.calibrate_rotate)
                    new_rect = rotated_image.get_rect(center = self.calibrate_yellow_spinner.get_rect(topleft = (575, 105)).center)

            self.game.display.blit(self.calibrate_gauge_t, (1100, 150))
            self.game.display.blit(rotated_image, new_rect)

            # Blue spinner
            rotated_image = pygame.transform.rotate(self.calibrate_blue_spinner, 70)
            new_rect = rotated_image.get_rect(center = self.calibrate_blue_spinner.get_rect(topleft = (575, 375)).center)
            self.game.display.blit(rotated_image, new_rect)
            self.game.display.blit(self.calibrate_gauge, (1105, 400))
            self.game.display.blit(self.calibrate_button, (1150, 500))
            self.game.display.blit(self.calibrate_gauge_t, (1100, 400))

            # Light blue spinner
            rotated_image = pygame.transform.rotate(self.calibrate_light_blue_spinner, 60)
            new_rect = rotated_image.get_rect(center = self.calibrate_light_blue_spinner.get_rect(topleft = (575, 645)).center)
            self.game.display.blit(self.calibrate_gauge, (1105, 670))
            self.game.display.blit(self.calibrate_button, (1150, 770))
            self.game.display.blit(self.calibrate_gauge_t, (1100, 670))
            self.game.display.blit(rotated_image, new_rect)



        elif self.calibrate_colour == "BLUE":
            # Yellow Spinner
            self.game.display.blit(self.calibrate_wire1, (795, 195))
            self.game.display.blit(self.calibrate_yellow_spinner, (575, 105))
            self.game.display.blit(self.calibrate_gauge, (1105, 150))
            self.game.display.blit(self.calibrate_button, (1150, 250))
            pygame.draw.rect(self.game.display, (255, 255, 0), (1105, 150, 240, 58)) # gauge rect
            self.game.display.blit(self.calibrate_gauge_t, (1100, 150))
            
            # blue spinner
            rotated_image = pygame.transform.rotate(self.calibrate_blue_spinner, self.calibrate_rotate)
            new_rect = rotated_image.get_rect(center = self.calibrate_blue_spinner.get_rect(topleft = (575, 375)).center)
            
            self.game.display.blit(self.calibrate_gauge, (1105, 400))
            random_int = random.randint(0, 50)
            pygame.draw.rect(self.game.display, (0, 0, 255), (1105, 400, random_int, 58))
            self.game.display.blit(self.calibrate_button, (1150, 500))
            self.calibrate_button_rect = pygame.Rect(1150, 500, 143, 50)
            pygame.draw.rect(self.game.display, (255, 255, 0), self.calibrate_button_rect, 2) # button rect

            if self.calibrate_rotate < 10 or self.calibrate_rotate > 350:
                self.game.display.blit(self.calibrate_wire2, (795, 460))
                pygame.draw.rect(self.game.display, (0, 0, 255), (1105, 400, 240, 58)) # gauge rect
                pygame.draw.rect(self.game.display, (0, 255, 0), self.calibrate_button_rect, 2) # button rect
                if self.calibrate_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                    self.calibrate_colour = "LIGHT BLUE"
                    self.calibrate_rotate = 60

            self.game.display.blit(self.calibrate_gauge_t, (1100, 400))
            self.game.display.blit(rotated_image, new_rect)

            # Light blue spinner
            rotated_image = pygame.transform.rotate(self.calibrate_light_blue_spinner, 60)
            new_rect = rotated_image.get_rect(center = self.calibrate_light_blue_spinner.get_rect(topleft = (575, 645)).center)
            self.game.display.blit(self.calibrate_gauge, (1105, 670))
            self.game.display.blit(self.calibrate_button, (1150, 770))
            self.game.display.blit(self.calibrate_gauge_t, (1100, 670))
            self.game.display.blit(rotated_image, new_rect)


        elif self.calibrate_colour == "LIGHT BLUE":
            # Yellow Spinner
            self.game.display.blit(self.calibrate_wire1, (795, 195))
            self.game.display.blit(self.calibrate_yellow_spinner, (575, 105))
            self.game.display.blit(self.calibrate_gauge, (1105, 150))
            self.game.display.blit(self.calibrate_button, (1150, 250))
            pygame.draw.rect(self.game.display, (255, 255, 0), (1105, 150, 240, 58)) # gauge rect
            self.game.display.blit(self.calibrate_gauge_t, (1100, 150))
            
            # blue spinner                
            self.game.display.blit(self.calibrate_gauge, (1105, 400))
            self.game.display.blit(self.calibrate_button, (1150, 500))
            self.game.display.blit(self.calibrate_wire2, (795, 460))
            pygame.draw.rect(self.game.display, (0, 0, 255), (1105, 400, 240, 58)) # gauge rect
            self.game.display.blit(self.calibrate_blue_spinner, (575, 375))
            self.game.display.blit(self.calibrate_gauge_t, (1100, 400))

            # Light blue spinner
            rotated_image = pygame.transform.rotate(self.calibrate_light_blue_spinner, self.calibrate_rotate)
            new_rect = rotated_image.get_rect(center = self.calibrate_light_blue_spinner.get_rect(topleft = (575, 645)).center)
            
            self.game.display.blit(self.calibrate_gauge, (1105, 670))
            random_int = random.randint(0, 50)
            pygame.draw.rect(self.game.display, (0, 255, 255), (1105, 670, random_int, 58))
            self.game.display.blit(self.calibrate_button, (1150, 770))
            self.calibrate_button_rect = pygame.Rect(1150, 770, 143, 50)
            pygame.draw.rect(self.game.display, (255, 255, 0), self.calibrate_button_rect, 2) # button rect

            if self.calibrate_rotate < 10 or self.calibrate_rotate > 350:
                self.game.display.blit(self.calibrate_wire3, (795, 730))
                pygame.draw.rect(self.game.display, (0, 255, 255), (1105, 670, 240, 58)) # gauge rect
                pygame.draw.rect(self.game.display, (0, 255, 0), self.calibrate_button_rect, 2) # button rect
                if self.calibrate_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                    if self.power_task == "REACTORS":
                        self.current_task = "TURN ON POWER ELECTRICAL"
                        self.calibrate_colour = "YELLOW"
                        self.game.task_running = False
                        self.power_task = "ELECTRICAL"
                    
                    elif self.power_task == "ELECTRICAL":
                        self.current_task = "PICK UP FUEL"
                        self.calibrate_colour = "YELLOW"
                        self.game.task_running = False
                        self.power_task = "DONE"
                        self.powered = True

            self.game.display.blit(self.calibrate_gauge_t, (1100, 670))
            self.game.display.blit(rotated_image, new_rect)

    def turn_on_power_electrical(self):
        self.electrical_task_rect = pygame.Rect(348 + self.scrollx, 1202 + self.scrolly, 33, 24)
        if pygame.Rect.colliderect(self.player_hitbox, self.electrical_task_rect):
            pygame.draw.rect(self.game.display, (0, 255, 0), self.electrical_task_rect, 2)
            self.use_button.set_alpha(255)
        
        else:
            pygame.draw.rect(self.game.display, (255, 255, 0), self.electrical_task_rect, 2)
            self.use_button.set_alpha(128)

        if pygame.Rect.colliderect(self.player_hitbox, self.electrical_task_rect) and self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
            self.game.task_running = True

        if self.game.task_running:
            self.calibrate_task()

    def turn_on_power_reactor(self):
        self.reactor_task_rect = pygame.Rect(-835 + self.scrollx, 1000 + self.scrolly, 56, 60)
        if pygame.Rect.colliderect(self.player_hitbox, self.reactor_task_rect):
            pygame.draw.rect(self.game.display, (0, 255, 0), self.reactor_task_rect, 2)
            self.use_button.set_alpha(255)
        
        else:
            pygame.draw.rect(self.game.display, (255, 255, 0), self.reactor_task_rect, 2)
            self.use_button.set_alpha(128)

        if pygame.Rect.colliderect(self.player_hitbox, self.reactor_task_rect) and self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
            self.game.task_running = True

        if self.game.task_running:
            self.calibrate_task()
    
    def pick_up_fuel(self):
        fuel_rect = pygame.Rect(750 + self.scrollx, 1700 + self.scrolly, 36, 47)
        
        if pygame.Rect.colliderect(self.player_hitbox, fuel_rect):
            pygame.draw.rect(self.game.display, (0, 255, 0), fuel_rect, 2)
            self.use_button.set_alpha(255)

            if self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                self.current_task = "FUEL LOWER ENGINE"
                self.use_button.set_alpha(128)
                self.show_fuel = False
        
        else:
            pygame.draw.rect(self.game.display, (255, 255, 0), fuel_rect, 2)
            self.use_button.set_alpha(128)

    def fuel_engine(self, lower):
        if lower:
            self.fuel_task_rect = pygame.Rect(-510 + self.scrollx, 1335 + self.scrolly, 36, 24)
            pygame.draw.rect(self.game.display, (255, 255, 0), self.fuel_task_rect, 2)
        
            if pygame.Rect.colliderect(self.player_hitbox, self.fuel_task_rect):
                pygame.draw.rect(self.game.display, (0, 255, 0), self.fuel_task_rect, 2)
                self.use_button.set_alpha(255)

                if self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                    self.game.task_running = True
                    self.use_button.set_alpha(128)

        if not lower:
            self.fuel_task_rect = pygame.Rect(-445 + self.scrollx, 295 + self.scrolly, 36, 24)
            pygame.draw.rect(self.game.display, (255, 255, 0), self.fuel_task_rect, 2)
        
            if pygame.Rect.colliderect(self.player_hitbox, self.fuel_task_rect):
                pygame.draw.rect(self.game.display, (0, 255, 0), self.fuel_task_rect, 2)
                self.use_button.set_alpha(255)

                if self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                    self.game.task_running = True
                    self.use_button.set_alpha(128)

        if self.game.task_running:
            base_rect = (500, 100, 614, 890)
            pygame.draw.rect(self.game.display, (0, 0, 0), base_rect) #background
            pygame.draw.rect(self.game.display, (255, 255, 0), self.engine_fuel_rect) # Fuel level
            self.game.display.blit(self.fuel_wires, (1100, 850))
            self.game.display.blit(self.fuel_base2, (1150, 775))
            self.game.display.blit(self.fuel_button, (1195, 815))
            button_rect = pygame.Rect(1195, 815, 137, 139)
            
            if button_rect.collidepoint(self.game.mouse_pos): 
                pygame.draw.rect(self.game.display, (0, 255, 0), button_rect, 2)
                
                if self.game.left_click:
                    if self.engine_fuel_rect.height > 10:
                        self.engine_fuel_rect.height -= 10
                        self.engine_fuel_rect.height -= 10
                        self.engine_fuel_rect.bottomleft = (500, 780)
                    else:
                        self.game.task_running = False
                        if lower:
                            self.current_task = "FUEL UPPER ENGINE"
                            self.engine_fuel_rect = pygame.Rect(500, 200, 614, 580)
                            self.use_button.set_alpha(128)
                        elif not lower:
                            self.current_task = "BIOMETERIC SCAN"
                            self.counter = 0
                            self.fueled = True

            else:
                pygame.draw.rect(self.game.display, (255, 255, 0), button_rect, 2)


            self.game.display.blit(self.fuel_base1, (500, 100))

    def biometric_scan(self):
        if not self.game.task_running:
            scan_rect = pygame.Rect(325 + self.scrollx, 960 + self.scrolly, 147, 93)
            pygame.draw.rect(self.game.display, (255, 255, 0), scan_rect, 2)
            
            if pygame.Rect.colliderect(self.player_hitbox, scan_rect):
                pygame.draw.rect(self.game.display, (0, 255, 0), scan_rect, 2)
                self.use_button.set_alpha(255)

                if self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                    self.game.task_running = True
                    self.use_button.set_alpha(128)       
        
        else:
            self.scrollx = 530
            self.scrolly = -467
            self.initiate_scan = True
            if self.powered and self.initiate_scan:
                self.game.display.blit(self.medbay_scan[self.medbay_scan_index], (350 + (self.medbay_scan_index * 7) + self.scrollx, 980 + -(self.medbay_scan_index * 20) + self.scrolly))
            
            self.game.display.blit(self.medbay_wire, (1325, 200))
            self.game.display.blit(self.medbay_base_top, (500, 100))
            self.game.display.blit(self.medbay_base_bottom, (500, 700))

            if self.counter > 820:
                if self.counter < 1000:
                    self.game.draw_text("Biometric Signature Authorized", 50, 950, 900, (0, 255, 0))
                
                else:
                    self.current_task = "NAVIGATE SHIP"
                    self.counter = 0
                    self.game.task_running = False

            else:
                pygame.draw.rect(self.game.display, (0, 255, 0), (545, 735, self.counter, 60))
                self.game.draw_text("Logging into system using biometric signature...", 50, 950, 300, (255, 255, 255))
                self.game.draw_text("Scan will complete shortly...", 50, 950, 900, (255, 255, 255))
            
            self.counter += 5
        
    def chart_course(self):
        if not self.game.task_running:
            task_rect = pygame.Rect(2531 + self.scrollx, 905 + self.scrolly, 76, 158)
            pygame.draw.rect(self.game.display, (255, 255, 0), task_rect, 2)
            
            if pygame.Rect.colliderect(self.player_hitbox, task_rect):
                pygame.draw.rect(self.game.display, (0, 255, 0), task_rect, 2)
                self.use_button.set_alpha(255)

                if self.use_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                    self.game.task_running = True
                    self.use_button.set_alpha(128)

        else:
            self.game.display.blit(self.upload_base, (350, 100))
            self.game.draw_text("Upload Auto-Pilot Software", 90, 950, 225)
            self.game.draw_text("Computer", 75, 610, 600)
            self.game.draw_text("Ship", 75, 1285, 600)
            self.game.display.blit(pygame.transform.scale(self.files, (300, 236)), (self.filesx, self.filesy))
            self.game.display.blit(self.folder_animation[self.folder_animation_counter], (482, 375))
            self.game.display.blit(self.folder_animation[self.folder_animation_counter], (1150, 375))
            self.game.display.blit(self.folder_upload_button, (850, 550))
            upload_button_rect = pygame.Rect(850, 550, 200, 62)
            self.game.draw_text("Upload Progress", 60, 950, 675)
            self.upload_progress_rect.width = self.folder_progress * 44 # Final form(440, 700, 1017, 60)
            self.game.display.blit(self.folder_progress_bar, (440, 700))
            pygame.draw.rect(self.game.display, (0, 255, 0), self.upload_progress_rect)
            

            if not self.begin_upload:
                pygame.draw.rect(self.game.display, (255, 255, 0), upload_button_rect, 5)

            else:
                pygame.draw.rect(self.game.display, (0, 255, 0), upload_button_rect, 5)
            
            if upload_button_rect.collidepoint(self.game.mouse_pos) and self.game.left_click:
                self.begin_upload = True
            
            
            if self.counter % 25 == 0 and self.begin_upload and not self.first_folder:
                self.folder_animation_counter += 1
                self.folder_progress += 1
                
                if self.folder_animation_counter < 4:
                    pass
                else:
                    self.first_folder = True
                    self.counter = 0

            elif self.counter % 25 == 0 and self.begin_upload and self.first_folder and not self.close_files:
                    self.filesx += 50
                    self.folder_progress += 1
                    if self.filesx > 1150:
                        self.close_files = True

            elif self.counter % 25 == 0 and self.begin_upload and self.first_folder and self.close_files:
                self.folder_animation_counter -= 1
                self.folder_progress += 1
                if self.folder_animation_counter >= 0:
                    pass
                else:
                    self.upload_progress_rect.right = 1017
                    self.current_task = "END GAME"
                    self.counter = 0
                    self.begin_upload = False
            
            self.counter += 1

    def blit_tasks(self):
        if self.current_task == "TURN ON POWER REACTOR":
            self.game.current_level = 4
            self.turn_on_power_reactor()
            self.game.draw_text("Level 4", 100, self.level_textx + 25, self.level_texty, (255, 255, 255))
            self.game.draw_text("Turn on power", 50, self.level_textx + 25, self.level_texty + 100, (255, 255, 255))
            self.game.draw_text("Task is in Reactors", 50, self.level_textx + 25, self.level_texty + 150, (255, 255, 255))

        elif self.current_task == "TURN ON POWER ELECTRICAL":
            self.game.current_level = 5
            self.turn_on_power_electrical()
            self.game.draw_text("Level 5", 100, self.level_textx + 25, self.level_texty, (255, 255, 255))
            self.game.draw_text("Turn on power", 50, self.level_textx + 25, self.level_texty + 100, (255, 255, 255))
            self.game.draw_text("Task is in Electrical", 50, self.level_textx + 25, self.level_texty + 150, (255, 255, 255))


        elif self.current_task == "PICK UP FUEL":
            self.game.current_level = 6
            self.pick_up_fuel()
            self.game.draw_text("Level 6", 100, self.level_textx + 25, self.level_texty, (255, 255, 255))
            self.game.draw_text("Pick Up Engine Fuel", 50, self.level_textx + 25, self.level_texty + 100, (255, 255, 255))
            self.game.draw_text("Task is in Storage", 50, self.level_textx + 25, self.level_texty + 150, (255, 255, 255))

        elif self.current_task == "FUEL LOWER ENGINE":
            self.game.current_level = 7
            self.game.draw_text("Level 7", 100, self.level_textx + 25, self.level_texty, (255, 255, 255))
            self.game.draw_text("Fuel Lower Engine", 50, self.level_textx + 25, self.level_texty + 100, (255, 255, 255))
            self.game.draw_text("Task is in", 50, self.level_textx + 25, self.level_texty + 150, (255, 255, 255))
            self.game.draw_text("Lower Engine Room", 50, self.level_textx + 25, self.level_texty + 200, (255, 255, 255))
            self.fuel_engine(lower=True)

        elif self.current_task == "FUEL UPPER ENGINE":
            self.game.current_level = 8
            self.game.draw_text("Level 8", 100, self.level_textx + 25, self.level_texty, (255, 255, 255))
            self.game.draw_text("Fuel Upper Engine", 50, self.level_textx + 25, self.level_texty + 100, (255, 255, 255))
            self.game.draw_text("Task is in", 50, self.level_textx + 25, self.level_texty + 150, (255, 255, 255))
            self.game.draw_text("Upper Engine Room", 50, self.level_textx + 25, self.level_texty + 200, (255, 255, 255))
            self.fuel_engine(lower=False)

        elif self.current_task == "BIOMETERIC SCAN":
            self.game.current_level = 9
            self.game.draw_text("Level 9", 100, self.level_textx + 25, self.level_texty, (255, 255, 255))
            self.game.draw_text("Complete Biometric Scan", 50, self.level_textx + 50, self.level_texty + 100, (255, 255, 255))
            self.game.draw_text("Task is in Medbay", 50, self.level_textx + 25, self.level_texty + 150, (255, 255, 255))
            self.biometric_scan()
        
        elif self.current_task == "NAVIGATE SHIP":
            self.game.current_level = 10
            self.game.draw_text("Level 10", 100, self.level_textx + 25, self.level_texty, (255, 255, 255))
            self.game.draw_text("Update Ship's Auto Pilot", 50, self.level_textx + 50, self.level_texty + 100, (255, 255, 255))
            self.game.draw_text("Task is in Navigation", 50, self.level_textx + 50, self.level_texty + 150, (255, 255, 255))
            self.chart_course()

        elif self.current_task == "END GAME":
            self.run_display = False
            self.reset()
            self.game.curr_menu = self.game.main_menu
            

        

    # blits all the map sprites
    def background(self):
        if self.border_color[3] == 0:
            self.draw_boundaries()
            self.game.display.blit(self.stars, (0,0))
            self.load_cafeteria()
            self.load_nav()
            self.game.display.blit(self.O2_nav_weap_hallway, (1675 + self.scrollx, 660 + self.scrolly))
            self.load_weapons()
            self.game.display.blit(self.O2_nav_weap_task, (2210 + self.scrollx, 890 + self.scrolly))
            self.load_oxygen()
            self.game.display.blit(self.storage_shield_hallway, (1105 + self.scrollx, 1477 + self.scrolly))
            self.load_shield()
            self.load_admin()
            self.load_electrical()
            self.load_storage()
            self.load_comms()
            self.load_engines()
            self.load_medbay()
            self.load_security()
            self.load_reactor()

        else:
            self.game.display.blit(self.stars, (0,0))
            self.load_cafeteria()
            self.load_nav()
            self.game.display.blit(self.O2_nav_weap_hallway, (1675 + self.scrollx, 660 + self.scrolly))
            self.load_weapons()
            self.game.display.blit(self.O2_nav_weap_task, (2210 + self.scrollx, 890 + self.scrolly))
            self.load_oxygen()
            self.game.display.blit(self.storage_shield_hallway, (1105 + self.scrollx, 1477 + self.scrolly))
            self.load_shield()
            self.load_admin()
            self.load_electrical()
            self.load_storage()
            self.load_comms()
            self.load_engines()
            self.load_medbay()
            self.load_security()
            self.load_reactor()
            self.draw_boundaries()



    # spawn animation
    def spawn(self):
        self.game.display.blit(pygame.transform.scale(self.idle[0], (50, 77)), (self.playerx, self.playery))
        self.spawned = True

    # check keyboard input
    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
        self.run_display = False

        boundary = self.boundaries()

        if self.game.move_f:
            if not boundary[0]:
                self.scrolly += 8
                self.status = "walking_r"
                self.input = True
                self.idle_left = False
            
            elif boundary[0] and boundary[1] == 'lf':
                self.scrolly += 8
                self.scrollx -= 8
                self.status = "walking_r"
                self.input = True
                self.idle_left = False
            
            elif boundary[0] and boundary[1] == 'rf':
                self.scrollx += 8
                self.scrolly += 8
                self.status = "walking_r"
                self.input = True
                self.idle_left = False
                
            
            elif boundary[0] and boundary[1] != 'f' and boundary[1] != 'lfc'  and boundary[1] != 'rfc':
                self.scrolly += 8
                self.status = "walking_r"
                self.input = True
                self.idle_left = False   

        if self.game.move_b:
            if not boundary[0]:
                self.input = True
                self.scrolly -= 8
                self.status = "walking_l"
                self.idle_left = True
            
            elif boundary[0] and boundary[1] == 'rb':
                self.scrollx += 8
                self.scrolly -= 8
                self.status = "walking_l"
                self.input = True
                self.idle_left = True
            
            elif boundary[0] and boundary[1] == 'lb':
                self.scrollx -= 8
                self.scrolly -= 8
                self.status = "walking_r"
                self.input = True
                self.idle_left = False
            
            elif boundary[0] and boundary[1] != 'b' and boundary[1] != 'rbc' and boundary[1] != 'lbc':
                self.scrolly -= 8
                self.status = "walking_l"
                self.input = True
                self.idle_left = True
                

        if self.game.move_r:
            if not boundary[0]:
                self.input = True
                self.scrollx -= 8
                self.status = "walking_r"
                self.idle_left = False
            
            elif boundary[0] and boundary[1] == 'rf':
                self.scrollx -= 8
                self.scrolly -= 8
                self.status = "walking_r"
                self.input = True
                self.idle_left = False

            elif boundary[0] and boundary[1] == 'rb':
                self.scrollx -= 8
                self.scrolly += 8
                self.status = "walking_r"
                self.input = True
                self.idle_left = False
            
            elif boundary[0] and boundary[1] != 'r' and boundary[1] != 'rfc' and boundary[1] != 'rbc':
                self.scrollx -= 8
                self.status = "walking_r"
                self.input = True
                self.idle_left = False
            
        if self.game.move_l:
            if not boundary[0]:
                self.input = True
                self.scrollx += 8
                self.status = "walking_l"
                self.idle_left = True
            
            elif boundary[0] and boundary[1] == 'lf':
                self.scrollx += 8
                self.scrolly -= 8
                self.status = "walking_l"
                self.input = True
                self.idle_left = True
            
            elif boundary[0] and boundary[1] == 'lb':
                self.scrollx += 8
                self.scrolly += 8
                self.status = "walking_l"
                self.input = True
                self.idle_left = True

            elif boundary[0] and boundary[1] != 'l' and boundary[1] != 'lfc' and boundary[1] != 'lbc':
                self.scrollx += 8
                self.status = "walking_l"
                self.input = True
                self.idle_left = True
            
    
        if not self.game.move_l and not self.game.move_r and not self.game.move_f and not self.game.move_b and not self.idle_left:
            self.status = "idle_r"
        
        elif not self.game.move_l and not self.game.move_r and not self.game.move_f and not self.game.move_b and self.idle_left:
            self.status = "idle_l"
    

    # update player animaton according to input
    def check_status(self):
        if self.status == "idle_r" and not self.idle_left:
            self.game.display.blit(pygame.transform.scale(self.idle[0], (50, 77)), (self.playerx, self.playery))
            if self.border_color[3] != 0:
                pygame.draw.rect(self.game.display, self.border_color, self.player_hitbox, 2)

        if self.status == "idle_l" and self.idle_left:
            self.game.display.blit(pygame.transform.scale(self.idle[1], (50, 77)), (self.playerx, self.playery))
            if self.border_color[3] != 0:
                pygame.draw.rect(self.game.display, self.border_color, self.player_hitbox, 2)
        
        if self.status == "walking_r":
            self.game.display.blit(pygame.transform.scale(self.walk[self.walk_counter], (50, 77)), (self.playerx, self.playery))
            self.walk_counter = (self.walk_counter + 1) % len(self.walk)
            if self.border_color[3] != 0:
                pygame.draw.rect(self.game.display, self.border_color, self.player_hitbox, 2)
        
        if self.status == "walking_l":
            self.game.display.blit(pygame.transform.flip(pygame.transform.scale(self.walk[self.walk_counter], (50, 77)), True, False), (self.playerx, self.playery))
            self.walk_counter = (self.walk_counter + 1) % len(self.walk)
            if self.border_color[3] != 0:
                pygame.draw.rect(self.game.display, self.border_color, self.player_hitbox, 2)

    # collide line line function deternmines if player is in contact with a line
    def collideLineLine(self, Player0, Player1, Boundary0, Boundary1):  
        d = (Player1[0]-Player0[0]) * (Boundary1[1]-Boundary0[1]) + (Player1[1]-Player0[1]) * (Boundary0[0]-Boundary1[0]) 

        if d == 0:
            return False

        t = ((Boundary0[0]-Player0[0]) * (Boundary1[1]-Boundary0[1]) + (Boundary0[1]-Player0[1]) * (Boundary0[0]-Boundary1[0])) / d
        u = ((Boundary0[0]-Player0[0]) * (Player1[1]-Player0[1]) + (Boundary0[1]-Player0[1]) * (Player0[0]-Player1[0])) / d
        return 0 <= t <= 1 and 0 <= u <= 1

    # collide RectLine Function determines if a line on player rect is in contact with angled line
    def collideRectLine(self, player, line_p1, line_p2):
        return (self.collideLineLine(line_p1, line_p2, player.topleft, player.bottomleft) or self.collideLineLine(line_p1, line_p2, player.bottomleft, player.bottomright) or 
            self.collideLineLine(line_p1, line_p2, player.bottomright, player.topright) or self.collideLineLine(line_p1, line_p2, player.topright, player.topleft))

    # boundaries function is used to determine what happens when player hitbox interferes with boundary hitbox
    def boundaries(self):
        # cafeteria boundaries
        def cafeteria_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.caf_tl_s):
                if self.collideRectLine(self.player_hitbox, *self.caf_tl_a_coords) or pygame.Rect.colliderect(self.player_hitbox, self.caf_hallway_top_s):
                    return True, "lfc"
                return True, "l"

            elif self.collideRectLine(self.player_hitbox, *self.caf_tl_a_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.caf_tl_s):
                    return True, "lfc"
                elif pygame.Rect.colliderect(self.player_hitbox, self.caf_ts):
                    return True, "lfc"
                return True, "lf"

            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_ts):
                if self.collideRectLine(self.player_hitbox, *self.caf_tl_a_coords):
                    return True, "lfc"
                
                elif self.collideRectLine(self.player_hitbox, *self.caf_tr_a_coords):
                    return True, "rfc"
                return True, "f"
            
            elif self.collideRectLine(self.player_hitbox, *self.caf_tr_a_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.caf_tr_s):
                    return True, "rfc"
                return True, "rf"

            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_tr_s):
                if pygame.Rect.colliderect(self.player_hitbox, self.weap_hallway_top):
                    return True, 'rfc'
                return True, "r"

            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_br_s):
                if self.collideRectLine(self.player_hitbox, *self.caf_br_a_coords):
                    return True, 'rbc'
                
                elif pygame.Rect.colliderect(self.player_hitbox, self.weap_hallway_bot):
                    return True, 'rbc'
                return True, "r"
            
            elif self.collideRectLine(self.player_hitbox, *self.caf_br_a_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.caf_br_s) or pygame.Rect.colliderect(self.player_hitbox, self.caf_bs_r):
                    return True, "rbc"
                return True, 'rb'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_bs_r):
                if pygame.Rect.colliderect(self.player_hitbox, self.sac_rt):
                    return True, 'rbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_bs_l):
                if pygame.Rect.colliderect(self.player_hitbox, self.sac_ls):
                    return True, 'lbc'

                elif self.collideRectLine(self.player_hitbox, *self.caf_bl_a_coords):
                    return True, 'lbc'

                return True, 'b'

            elif self.collideRectLine(self.player_hitbox, *self.caf_bl_a_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.caf_bs_r) or pygame.Rect.colliderect(self.player_hitbox, self.caf_bl_s):
                    return True, 'lbc'
                    
                return True, 'lb'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_bl_s):
                if pygame.Rect.colliderect(self.player_hitbox, self.caf_hallway_br_s):
                    return True, 'lbc'
                return True, 'l'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_hallway_top_s):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_rt):
                    return True, 'rfc'
                return True, 'f'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_hallway_br_s):
                if pygame.Rect.colliderect(self.player_hitbox, self.medbay_0r):
                    return True, 'rbc'
                return True, 'b'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_hallway_bl_s):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_rb):
                    return True, 'rbc'

                elif pygame.Rect.colliderect(self.player_hitbox, self.medbay_0l):
                    return True, 'lbc'

                return True, 'b'
            
            return False, "N/A"
        
        # Cafeteria result
        result = cafeteria_boundaries(self)
        if result[0]:
            return result
        
        def weapons_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.weap_hallway_top):
                if pygame.Rect.colliderect(self.player_hitbox, self.weap_tl):
                    return True, 'lfc'
                return True, 'f'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.weap_tl):
                if pygame.Rect.colliderect(self.player_hitbox, self.weap_ts):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.weap_ts):
                if self.collideRectLine(self.player_hitbox, *self.weap_tr_a_coords):
                    return True, 'rfc'
                return True, 'f'

            elif self.collideRectLine(self.player_hitbox, *self.weap_tr_a_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.weap_rs):
                    return True, 'rfc'
                return True, 'rf'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.weap_rs):
                if pygame.Rect.colliderect(self.player_hitbox, self.weap_brs):
                    return True, 'rbc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.weap_brs):
                if pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_0r):
                    return True, 'rbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.weap_bls):
                if self.collideRectLine(self.player_hitbox, *self.weap_bl_a_coords):
                    return True, 'lbc'
                return True, 'b'
            
            elif self.collideRectLine(self.player_hitbox, *self.weap_bl_a_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.weap_hallway_bot):
                    return True, 'lbc'
                return True, 'lb'

            elif pygame.Rect.colliderect(self.player_hitbox, self.weap_hallway_bot):
                return True, 'b'
            
            return False, "N/A"
        
        # weapons result
        result = weapons_boundaries(self)
        if result[0]:
            return result

        def Oxygen_nav_weap_hallway_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_0r):
                if pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_1r):
                    return True, 'rfc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_1r):
                if pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_2r):
                    return True, 'rfc'
                return True, 'f'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_2r):
                if pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_3r):
                    return True, 'rfc'
                return True, 'r'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_3r):
                if pygame.Rect.colliderect(self.player_hitbox, self.nav_tl):
                    return True, 'lfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_4r):
                if pygame.Rect.colliderect(self.player_hitbox, self.nav_bl):
                    return True, 'lbc'
                elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_5r):
                    return True, 'rbc'
                return True, 'b'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_5r):
                if pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_6r):
                    return True, 'rbc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_6r):
                if pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_7r):
                    return True, 'rbc'
                return True, 'b'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_7r):
                if pygame.Rect.colliderect(self.player_hitbox, self.shield_tls):
                    return True, 'rfc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_0l):
                if pygame.Rect.colliderect(self.player_hitbox, self.oxygen_top):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_1l):
                if pygame.Rect.colliderect(self.player_hitbox, self.oxygen_bottom):
                    return True, 'lbc'

                elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_2l):
                    return True, 'lfc'
                return True, 'l'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_2l):
                if pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_3l):
                    return True, 'lfc'
                return True, 'f'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.Oxygen_nav_weap_hall_3l):
                if self.collideRectLine(self.player_hitbox, *self.shield_ta_coords):
                    return True, 'lfc'
                return True, 'l'

            return False, 'N/A'
        
        # 0xygen, navigation and weapons hallway result
        result = Oxygen_nav_weap_hallway_boundaries(self)
        if result[0]:
            return result

        def oxygen_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.oxygen_top):
                if self.collideRectLine(self.player_hitbox, *self.oxygen_angle_coords):
                    return True, 'lfc'
                return True, 'f'
            
            elif self.collideRectLine(self.player_hitbox, *self.oxygen_angle_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.oxygen_bottom):
                    return True,'lbc'
                return True, 'lf'

            elif pygame.Rect.colliderect(self.player_hitbox, self.oxygen_bottom):
                return True, 'b'
            return False, 'N/A'
            
        
        result = oxygen_boundaries(self)
        if result[0]:
            return result

        def navigation_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.nav_tl):
                if pygame.Rect.colliderect(self.player_hitbox, self.nav_ts):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.nav_ts):
                if self.collideRectLine(self.player_hitbox, *self.nav_tr_a_coords):
                    return True, 'rfc'
                return True, 'f'

            elif self.collideRectLine(self.player_hitbox, *self.nav_tr_a_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.nav_rs):
                    return True, 'rfc'
                return True, 'rf'

            elif pygame.Rect.colliderect(self.player_hitbox, self.nav_rs):
                if self.collideRectLine(self.player_hitbox, *self.nav_br_a_coords):
                    return True, 'rbc'
                return True, 'r'

            elif self.collideRectLine(self.player_hitbox, *self.nav_br_a_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.nav_bs):
                    return True, 'rbc'
                return True, 'rb'

            elif pygame.Rect.colliderect(self.player_hitbox, self.nav_bs):
                if pygame.Rect.colliderect(self.player_hitbox, self.nav_bl):
                    return True, 'lbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.nav_bl):
                return True, 'l'
            
            return False, 'N/A'

        result = navigation_boundaries(self)
        if result[0]:
            return result

        def shield_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.shield_tls):
                if pygame.Rect.colliderect(self.player_hitbox, self.shield_rs):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.shield_rs):
                if self.collideRectLine(self.player_hitbox, *self.shield_ba_coords):
                    return True, 'rbc'
                return True, 'r'
            
            elif self.collideRectLine(self.player_hitbox, *self.shield_ba_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.shield_bs):
                    return True, 'rbc'
                return True, 'rb'

            elif pygame.Rect.colliderect(self.player_hitbox, self.shield_bs):
                if pygame.Rect.colliderect(self.player_hitbox, self.shield_lbs):
                    return True, 'lbc'

                elif pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_hbr):
                    return True, 'lbc'

                return True, 'b'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.shield_lbs):
                return True, 'l' 

            elif self.collideRectLine(self.player_hitbox, *self.shield_ta_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_ts):
                    return True, 'lfc'
                return True, 'lf'

            return False, 'N/A'

        result = shield_boundaries(self)
        if result[0]:
            return result

        def scs_hallway_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_ts):
                if pygame.Rect.colliderect(self.player_hitbox, self.storage_rt):
                    return True, 'rfc'
                return True, 'f'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_hbr):
                if pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_vbr):
                    return True, 'rbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_vbr):
                if pygame.Rect.colliderect(self.player_hitbox, self.comms_tr):
                    return True, 'rfc'
                return True, 'r'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_vbl):
                if pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_hbl):
                    return True, 'lbc'
                
                elif pygame.Rect.colliderect(self.player_hitbox, self.comms_tl):
                    return True, 'lfc'

                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.scs_hallway_hbl):
                if pygame.Rect.colliderect(self.player_hitbox, self.storage_rb):
                    return True, 'rbc'
                return True, 'b'

            return False, 'N/A'

        result = scs_hallway_boundaries(self)
        if result[0]:
            return result

        def comms_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.comms_tr):
                if pygame.Rect.colliderect(self.player_hitbox, self.comms_r):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.comms_r):
                if pygame.Rect.colliderect(self.player_hitbox, self.comms_b):
                    return True, 'rbc'
                return True, 'r'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.comms_b):
                if pygame.Rect.colliderect(self.player_hitbox, self.comms_l):
                    return True, 'lbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.comms_l):
                if pygame.Rect.colliderect(self.player_hitbox, self.comms_tl):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.comms_tl):
                return True, 'f'

            return False, 'N/A'

        result = comms_boundaries(self)
        if result[0]:
            return result

        def storage_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.storage_rb):
                if pygame.Rect.colliderect(self.player_hitbox, self.storage_br):
                    return True, 'rbc'
                return True, 'r'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.storage_br):
                if self.collideRectLine(self.player_hitbox, *self.storage_bla_coords):
                    return True, 'lbc'
                return True, 'b'

            elif self.collideRectLine(self.player_hitbox, *self.storage_bla_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.seeh_b0):
                    return True, 'lbc'
                return True, 'lb'

            elif pygame.Rect.colliderect(self.player_hitbox, self.storage_lt):
                if self.collideRectLine(self.player_hitbox, *self.storage_lta_coords):
                    return True, 'lfc'

                elif pygame.Rect.colliderect(self.player_hitbox, self.seeh_t0):
                    return True, 'lfc'
                    
                return True, 'l'
            
            elif self.collideRectLine(self.player_hitbox, *self.storage_lta_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.storage_tl):    
                    return True, 'lfc'
                return True, 'lf'

            elif pygame.Rect.colliderect(self.player_hitbox, self.storage_tl):  
                if pygame.Rect.colliderect(self.player_hitbox, self.sac_ls):
                    return True, 'lfc'  
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.storage_tr):
                if pygame.Rect.colliderect(self.player_hitbox, self.storage_rt) or pygame.Rect.colliderect(self.player_hitbox, self.sac_rb):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.storage_rt):
                return True, 'r'            
            
            return False, 'N/A'

        result = storage_boundaries(self)
        if result[0]:
            return result

        def sac_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.sac_ls):
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.sac_rt):
                if pygame.Rect.colliderect(self.player_hitbox, self.admin_top):
                    return True, 'rfc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.sac_rb):
                if pygame.Rect.colliderect(self.player_hitbox, self.admin_bh):
                    return True, 'rbc'
                return True, 'r'

            return False, 'N/A'

        result = sac_boundaries(self)
        if result[0]:
            return result

        def admin_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.admin_top):
                if pygame.Rect.colliderect(self.player_hitbox, self.admin_rs):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.admin_rs):
                if self.collideRectLine(self.player_hitbox, *self.admin_ra_coords):
                    return True, 'rbc'
                return True, 'r'

            elif self.collideRectLine(self.player_hitbox, *self.admin_ra_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.admin_bottom):
                    return True, 'rbc'
                return True, 'rb'

            elif pygame.Rect.colliderect(self.player_hitbox, self.admin_bottom):
                if pygame.Rect.colliderect(self.player_hitbox, self.admin_left):
                    return True, 'lbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.admin_left):
                if pygame.Rect.colliderect(self.player_hitbox, self.admin_bh):
                    return True, 'lbc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.admin_bh):
                return True, 'b'

            return False, 'N/A'
        
        result = admin_boundaries(self)
        if result[0]:
            return result

        def seeh_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.seeh_t0):
                if pygame.Rect.colliderect(self.player_hitbox,self.electrical_r5):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.seeh_t1):
                if pygame.Rect.colliderect(self.player_hitbox, self.seeh_t2):
                    return True, 'rfc'
                
                elif pygame.Rect.colliderect(self.player_hitbox,self.electrical_l):
                    return True, 'lfc'

                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.seeh_t2):
                if pygame.Rect.colliderect(self.player_hitbox, self.seeh_t3):
                    return True, 'rfc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.seeh_t3):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_rt):
                    return True, 'rfc'
                return True, 'f'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.seeh_b0):
                if pygame.Rect.colliderect(self.player_hitbox, self.seeh_b1):
                    return True, 'lbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.seeh_b1):
                if pygame.Rect.colliderect(self.player_hitbox, self.seeh_b2):
                    return True, 'lbc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.seeh_b2):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_rb):
                    return True, 'rbc'
                return True, 'b'

            return False, 'N/A'

        result = seeh_boundaries(self)
        if result[0]:
            return result

        def electrical_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox,self.electrical_l):
                if pygame.Rect.colliderect(self.player_hitbox,self.electrical_t):
                    return True, 'lfc'
                return True, 'l'
            
            elif pygame.Rect.colliderect(self.player_hitbox,self.electrical_t):
                if pygame.Rect.colliderect(self.player_hitbox,self.electrical_r0):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox,self.electrical_r0):
                if self.collideRectLine(self.player_hitbox, *self.electrical_r1_coords):
                    return True, 'rbc'
                return True, 'r'

            elif self.collideRectLine(self.player_hitbox, *self.electrical_r1_coords):
                if pygame.Rect.colliderect(self.player_hitbox,self.electrical_r2):
                    return True, 'rbc'
                return True, 'rb'

            elif pygame.Rect.colliderect(self.player_hitbox,self.electrical_r2):
                if self.collideRectLine(self.player_hitbox, *self.electrical_r3_coords):
                    return True, 'rbc'
                return True, 'r'

            elif self.collideRectLine(self.player_hitbox, *self.electrical_r3_coords):
                if pygame.Rect.colliderect(self.player_hitbox,self.electrical_r4):
                    return True, 'rbc'
                return True, 'rb'

            elif pygame.Rect.colliderect(self.player_hitbox,self.electrical_r4):
                if pygame.Rect.colliderect(self.player_hitbox,self.electrical_r5):
                    return True, 'rbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox,self.electrical_r5):
                return True, 'r'

            return False, 'N/A'

        result = electrical_boundaries(self)
        if result[0]:
            return result

        def lower_engine_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_rb):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_b):
                    return True, 'rbc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_b):
                if self.collideRectLine(self.player_hitbox, *self.l_engine_ba_coords):
                    return True, 'lbc'
                return True, 'b'

            elif self.collideRectLine(self.player_hitbox, *self.l_engine_ba_coords):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_lb):
                    return True, 'lbc'
                return True, 'lb'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_lb):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_eb):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_eb):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_v):
                    return True, 'lfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_v):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_et):
                    return True, 'lbc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_et):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_lt):
                    return True, 'lbc'
                return True, 'b'
            
            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_lt):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_tl):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_tl):
                if pygame.Rect.colliderect(self.player_hitbox, self.ers_lbv):
                    return True, 'lfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_tr):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_rt):
                    return True, 'rfc'

                elif pygame.Rect.colliderect(self.player_hitbox, self.ers_rbv):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_rt):
                return True, 'r'

            return False, 'N/A'
        
        result = lower_engine_boundaries(self)
        if result[0]:
            return result

        def ers_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.ers_lbv):
                if pygame.Rect.colliderect(self.player_hitbox, self.ers_lbh):
                    return True, 'lbc'
                return True, 'l'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.ers_lbh):
                if pygame.Rect.colliderect(self.player_hitbox, self.reactor_0rb):
                    return True, 'rbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.ers_lth):
                if pygame.Rect.colliderect(self.player_hitbox, self.ers_ltv):
                    return True, 'lfc'
                
                elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_0rt):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.ers_ltv):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_bl):
                    return True, 'lbc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.ers_rtv):
                if pygame.Rect.colliderect(self.player_hitbox, self.ers_rth):
                    return True, 'rfc'
                
                elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_br):
                    return True, 'rbc'

                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.ers_rth):
                if pygame.Rect.colliderect(self.player_hitbox, self.security_lt):
                    return True, 'lfc'
                return True, 'f'
                
            elif pygame.Rect.colliderect(self.player_hitbox, self.ers_rbh):
                if pygame.Rect.colliderect(self.player_hitbox, self.ers_rbv):
                    return True, 'rbc'
                
                elif pygame.Rect.colliderect(self.player_hitbox, self.security_lb):
                    return True, 'lbc'  

                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.ers_rbv):
                return True, 'r'

            return False, 'N/A'


        result = ers_boundaries(self)
        if result[0]:
            return result

        def reactor_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.reactor_0rb):
                if pygame.Rect.colliderect(self.player_hitbox, self.reactor_1rb):
                    return True, 'rbc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_1rb):
                if pygame.Rect.colliderect(self.player_hitbox, self.reactor_2rb):
                    return True, 'rbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_2rb):
                if pygame.Rect.colliderect(self.player_hitbox, self.reactor_bs):
                    return True, 'rbc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_bs):
                if self.collideRectLine(self.player_hitbox, *self.reactor_ba_coords):
                    return True, 'lbc'
                return True, 'b'

            elif self.collideRectLine(self.player_hitbox, *self.reactor_ba_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.reactor_ls):
                    return True, 'lbc'
                return True, 'lb'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_ls):
                if self.collideRectLine(self.player_hitbox, *self.reactor_ta_coords):
                    return True, 'lfc' 
                return True, 'l'
                
            elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_0rt):
                if pygame.Rect.colliderect(self.player_hitbox, self.reactor_1rt):
                    return True, 'rfc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_1rt):
                if pygame.Rect.colliderect(self.player_hitbox, self.reactor_2rt):
                    return True, 'rfc' 
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_2rt):
                if pygame.Rect.colliderect(self.player_hitbox, self.reactor_ts):
                    return True, 'rfc' 
                return True, 'r' 

            elif pygame.Rect.colliderect(self.player_hitbox, self.reactor_ts):
                if self.collideRectLine(self.player_hitbox, *self.reactor_ta_coords):
                    return True, 'lfc' 
                return True, 'f'

            elif self.collideRectLine(self.player_hitbox, *self.reactor_ta_coords):
                return True, 'lf' 

            return False, 'N/A'

        result = reactor_boundaries(self)
        if result[0]:
            return result

        def security_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.security_lt):
                if pygame.Rect.colliderect(self.player_hitbox, self.security_t):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.security_t):
                if pygame.Rect.colliderect(self.player_hitbox, self.security_r):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.security_r):
                if pygame.Rect.colliderect(self.player_hitbox, self.security_b):
                    return True, 'rbc'    
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.security_b):
                if pygame.Rect.colliderect(self.player_hitbox, self.security_lb):
                    return True, 'lbc'    
                return True, 'b'    
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.security_lb):
                return True, 'l'    

            return False, 'N/A'


        result = security_boundaries(self)
        if result[0]:
            return result

        def upper_engine_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_bl):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_lb):
                    return True, 'lbc'
                return True, 'b'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_lb):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_eb):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_eb):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_er):
                    return True, 'lfc'
                return True, 'f'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_er):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_et):
                    return True, 'lbc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_et):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_lt):
                    return True, 'lbc'
                elif self.collideRectLine(self.player_hitbox, *self.u_engine_lta_coords):
                    return True, 'l'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_lt):
                if self.collideRectLine(self.player_hitbox, *self.u_engine_lta_coords):
                    return True, 'lfc'
                return True, 'l'

            elif self.collideRectLine(self.player_hitbox, *self.u_engine_lta_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_t):
                    return True, 'lfc'
                return True, 'lf'

            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_t):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_rt):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_rt):
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_rb):
                if pygame.Rect.colliderect(self.player_hitbox, self.u_engine_br):
                    return True, 'rbc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.u_engine_br):
                return True, 'b'

            return False, 'N/A'


        result = upper_engine_boundaries(self)
        if result[0]:
            return result

        def medbay_boundaries(self):
            if pygame.Rect.colliderect(self.player_hitbox, self.medbay_0l):
                if pygame.Rect.colliderect(self.player_hitbox, self.medbay_1l):
                    return True, 'lfc'
                return True, 'l'

            elif pygame.Rect.colliderect(self.player_hitbox, self.medbay_1l):
                if pygame.Rect.colliderect(self.player_hitbox, self.medbay_2l):
                    return True, 'lfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.medbay_2l):
                if self.collideRectLine(self.player_hitbox, *self.medbay_3l_coords):
                    return True, 'lbc'
                return True, 'l'

            elif self.collideRectLine(self.player_hitbox, *self.medbay_3l_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.medbay_bottom):
                    return True, 'lbc'
                return True, 'lb'

            elif pygame.Rect.colliderect(self.player_hitbox, self.medbay_bottom):
                if pygame.Rect.colliderect(self.player_hitbox, self.medbay_4r):
                    return True, 'rbc'
                return True, 'b'

            elif pygame.Rect.colliderect(self.player_hitbox, self.medbay_0r):
                if pygame.Rect.colliderect(self.player_hitbox, self.medbay_1r):
                    return True, 'rfc'
                return True, 'r'

            elif pygame.Rect.colliderect(self.player_hitbox, self.medbay_1r):
                if pygame.Rect.colliderect(self.player_hitbox, self.medbay_2r):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox, self.medbay_2r):
                if self.collideRectLine(self.player_hitbox, *self.medbay_3r_coords):
                    return True, 'rfc'
                return True, 'r'

            elif self.collideRectLine(self.player_hitbox, *self.medbay_3r_coords):
                if pygame.Rect.colliderect(self.player_hitbox, self.medbay_4r):
                    return True, 'rfc'
                return True, 'rf'

            elif pygame.Rect.colliderect(self.player_hitbox, self.medbay_4r):
                return True, 'r'
            

            return False, 'N/A'


        result = medbay_boundaries(self)
        if result[0]:
            return result

        return False, 'N/A'

    # This function draws the boundary lines
    def draw_boundaries(self):
        # cafeteria and cafeteria hallway(left) lines
        def draw_cafeteria_boundaries(self):
            # top left straight
            self.caf_tl_s = pygame.draw.line(self.game.display, self.border_color, (492 + self.scrollx, 375 + self.scrolly), (492 + self.scrollx, 170 + self.scrolly), 5)

            # top left angle
            self.caf_tl_a_coords = [(490 + self.scrollx, 175 + self.scrolly), (660 + self.scrollx, 5 + self.scrolly)]
            self.caf_tl_a = pygame.draw.line(self.game.display, self.border_color, self.caf_tl_a_coords[0], self.caf_tl_a_coords[1], 5)

            # top straight
            self.caf_ts = pygame.draw.line(self.game.display, self.border_color, (658 + self.scrollx, 5 + self.scrolly), (1187 + self.scrollx, 5 + self.scrolly), 5)

            # top right angle
            self.caf_tr_a_coords = [(1187 + self.scrollx, 5 + self.scrolly), (1430 + self.scrollx, 250 + self.scrolly)]
            self.caf_tr_a = pygame.draw.line(self.game.display, self.border_color, self.caf_tr_a_coords[0], self.caf_tr_a_coords[1], 5)

            # top right straight
            self.caf_tr_s = pygame.draw.line(self.game.display, self.border_color, (1430 + self.scrollx, 250 + self.scrolly), (1430 + self.scrollx, 375 + self.scrolly), 5)

            # bottom right straight
            self.caf_br_s = pygame.draw.line(self.game.display, self.border_color, (1430 + self.scrollx, 535 + self.scrolly), (1430 + self.scrollx, 730 + self.scrolly), 5)

            # bottom right angle
            self.caf_br_a_coords = [(1430 + self.scrollx, 730 + self.scrolly), (1215 + self.scrollx, 945 + self.scrolly)]
            self.caf_br_a = pygame.draw.line(self.game.display, self.border_color, self.caf_br_a_coords[0], self.caf_br_a_coords[1], 5)

            # bottom right straight
            self.caf_bs_r = pygame.draw.line(self.game.display, self.border_color, (1215 + self.scrollx, 945 + self.scrolly), (1020 + self.scrollx, 945 + self.scrolly), 5)

            # bottom straight left
            self.caf_bs_l = pygame.draw.line(self.game.display, self.border_color, (701 + self.scrollx, 945 + self.scrolly), (890 + self.scrollx, 945 + self.scrolly), 5)
            
            # bottom left angle
            self.caf_bl_a_coords = [(701 + self.scrollx, 945 + self.scrolly), (490 + self.scrollx, 735 + self.scrolly)]
            self.caf_bl_a = pygame.draw.line(self.game.display, self.border_color, self.caf_bl_a_coords[0], self.caf_bl_a_coords[1], 5)

            # Bottom left straight
            self.caf_bl_s = pygame.draw.line(self.game.display, self.border_color, (492 + self.scrollx, 735 + self.scrolly), (492 + self.scrollx, 535 + self.scrolly), 5)

            # cafeteria hallway top straight
            self.caf_hallway_top_s = pygame.draw.line(self.game.display, self.border_color, (492 + self.scrollx, 372 + self.scrolly), (-225 + self.scrollx, 372 + self.scrolly), 5)
            
            # cafeteria hallway bottom right straight
            self.caf_hallway_br_s = pygame.draw.line(self.game.display, self.border_color, (492 + self.scrollx, 540 + self.scrolly), (312 + self.scrollx, 540 + self.scrolly), 5)

            # cafeteria hallway bottom left straight
            self.caf_hallway_bl_s = pygame.draw.line(self.game.display, self.border_color, (180 + self.scrollx, 540 + self.scrolly), (-225 + self.scrollx, 540 + self.scrolly), 5)

        def draw_weapons_boundaries(self):
            # weapons hallway top line
            self.weap_hallway_top = pygame.draw.line(self.game.display, self.border_color, (1430 + self.scrollx, 375 + self.scrolly), (1600 + self.scrollx, 375 + self.scrolly), 5)

            # weapons top left line
            self.weap_tl = pygame.draw.line(self.game.display, self.border_color, (1600 + self.scrollx, 375 + self.scrolly), (1600 + self.scrollx, 197 + self.scrolly), 5)

            # weapons top straight
            self.weap_ts = pygame.draw.line(self.game.display, self.border_color, (1600 + self.scrollx, 197 + self.scrolly), (1805 + self.scrollx, 197 + self.scrolly), 5)

            # weapons right angle
            self.weap_tr_a_coords = [(1805 + self.scrollx, 197 + self.scrolly), (1990 + self.scrollx, 380 + self.scrolly)]
            self.weap_tr_a = pygame.draw.line(self.game.display, self.border_color, self.weap_tr_a_coords[0], self.weap_tr_a_coords[1], 5)

            # weapons right straight
            self.weap_rs = pygame.draw.line(self.game.display, self.border_color, (1990 + self.scrollx, 380 + self.scrolly), (1990 + self.scrollx, 645 + self.scrolly), 5)

            # weapons bottom right straight 
            self.weap_brs = pygame.draw.line(self.game.display, self.border_color, (1990 + self.scrollx, 645 + self.scrolly), (1872 + self.scrollx, 645 + self.scrolly), 5)

            # weapons bottom left straight 
            self.weap_bls = pygame.draw.line(self.game.display, self.border_color, (1740 + self.scrollx, 645 + self.scrolly), (1690 + self.scrollx, 645 + self.scrolly), 5)
            
            # weapons bottom left angle
            self.weap_bl_a_coords = [(1690 + self.scrollx, 645 + self.scrolly), (1600 + self.scrollx, 535 + self.scrolly)]
            self.weap_bl_a = pygame.draw.line(self.game.display, self.border_color, self.weap_bl_a_coords[0], self.weap_bl_a_coords[1], 5)

            # weapons hallway bottom line
            self.weap_hallway_bot = pygame.draw.line(self.game.display, self.border_color, (1430 + self.scrollx, 535 + self.scrolly), (1600 + self.scrollx, 535 + self.scrolly), 5)
        
        def draw_Oxygen_nav_weap_hallway_boundaries(self):
            # numerically in order from top down
                # 0th line on the right side
            self.Oxygen_nav_weap_hall_0r =  pygame.draw.line(self.game.display, self.border_color, (1873 + self.scrollx, 645 + self.scrolly), (1873 + self.scrollx, 760 + self.scrolly), 5)
            
                # 1st line on the right side
            self.Oxygen_nav_weap_hall_1r =  pygame.draw.line(self.game.display, self.border_color, (1873 + self.scrollx, 760 + self.scrolly), (2070 + self.scrollx, 760 + self.scrolly), 5)
            
                # 2nd line on right side
            self.Oxygen_nav_weap_hall_2r =  pygame.draw.line(self.game.display, self.border_color, (2070 + self.scrollx, 760 + self.scrolly), (2070 + self.scrollx, 875 + self.scrolly), 5)

                # 3rd line on right side
            self.Oxygen_nav_weap_hall_3r =  pygame.draw.line(self.game.display, self.border_color, (2070 + self.scrollx, 875 + self.scrolly), (2310 + self.scrollx, 875 + self.scrolly), 5)

                # 4th line on right side
            self.Oxygen_nav_weap_hall_4r =  pygame.draw.line(self.game.display, self.border_color, (2070 + self.scrollx, 1035 + self.scrolly), (2310 + self.scrollx, 1035 + self.scrolly), 5)

                # 5th line on right side
            self.Oxygen_nav_weap_hall_5r =  pygame.draw.line(self.game.display, self.border_color, (2070 + self.scrollx, 1035 + self.scrolly), (2070 + self.scrollx, 1185 + self.scrolly), 5)

                # 6th line on right side
            self.Oxygen_nav_weap_hall_6r =  pygame.draw.line(self.game.display, self.border_color, (2070 + self.scrollx, 1185 + self.scrolly), (1872 + self.scrollx, 1185 + self.scrolly), 5)

                # 7th line on right side
            self.Oxygen_nav_weap_hall_7r =  pygame.draw.line(self.game.display, self.border_color, (1872 + self.scrollx, 1185 + self.scrolly), (1872 + self.scrollx, 1380 + self.scrolly), 5)

                # 0th line on left side
            self.Oxygen_nav_weap_hall_0l =  pygame.draw.line(self.game.display, self.border_color, (1740 + self.scrollx, 645 + self.scrolly), (1740 + self.scrollx, 760 + self.scrolly), 5)

                # 1st line on left side
            self.Oxygen_nav_weap_hall_1l = pygame.draw.line(self.game.display, self.border_color, (1935 + self.scrollx, 925 + self.scrolly), (1935 + self.scrollx, 1020 + self.scrolly), 5)

                # 2nd line on left side
            self.Oxygen_nav_weap_hall_2l = pygame.draw.line(self.game.display, self.border_color, (1735 + self.scrollx, 1020 + self.scrolly), (1935 + self.scrollx, 1020 + self.scrolly), 5)

                # 3rd line on left side
            self.Oxygen_nav_weap_hall_3l = pygame.draw.line(self.game.display, self.border_color, (1735 + self.scrollx, 1020 + self.scrolly), (1735 + self.scrollx, 1380 + self.scrolly), 5)
        

        def draw_oxygen_boundaries(self):
            # Oxygen top line
            self.oxygen_top =  pygame.draw.line(self.game.display, self.border_color, (1740 + self.scrollx, 760 + self.scrolly), (1475 + self.scrollx, 760 + self.scrolly), 5)
            
            # Oxygen Angle
            self.oxygen_angle_coords = [(1475 + self.scrollx, 760 + self.scrolly), (1350 + self.scrollx, 925 + self.scrolly)]
            self.oxygen_angle = pygame.draw.line(self.game.display, self.border_color, self.oxygen_angle_coords[0], self.oxygen_angle_coords[1], 5)
            
            # Oxygen bottom line
            self.oxygen_bottom =  pygame.draw.line(self.game.display, self.border_color, (1350 + self.scrollx, 925 + self.scrolly), (1935 + self.scrollx, 925 + self.scrolly), 5)
        

        def draw_navigation_boundaries(self):
            # Nav top left line
            self.nav_tl = pygame.draw.line(self.game.display, self.border_color, (2310 + self.scrollx, 875 + self.scrolly), (2310 + self.scrollx, 755 + self.scrolly), 5)

            # Nav top straight
            self.nav_ts = pygame.draw.line(self.game.display, self.border_color, (2310 + self.scrollx, 755 + self.scrolly), (2465 + self.scrollx, 755 + self.scrolly), 5)

            # nav top right angle
            self.nav_tr_a_coords = [(2465 + self.scrollx, 755 + self.scrolly), (2605 + self.scrollx, 875 + self.scrolly)]
            self.nav_tr_a = pygame.draw.line(self.game.display, self.border_color, self.nav_tr_a_coords[0], self.nav_tr_a_coords[1], 5)

            # nav right straight
            self.nav_rs = pygame.draw.line(self.game.display, self.border_color, (2605 + self.scrollx, 875 + self.scrolly), (2605 + self.scrollx, 1040 + self.scrolly), 5)

            # nav bottom right angle
            self.nav_br_a_coords = [(2605 + self.scrollx, 1040 + self.scrolly), (2465 + self.scrollx, 1150 + self.scrolly)]
            self.nav_br_a = pygame.draw.line(self.game.display, self.border_color, self.nav_br_a_coords[0], self.nav_br_a_coords[1], 5)

            # nav bottom straight
            self.nav_bs = pygame.draw.line(self.game.display, self.border_color, (2465 + self.scrollx, 1150 + self.scrolly), (2310 + self.scrollx, 1150 + self.scrolly), 5)

            # nav bottom left straight
            self.nav_bl = pygame.draw.line(self.game.display, self.border_color, (2310 + self.scrollx, 1150 + self.scrolly), (2310 + self.scrollx, 1035 + self.scrolly), 5)
            

        def draw_shield_boundaries(self):
            #shield top left straight
            self.shield_tls = pygame.draw.line(self.game.display, self.border_color, (1872 + self.scrollx, 1380 + self.scrolly), (1990 + self.scrollx, 1380 + self.scrolly), 5)

            # shield right straight
            self.shield_rs = pygame.draw.line(self.game.display, self.border_color, (1990 + self.scrollx, 1380 + self.scrolly), (1990 + self.scrollx, 1640 + self.scrolly), 5)

            # shield bottom angle
            self.shield_ba_coords = [(1990 + self.scrollx, 1640 + self.scrolly), (1805 + self.scrollx, 1820 + self.scrolly)]
            self.shield_ba = pygame.draw.line(self.game.display, self.border_color, self.shield_ba_coords[0], self.shield_ba_coords[1], 5)

            # sheild bottom straight
            self.shield_bs = pygame.draw.line(self.game.display, self.border_color, (1805 + self.scrollx, 1820 + self.scrolly), (1600 + self.scrollx, 1820 + self.scrolly), 5)

            # shield bottom left straight
            self.shield_lbs = pygame.draw.line(self.game.display, self.border_color, (1600 + self.scrollx, 1820 + self.scrolly), (1600 + self.scrollx, 1645 + self.scrolly), 5)

            # shield top left angle
            self.shield_ta_coords = [(1735 + self.scrollx, 1380 + self.scrolly), (1600 + self.scrollx, 1485 + self.scrolly)]
            self.shield_ta = pygame.draw.line(self.game.display, self.border_color, self.shield_ta_coords[0], self.shield_ta_coords[1], 5)


        def draw_scs_hallway_boundaries(self):
            # hallway top straight
            self.scs_hallway_ts = pygame.draw.line(self.game.display, self.border_color, (1600 + self.scrollx, 1485 + self.scrolly), (1095 + self.scrollx, 1485 + self.scrolly), 5)

            # hallway horizontal botom right straight
            self.scs_hallway_hbr = pygame.draw.line(self.game.display, self.border_color, (1600 + self.scrollx, 1645 + self.scrolly), (1510 + self.scrollx, 1645 + self.scrolly), 5)

            # hallway vertical botom right straight
            self.scs_hallway_vbr = pygame.draw.line(self.game.display, self.border_color, (1510 + self.scrollx, 1645 + self.scrolly), (1510 + self.scrollx, 1720 + self.scrolly), 5)

            # hallway vertical botom left straight
            self.scs_hallway_vbl = pygame.draw.line(self.game.display, self.border_color, (1375 + self.scrollx, 1645 + self.scrolly), (1375 + self.scrollx, 1720 + self.scrolly), 5)

            # hallway horizontal bottom left straight
            self.scs_hallway_hbl = pygame.draw.line(self.game.display, self.border_color, (1375 + self.scrollx, 1645 + self.scrolly), (1095 + self.scrollx, 1645 + self.scrolly), 5)


        def draw_comms_boundaries(self):
            # comms top right straight
            self.comms_tr = pygame.draw.line(self.game.display, self.border_color, (1510 + self.scrollx, 1720 + self.scrolly), (1560 + self.scrollx, 1720 + self.scrolly), 5)

            # right straight
            self.comms_r = pygame.draw.line(self.game.display, self.border_color, (1560 + self.scrollx, 1720 + self.scrolly), (1560 + self.scrollx, 1955 + self.scrolly), 5)

            # bottom straight
            self.comms_b = pygame.draw.line(self.game.display, self.border_color, (1560 + self.scrollx, 1955 + self.scrolly), (1140 + self.scrollx, 1955 + self.scrolly), 5) 

            # left straight
            self.comms_l = pygame.draw.line(self.game.display, self.border_color, (1140 + self.scrollx, 1720 + self.scrolly), (1140 + self.scrollx, 1955 + self.scrolly), 5) 

            # top left straight
            self.comms_tl = pygame.draw.line(self.game.display, self.border_color, (1140 + self.scrollx, 1720 + self.scrolly), (1375 + self.scrollx, 1720 + self.scrolly), 5) 


        def draw_storage_boundaries(self):
            # Right bottom straight
            self.storage_rb = pygame.draw.line(self.game.display, self.border_color, (1095 + self.scrollx, 1645 + self.scrolly), (1095 + self.scrollx, 2035 + self.scrolly), 5)

            # Bottom right straight
            self.storage_br = pygame.draw.line(self.game.display, self.border_color, (1095 + self.scrollx, 2035 + self.scrolly), (760 + self.scrollx, 2035 + self.scrolly), 5)

            # Bottom left angle
            self.storage_bla_coords = [(760 + self.scrollx, 2035 + self.scrolly), (582 + self.scrollx, 1843 + self.scrolly)]
            self.storage_bla = pygame.draw.line(self.game.display, self.border_color, self.storage_bla_coords[0], self.storage_bla_coords[1], 5)

            # left Top straight
            self.storage_lt = pygame.draw.line(self.game.display, self.border_color, (582 + self.scrollx, 1675 + self.scrolly), (582 + self.scrollx, 1390 + self.scrolly), 5)

            # left top angle
            self.storage_lta_coords = [(582 + self.scrollx, 1390 + self.scrolly), (710 + self.scrollx, 1265 + self.scrolly)]
            self.storage_lta = pygame.draw.line(self.game.display, self.border_color, self.storage_lta_coords[0], self.storage_lta_coords[1], 5)

            # top left straight
            self.storage_tl =  pygame.draw.line(self.game.display, self.border_color, (710 + self.scrollx, 1265 + self.scrolly), (890 + self.scrollx, 1265 + self.scrolly), 5)

            # top right straight
            self.storage_tr = pygame.draw.line(self.game.display, self.border_color, (1020 + self.scrollx, 1265 + self.scrolly), (1095 + self.scrollx, 1265 + self.scrolly), 5)

            # right top straight
            self.storage_rt = pygame.draw.line(self.game.display, self.border_color, (1095 + self.scrollx, 1265 + self.scrolly), (1095 + self.scrollx, 1485 + self.scrolly), 5)


        # SAC = Storage + Admin + Cafeteria
        def draw_sac_boundaries(self):
            # left vertical straight
            self.sac_ls = pygame.draw.line(self.game.display, self.border_color, (890 + self.scrollx, 1265 + self.scrolly), (890 + self.scrollx, 945 + self.scrolly), 5)

            # right top straight
            self.sac_rt = pygame.draw.line(self.game.display, self.border_color, (1020 + self.scrollx, 945 + self.scrolly), (1020 + self.scrollx, 1060 + self.scrolly), 5)

            # right bottom straight
            self.sac_rb = pygame.draw.line(self.game.display, self.border_color, (1020 + self.scrollx, 1265 + self.scrolly), (1020 + self.scrollx, 1215 + self.scrolly), 5)


        def draw_admin_boundaries(self):
            # Top straight
            self.admin_top = pygame.draw.line(self.game.display, self.border_color, (1020 + self.scrollx, 1060 + self.scrolly), (1595 + self.scrollx, 1060 + self.scrolly), 5)

            # right straight
            self.admin_rs = pygame.draw.line(self.game.display, self.border_color, (1595 + self.scrollx, 1060 + self.scrolly), (1595 + self.scrollx, 1360 + self.scrolly), 5)

            # right bottom angle
            self.admin_ra_coords = [(1595 + self.scrollx, 1360 + self.scrolly), (1520 + self.scrollx, 1435 + self.scrolly)]
            self.admin_ra = pygame.draw.line(self.game.display, self.border_color, self.admin_ra_coords[0], self.admin_ra_coords[1], 5)

            # bottom straight
            self.admin_bottom = pygame.draw.line(self.game.display, self.border_color, (1520 + self.scrollx, 1435 + self.scrolly), (1175 + self.scrollx, 1435 + self.scrolly), 5)

            # left straight
            self.admin_left = pygame.draw.line(self.game.display, self.border_color, (1175 + self.scrollx, 1435 + self.scrolly), (1175 + self.scrollx, 1215 + self.scrolly), 5)

            # admin bottom hallway
            self.admin_bh = pygame.draw.line(self.game.display, self.border_color, (1175 + self.scrollx, 1215 + self.scrolly), (1020 + self.scrollx, 1215 + self.scrolly), 5)

        # Storage electrical and engine hallway
        def draw_seeh_boundaries(self):
            # 0th top line
            self.seeh_t0 = pygame.draw.line(self.game.display, self.border_color, (582 + self.scrollx, 1675 + self.scrolly), (280 + self.scrollx, 1675 + self.scrolly), 5)

            # 1st top line
            self.seeh_t1 = pygame.draw.line(self.game.display, self.border_color, (153 + self.scrollx, 1675 + self.scrolly), (67 + self.scrollx, 1675 + self.scrolly), 5)

            # 2nd top line
            self.seeh_t2 = pygame.draw.line(self.game.display, self.border_color, (67 + self.scrollx, 1675 + self.scrolly), (67 + self.scrollx, 1440 + self.scrolly), 5)

            # 3rd top line
            self.seeh_t3 = pygame.draw.line(self.game.display, self.border_color, (67 + self.scrollx, 1440 + self.scrolly), (-225 + self.scrollx, 1440 + self.scrolly), 5)

            # 0th bottom line
            self.seeh_b0 = pygame.draw.line(self.game.display, self.border_color, (582 + self.scrollx, 1843 + self.scrolly), (-70 + self.scrollx, 1843 + self.scrolly), 5)

            # 1st bottom line
            self.seeh_b1 = pygame.draw.line(self.game.display, self.border_color, (-70 + self.scrollx, 1843 + self.scrolly), (-70 + self.scrollx, 1605 + self.scrolly), 5)

            # 2nd bottom line
            self.seeh_b2 = pygame.draw.line(self.game.display, self.border_color, (-70 + self.scrollx, 1605 + self.scrolly), (-225 + self.scrollx, 1605 + self.scrolly), 5)

        def draw_electrical_boundaries(self):
            # left straight line
            self.electrical_l = pygame.draw.line(self.game.display, self.border_color, (153 + self.scrollx, 1675 + self.scrolly), (153 + self.scrollx, 1145 + self.scrolly), 5)

            # top straight
            self.electrical_t = pygame.draw.line(self.game.display, self.border_color, (153 + self.scrollx, 1145 + self.scrolly), (580 + self.scrollx, 1145 + self.scrolly), 5)

            # 0th right (top down)
            self.electrical_r0 = pygame.draw.line(self.game.display, self.border_color, (580 + self.scrollx, 1145 + self.scrolly), (580 + self.scrollx, 1255 + self.scrolly), 5)

            # 1st right
            self.electrical_r1_coords = [(580 + self.scrollx, 1255 + self.scrolly), (480 + self.scrollx, 1360 + self.scrolly)]
            self.electrical_r1 = pygame.draw.line(self.game.display, self.border_color, self.electrical_r1_coords[0], self.electrical_r1_coords[1], 5)

            # 2nd Right
            self.electrical_r2 = pygame.draw.line(self.game.display, self.border_color, (480 + self.scrollx, 1360 + self.scrolly), (480 + self.scrollx, 1525 + self.scrolly), 5)

            # 3rd right
            self.electrical_r3_coords = [(480 + self.scrollx, 1525 + self.scrolly), (390 + self.scrollx, 1610 + self.scrolly)]
            self.electrical_r3 = pygame.draw.line(self.game.display, self.border_color, self.electrical_r3_coords[0], self.electrical_r3_coords[1], 5)

            # 4th right
            self.electrical_r4 = pygame.draw.line(self.game.display, self.border_color, (390 + self.scrollx, 1610 + self.scrolly), (280 + self.scrollx, 1610 + self.scrolly), 5)

            # 5th right
            self.electrical_r5 = pygame.draw.line(self.game.display, self.border_color, (280 + self.scrollx, 1610 + self.scrolly), (280 + self.scrollx, 1675 + self.scrolly), 5)

        def draw_lower_engine_boundaries(self):
            # Right bottom
            self.l_engine_rb = pygame.draw.line(self.game.display, self.border_color, (-225 + self.scrollx, 1605 + self.scrolly), (-225 + self.scrollx, 1745 + self.scrolly), 5)

            # bottom
            self.l_engine_b = pygame.draw.line(self.game.display, self.border_color, (-225 + self.scrollx, 1745 + self.scrolly), (-520 + self.scrollx, 1745 + self.scrolly), 5)

            # bottom angle
            self.l_engine_ba_coords = [(-520 + self.scrollx, 1745 + self.scrolly), (-620 + self.scrollx, 1660 + self.scrolly)]
            self.l_engine_ba = pygame.draw.line(self.game.display, self.border_color, self.l_engine_ba_coords[0], self.l_engine_ba_coords[1], 5)
            
            # left bottom
            self.l_engine_lb = pygame.draw.line(self.game.display, self.border_color, (-620 + self.scrollx, 1660 + self.scrolly), (-620 + self.scrollx, 1560 + self.scrolly), 5)

            # engine bottom
            self.l_engine_eb = pygame.draw.line(self.game.display, self.border_color, (-620 + self.scrollx, 1560 + self.scrolly), (-310 + self.scrollx, 1560 + self.scrolly), 5)

            # engine verticle
            self.l_engine_v = pygame.draw.line(self.game.display, self.border_color, (-310 + self.scrollx, 1560 + self.scrolly), (-310 + self.scrollx, 1425 + self.scrolly), 5)

            # engine top
            self.l_engine_et = pygame.draw.line(self.game.display, self.border_color, (-310 + self.scrollx, 1425 + self.scrolly), (-620 + self.scrollx, 1425 + self.scrolly), 5)

            # left top
            self.l_engine_lt = pygame.draw.line(self.game.display, self.border_color, (-620 + self.scrollx, 1425 + self.scrolly), (-620 + self.scrollx, 1305 + self.scrolly), 5)

            # top left
            self.l_engine_tl = pygame.draw.line(self.game.display, self.border_color, (-620 + self.scrollx, 1305 + self.scrolly), (-467 + self.scrollx, 1305 + self.scrolly), 5)

            # top right
            self.l_engine_tr = pygame.draw.line(self.game.display, self.border_color, (-335 + self.scrollx, 1305 + self.scrolly), (-225 + self.scrollx, 1305 + self.scrolly), 5)

            # right top
            self.l_engine_rt = pygame.draw.line(self.game.display, self.border_color, (-225 + self.scrollx, 1305 + self.scrolly), (-225 + self.scrollx, 1440 + self.scrolly), 5)

        def draw_ers_boundaries(self):
            # left bottom vert
            self.ers_lbv = pygame.draw.line(self.game.display, self.border_color, (-467 + self.scrollx, 1305 + self.scrolly), (-467 + self.scrollx, 1080 + self.scrolly), 5)

            # left bottom horizontal
            self.ers_lbh = pygame.draw.line(self.game.display, self.border_color, (-467 + self.scrollx, 1080 + self.scrolly), (-590 + self.scrollx, 1080 + self.scrolly), 5)

            # left top horizontal
            self.ers_lth = pygame.draw.line(self.game.display, self.border_color, (-467 + self.scrollx, 915 + self.scrolly), (-590 + self.scrollx, 915 + self.scrolly), 5)

            # left top verticle
            self.ers_ltv = pygame.draw.line(self.game.display, self.border_color, (-467 + self.scrollx, 915 + self.scrolly), (-467 + self.scrollx, 705 + self.scrolly), 5)

            # right top verticle
            self.ers_rtv = pygame.draw.line(self.game.display, self.border_color, (-335 + self.scrollx, 915 + self.scrolly), (-335 + self.scrollx, 705 + self.scrolly), 5)

            # right top horizontal
            self.ers_rth = pygame.draw.line(self.game.display, self.border_color, (-335 + self.scrollx, 915 + self.scrolly), (-203 + self.scrollx, 915 + self.scrolly), 5)

            # right bottom horizontal
            self.ers_rbh = pygame.draw.line(self.game.display, self.border_color, (-335 + self.scrollx, 1080 + self.scrolly), (-203 + self.scrollx, 1080 + self.scrolly), 5)

            # right bottom verticle
            self.ers_rbv = pygame.draw.line(self.game.display, self.border_color, (-335 + self.scrollx, 1080 + self.scrolly), (-335 + self.scrollx, 1305 + self.scrolly), 5)

        def draw_reactor_boundaries(self):
            # 0th right bottom
            self.reactor_0rb = pygame.draw.line(self.game.display, self.border_color, (-590 + self.scrollx, 1080 + self.scrolly), (-590 + self.scrollx, 1190 + self.scrolly), 5)

            # 1st right bottom
            self.reactor_1rb = pygame.draw.line(self.game.display, self.border_color, (-590 + self.scrollx, 1190 + self.scrolly), (-720 + self.scrollx, 1190 + self.scrolly), 5)

            # 2nd right bottom
            self.reactor_2rb = pygame.draw.line(self.game.display, self.border_color, (-720 + self.scrollx, 1190 + self.scrolly), (-720 + self.scrollx, 1330 + self.scrolly), 5)

            # bottom straight
            self.reactor_bs = pygame.draw.line(self.game.display, self.border_color, (-720 + self.scrollx, 1330 + self.scrolly), (-805 + self.scrollx, 1330 + self.scrolly), 5)

            # bottom angle
            self.reactor_ba_coords = [(-805 + self.scrollx, 1330 + self.scrolly), (-955 + self.scrollx, 1230 + self.scrolly)]
            self.reactor_ba = pygame.draw.line(self.game.display, self.border_color, self.reactor_ba_coords[0], self.reactor_ba_coords[1], 5)

            # left straight
            self.reactor_ls = pygame.draw.line(self.game.display, self.border_color, (-955 + self.scrollx, 1230 + self.scrolly), (-955 + self.scrollx, 750 + self.scrolly), 5)

            # 0th right top
            self.reactor_0rt = pygame.draw.line(self.game.display, self.border_color, (-590 + self.scrollx, 915 + self.scrolly), (-590 + self.scrollx, 795 + self.scrolly), 5)

            # 1st right top
            self.reactor_1rt = pygame.draw.line(self.game.display, self.border_color, (-590 + self.scrollx, 795 + self.scrolly), (-720 + self.scrollx, 795 + self.scrolly), 5)

            # 2nd right top
            self.reactor_2rt = pygame.draw.line(self.game.display, self.border_color, (-720 + self.scrollx, 795 + self.scrolly), (-720 + self.scrollx, 650 + self.scrolly), 5)

            # top straight
            self.reactor_ts = pygame.draw.line(self.game.display, self.border_color, (-720 + self.scrollx, 650 + self.scrolly), (-805 + self.scrollx, 650 + self.scrolly), 5)

            # top angle
            self.reactor_ta_coords = [(-805 + self.scrollx, 650 + self.scrolly), (-955 + self.scrollx, 750 + self.scrolly)]
            self.reactor_ta = pygame.draw.line(self.game.display, self.border_color, self.reactor_ta_coords[0], self.reactor_ta_coords[1], 5)


        def draw_security_boundaries(self):
            # left top
            self.security_lt = pygame.draw.line(self.game.display, self.border_color, (-203 + self.scrollx, 915 + self.scrolly), (-203 + self.scrollx, 815 + self.scrolly), 5)

            # top straight
            self.security_t = pygame.draw.line(self.game.display, self.border_color, (-203 + self.scrollx, 815 + self.scrolly), (20 + self.scrollx, 815 + self.scrolly), 5)

            # right straight
            self.security_r = pygame.draw.line(self.game.display, self.border_color, (20 + self.scrollx, 815 + self.scrolly), (20 + self.scrollx, 1185 + self.scrolly), 5)

            # bottom straight
            self.security_b = pygame.draw.line(self.game.display, self.border_color, (20 + self.scrollx, 1185 + self.scrolly), (-203 + self.scrollx, 1185 + self.scrolly), 5)

            # left bottom
            self.security_lb = pygame.draw.line(self.game.display, self.border_color, (-203 + self.scrollx, 1185 + self.scrolly), (-203 + self.scrollx, 1080 + self.scrolly), 5)

        def draw_upper_engine_boundaries(self):
            # bottom left straight
            self.u_engine_bl = pygame.draw.line(self.game.display, self.border_color, (-620 + self.scrollx, 705 + self.scrolly), (-467 + self.scrollx, 705 + self.scrolly), 5)

            # left bottom straight
            self.u_engine_lb = pygame.draw.line(self.game.display, self.border_color, (-620 + self.scrollx, 705 + self.scrolly), (-620 + self.scrollx, 540 + self.scrolly), 5)

            # engine bottom
            self.u_engine_eb = pygame.draw.line(self.game.display, self.border_color, (-620 + self.scrollx, 540 + self.scrolly), (-310 + self.scrollx, 540 + self.scrolly), 5)

            # engine right
            self.u_engine_er = pygame.draw.line(self.game.display, self.border_color, (-310 + self.scrollx, 540 + self.scrolly), (-310 + self.scrollx, 405 + self.scrolly), 5)

            # engine top
            self.u_engine_et = pygame.draw.line(self.game.display, self.border_color, (-310 + self.scrollx, 405 + self.scrolly), (-620 + self.scrollx, 405 + self.scrolly), 5)

            # left top straight
            self.u_engine_lt = pygame.draw.line(self.game.display, self.border_color, (-620 + self.scrollx, 405 + self.scrolly), (-620 + self.scrollx, 350 + self.scrolly), 5)

            # left top angle
            self.u_engine_lta_coords = [(-620 + self.scrollx, 350 + self.scrolly), (-520 + self.scrollx, 275 + self.scrolly)]
            self.u_engine_lta = pygame.draw.line(self.game.display, self.border_color, self.u_engine_lta_coords[0], self.u_engine_lta_coords[1], 5)

            # top straight
            self.u_engine_t = pygame.draw.line(self.game.display, self.border_color, (-520 + self.scrollx, 275 + self.scrolly), (-225 + self.scrollx, 275 + self.scrolly), 5)

            # right top
            self.u_engine_rt = pygame.draw.line(self.game.display, self.border_color, (-225 + self.scrollx, 275 + self.scrolly), (-225 + self.scrollx, 372 + self.scrolly), 5)

            # right bottom
            self.u_engine_rb = pygame.draw.line(self.game.display, self.border_color, (-225 + self.scrollx, 540 + self.scrolly), (-225 + self.scrollx, 705 + self.scrolly), 5)

            # bottom right
            self.u_engine_br = pygame.draw.line(self.game.display, self.border_color, (-225 + self.scrollx, 705 + self.scrolly), (-335 + self.scrollx, 705 + self.scrolly), 5)

        def draw_medbay_boundaries(self):
            # 0th left side
            self.medbay_0l = pygame.draw.line(self.game.display, self.border_color, (180 + self.scrollx, 540 + self.scrolly), (180 + self.scrollx, 595 + self.scrolly), 5)

            # 1st left side
            self.medbay_1l = pygame.draw.line(self.game.display, self.border_color, (180 + self.scrollx, 595 + self.scrolly), (80 + self.scrollx, 595 + self.scrolly), 5)

            # 2nd left side
            self.medbay_2l = pygame.draw.line(self.game.display, self.border_color, (80 + self.scrollx, 595 + self.scrolly), (80 + self.scrollx, 970 + self.scrolly), 5)

            # 3rd left side angle
            self.medbay_3l_coords = [(80 + self.scrollx, 970 + self.scrolly), (150 + self.scrollx, 1060 + self.scrolly)]
            self.medbay_3l = pygame.draw.line(self.game.display, self.border_color, self.medbay_3l_coords[0], self.medbay_3l_coords[1], 5)

            # bottom straight
            self.medbay_bottom = pygame.draw.line(self.game.display, self.border_color, (150 + self.scrollx, 1060 + self.scrolly), (575 + self.scrollx, 1060 + self.scrolly), 5)

            # 0th right
            self.medbay_0r = pygame.draw.line(self.game.display, self.border_color, (312 + self.scrollx, 540 + self.scrolly), (312 + self.scrollx, 595 + self.scrolly), 5) 

            # 1st right
            self.medbay_1r = pygame.draw.line(self.game.display, self.border_color, (312 + self.scrollx, 595 + self.scrolly), (430 + self.scrollx, 595 + self.scrolly), 5) 

            # 2nd right
            self.medbay_2r = pygame.draw.line(self.game.display, self.border_color, (430 + self.scrollx, 595 + self.scrolly), (430 + self.scrollx, 810 + self.scrolly), 5) 

            # 3rd right
            self.medbay_3r_coords = [(430 + self.scrollx, 810 + self.scrolly), (575 + self.scrollx, 950 + self.scrolly)]
            self.medbay_3r = pygame.draw.line(self.game.display, self.border_color, self.medbay_3r_coords[0], self.medbay_3r_coords[1], 5)

            # 4th right
            self.medbay_4r = pygame.draw.line(self.game.display, self.border_color, (575 + self.scrollx, 950 + self.scrolly), (575 + self.scrollx, 1060 + self.scrolly), 5) 


        draw_cafeteria_boundaries(self)
        draw_weapons_boundaries(self)
        draw_Oxygen_nav_weap_hallway_boundaries(self)
        draw_oxygen_boundaries(self)
        draw_navigation_boundaries(self)
        draw_shield_boundaries(self)
        draw_scs_hallway_boundaries(self)
        draw_comms_boundaries(self)
        draw_storage_boundaries(self)
        draw_sac_boundaries(self)
        draw_admin_boundaries(self)
        draw_seeh_boundaries(self)
        draw_electrical_boundaries(self)
        draw_lower_engine_boundaries(self)
        draw_ers_boundaries(self)
        draw_reactor_boundaries(self)
        draw_security_boundaries(self)
        draw_upper_engine_boundaries(self)
        draw_medbay_boundaries(self)


    # blits cafeteria section
    def load_cafeteria(self):
        self.game.display.blit(self.cafeteria_hallway_left, (-248 + self.scrollx, 353 + self.scrolly))
        self.game.display.blit(self.cafeteria, (467 + self.scrollx, 0 + self.scrolly))


    # blits weapons section
    def load_weapons(self):
        self.game.display.blit(self.weapons_base[0], (1570 + self.scrollx, 257 + self.scrolly))
        self.game.display.blit(self.weapons_base[3], (1605 + self.scrollx, 205 + self.scrolly)) 
        self.game.display.blit(self.weapons_base[4], (1604 + self.scrollx, 290 + self.scrolly))
        self.game.display.blit(self.weapons_base[5], (1850 + self.scrollx, 465 + self.scrolly))
        self.game.display.blit(self.weapons_base[1], (1587 + self.scrollx, 264 + self.scrolly)) 
        self.game.display.blit(self.cafeteria_weapons_hallway, (1447 + self.scrollx, 362 + self.scrolly)) 
        self.game.display.blit(self.weapons_base[2], (1447 + self.scrollx, 193 + self.scrolly))
        self.game.display.blit(self.weapons_base[6], (1596 + self.scrollx, 250 + self.scrolly))
        self.game.display.blit(self.weapons_base[7], (1598 + self.scrollx, 516 + self.scrolly))
        self.game.display.blit(self.weapons_base[8], (1859 + self.scrollx, 419 + self.scrolly))
        self.game.display.blit(self.weapons_base[2], (1447 + self.scrollx, 193 + self.scrolly))
        self.game.display.blit(self.weapons_chair, (1725 + self.scrollx, 375 + self.scrolly))
        self.game.display.blit(self.weapons_screen[self.screen_index], (1775 + self.scrollx, 300 + self.scrolly))
        self.game.display.blit(self.weapons_box, (1958 + self.scrollx, 377 + self.scrolly))
        self.game.display.blit(self.weapons_task[0], (1725 + self.scrollx, 225 + self.scrolly))
    
    # blits oxygen section
    def load_oxygen(self):
        self.game.display.blit(self.oxygen, (1342 + self.scrollx, 717 + self.scrolly))
        self.game.display.blit(self.oxygen_fans[self.oxygen_index], (1358 + self.scrollx, 785 + self.scrolly))
        self.game.display.blit(self.oxygen_vent, (1475 + self.scrollx, 810 + self.scrolly))
        self.game.display.blit(self.oxygen_plant, (1535 + self.scrollx, 729 + self.scrolly))
        self.game.display.blit(self.oxygen_task2, (1410 + self.scrollx, 835 + self.scrolly))
        self.game.display.blit(self.oxygen_task1, (1558 + self.scrollx, 811 + self.scrolly))

    # blits navigation section
    def load_nav(self):
        self.game.display.blit(self.nav2, (2270 + self.scrollx, 801 + self.scrolly))
        self.game.display.blit(self.nav3, (2276 + self.scrollx, 755 + self.scrolly))
        self.game.display.blit(self.console1, (2531 + self.scrollx, 905 + self.scrolly))
        self.game.display.blit(self.console2, (2483 + self.scrollx, 815 + self.scrolly))
        self.game.display.blit(self.chair1, (2450 + self.scrollx, 840 + self.scrolly))
        self.game.display.blit(self.chair2, (2465 + self.scrollx, 1060 + self.scrolly))
        self.game.display.blit(self.chair3, (2479 + self.scrollx, 919 + self.scrolly))
        self.game.display.blit(self.nav_box, (2325 + self.scrollx, 770 + self.scrolly))
        self.game.display.blit(self.nav_task1, (2415 + self.scrollx, 770 + self.scrolly))
        self.game.display.blit(self.nav1, (2274 + self.scrollx, 751 + self.scrolly))

    # blits shield section
    def load_shield(self):
        self.game.display.blit(self.shield1, (1550 + self.scrollx, 1375 + self.scrolly))
        self.game.display.blit(self.shield2, (1550 + self.scrollx, 1375 + self.scrolly))
        self.game.display.blit(self.shield3, (1525 + self.scrollx, 1344 + self.scrolly))
        self.game.display.blit(self.shield_light, (1670 + self.scrollx, 1380 + self.scrolly))
        self.game.display.blit(self.shield_light, (1655 + self.scrollx, 1400 + self.scrolly))
        self.game.display.blit(self.shield_light, (1640 + self.scrollx, 1420 + self.scrolly))
        self.game.display.blit(self.shield_light, (1625 + self.scrollx, 1440 + self.scrolly))
        self.game.display.blit(self.shield_light, (1940 + self.scrollx, 1480 + self.scrolly))
        self.game.display.blit(self.shield_light, (1940 + self.scrollx, 1505 + self.scrolly))
        self.game.display.blit(self.shield_light, (1940 + self.scrollx, 1530 + self.scrolly))
        self.game.display.blit(self.shield_rail1, (1536 + self.scrollx, 1620 + self.scrolly))
        self.game.display.blit(self.shield_rail2, (1784 + self.scrollx, 1440 + self.scrolly))
        self.game.display.blit(self.shield_rail3, (1846 + self.scrollx, 1596 + self.scrolly))
        self.game.display.blit(self.shield_rail4, (1576 + self.scrollx, 1429 + self.scrolly))
        self.game.display.blit(self.shield_mic, (1600 + self.scrollx, 1700 + self.scrolly))
    
    # blits admin section
    def load_admin(self):
        self.game.display.blit(self.admin_base1, (1025 + self.scrollx, 1107 + self.scrolly))
        self.game.display.blit(self.admin_base3, (1039 + self.scrollx, 1057 + self.scrolly))
        self.game.display.blit(self.admin_hallway, (881 + self.scrollx, 952 + self.scrolly))
        self.game.display.blit(self.admin_base2, (1040 + self.scrollx, 1049 + self.scrolly))
        self.game.display.blit(self.admin_screen2, (1290 + self.scrollx, 1075 + self.scrolly))
        self.game.display.blit(self.admin_screen1, (1457 + self.scrollx, 1074 + self.scrolly))
        self.game.display.blit(self.admin_chairs, (1295 + self.scrollx, 1100 + self.scrolly))
        self.game.display.blit(self.admin_table1, (1290 + self.scrollx, 1244 + self.scrolly))
        self.game.display.blit(self.admin_table2, (1288 + self.scrollx, 1252 + self.scrolly))
        self.game.display.blit(self.admin_table3, (1462 + self.scrollx, 1252 + self.scrolly))
        self.game.display.blit(self.admin_table4, (1335 + self.scrollx, 1257 + self.scrolly))
        self.game.display.blit(self.admin_task1, (1203 + self.scrollx, 1080 + self.scrolly))
        self.game.display.blit(self.admin_task2, (1110 + self.scrollx, 1085 + self.scrolly))
        self.game.display.blit(self.admin_vent, (1535 + self.scrollx, 1091 + self.scrolly))

    # blits storage section
    def load_storage(self):
        self.game.display.blit(self.storage_base, (548 + self.scrollx, 1240 + self.scrolly))
        self.game.display.blit(self.storage_bins, (670 + self.scrollx, 1477 + self.scrolly))
        self.game.display.blit(self.storage_bin, (925 + self.scrollx, 1485 + self.scrolly))
        self.game.display.blit(self.storage_task1, (1069 + self.scrollx, 1925 + self.scrolly))
        self.game.display.blit(self.storage_task2, (835 + self.scrollx, 1285 + self.scrolly))

        if self.show_fuel == True:
            self.game.display.blit(self.storage_fuel, (750 + self.scrollx, 1700 + self.scrolly))

    # blits comms section
    def load_comms(self):
        self.game.display.blit(self.comms_base1, (1131 + self.scrollx, 1735 + self.scrolly))
        self.game.display.blit(self.comms_base3, (1143 + self.scrollx, 1722 + self.scrolly))
        self.game.display.blit(self.comms_base5, (1260 + self.scrollx, 1927 + self.scrolly))
        self.game.display.blit(self.comms_base4, (1277 + self.scrollx, 1962 + self.scrolly))
        self.game.display.blit(self.comms_base6, (1137 + self.scrollx, 1850 + self.scrolly))
        self.game.display.blit(self.comms_base7, (1510 + self.scrollx, 1845 + self.scrolly))
        self.game.display.blit(self.comms_task, (1515 + self.scrollx, 1740 + self.scrolly))
        self.game.display.blit(self.comms_tape[self.comms_index], (1163 + self.scrollx, 1748 + self.scrolly))
        self.game.display.blit(self.comms_base2, (1130 + self.scrollx, 1690 + self.scrolly))

    # blits electrical section
    def load_electrical(self):
        self.game.display.blit(self.elec_base1, (-222 + self.scrollx, 1138 + self.scrolly))
        self.game.display.blit(self.elec_base2, (154 + self.scrollx, 1275 + self.scrolly))
        self.game.display.blit(self.elec_task1, (348 + self.scrollx, 1202 + self.scrolly))
        self.game.display.blit(self.elec_task2, (248 + self.scrollx, 1173 + self.scrolly))
        self.game.display.blit(self.elec_door1, (160 + self.scrollx, 1368 + self.scrolly))
        self.game.display.blit(self.elec_door2, (502 + self.scrollx, 1173 + self.scrolly))
        self.game.display.blit(self.elec_wire1, (130 + self.scrollx, 1150 + self.scrolly))
        self.game.display.blit(self.elec_wire2, (151 + self.scrollx, 1324 + self.scrolly))
    
    # blits engines section
    def load_engines(self):
        self.game.display.blit(self.upper_engine_base, (-629 + self.scrollx, 261 + self.scrolly))
        self.game.display.blit(self.engine_task3, (-445 + self.scrollx, 295 + self.scrolly))
        self.game.display.blit(self.engines_reactor_security_hallway, (-585 + self.scrollx, 725 + self.scrolly))
        self.game.display.blit(self.lower_engine_base, (-629 + self.scrollx, 1261 + self.scrolly))
        self.game.display.blit(self.engine_task3, (-510 + self.scrollx, 1335 + self.scrolly))
        # upper
        self.create_engine(-620, 370)

        # lower
        self.create_engine(-618, 1392)

    # engine function so the engine can be duplicates for upper and lower
    def create_engine(self, x, y):
        self.game.display.blit(self.engine_rail2, (x + 252 + self.scrollx, y + 40 + self.scrolly))
        self.game.display.blit(self.engine_base[self.engine_index], (x + self.scrollx, y + self.scrolly))
        self.game.display.blit(self.engine_rail1, (x + 97 + self.scrollx, y + 188 + self.scrolly))

        bolt = random.randint(0, 10)
        if bolt and self.powered and self.fueled:
            self.game.display.blit(self.engine_bolt[self.engine_bolt_index], (x + 103 + self.scrollx, y + 49 + self.scrolly))
            self.game.display.blit(self.engine_bolt[self.engine_bolt_index], (x + 103 + self.scrollx, y + 85 + self.scrolly))
            self.game.display.blit(self.engine_puff[self.engine_puff_index], (x + 275 + self.scrollx, y + 35 + (self.engine_puff_index * -25) + self.scrolly))

        self.game.display.blit(self.engine_task1, (x + 10 + self.scrollx, y + 210 + self.scrolly))
        self.game.display.blit(self.engine_task2, (x + 77 + self.scrollx, y + 197 + self.scrolly))
    
    # blit medbay section
    def load_medbay(self): 
        self.game.display.blit(self.medbay_base1, (68 + self.scrollx, 550 + self.scrolly))
        self.game.display.blit(self.medbay_base2, (325 + self.scrollx, 960 + self.scrolly))
        self.game.display.blit(self.medbay_base3, (440 + self.scrollx, 875 + self.scrolly))

    # blit security section
    def load_security(self):
        self.game.display.blit(self.security_base1, (-235 + self.scrollx, 730 + self.scrolly))
        self.game.display.blit(self.security_wire, (0 + self.scrollx, 790 + self.scrolly))
        self.game.display.blit(self.security_task, (-10 + self.scrollx, 805 + self.scrolly))
        self.game.display.blit(self.security_screen[self.security_screen_index], (-155 + self.scrollx, 740 + self.scrolly))
        self.game.display.blit(self.security_server[self.security_server_index], (-200 + self.scrollx, 780 + self.scrolly))
        self.game.display.blit(self.security_chair, (-125 + self.scrollx, 802 + self.scrolly))

    # blit reactor section
    def load_reactor(self):
        self.game.display.blit(self.reactor_base1, (-967 + self.scrollx, 700 + self.scrolly))
        self.game.display.blit(self.reactor_part3, (-730 + self.scrollx, 950 + self.scrolly))
        self.game.display.blit(self.reactor_part3, (-730 + self.scrollx, 1083 + self.scrolly))
        self.game.display.blit(self.reactor_base5, (-592 + self.scrollx, 918 + self.scrolly))
        self.game.display.blit(self.reactor_base3, (-950 + self.scrollx, 650 + self.scrolly))
        self.game.display.blit(self.reactor_part11, (-810 + self.scrollx, 820 + self.scrolly))
        self.game.display.blit(self.reactor_base4, (-724 + self.scrollx, 795 + self.scrolly))
        self.game.display.blit(self.reactor_part13, (-870 + self.scrollx, 680 + self.scrolly))
        self.game.display.blit(self.reactor_part15, (-955 + self.scrollx, 670 + self.scrolly))
        self.game.display.blit(self.reactor_part8, (-939 + self.scrollx, 798 + self.scrolly))
        self.game.display.blit(self.reactor_part10, (-887 + self.scrollx, 690 + self.scrolly))
        self.game.display.blit(self.reactor_part2, (-890 + self.scrollx, 1082 + self.scrolly))
        self.game.display.blit(self.reactor_task2, (-785 + self.scrollx, 660 + self.scrolly))
        self.game.display.blit(self.reactor_part14, (-960 + self.scrollx, 965 + self.scrolly))
        self.game.display.blit(self.reactor_part1, (-967 + self.scrollx, 830 + self.scrolly))
        self.game.display.blit(self.reactor_task3, (-675 + self.scrollx, 815 + self.scrolly))
        self.game.display.blit(self.reactor_part9, (-815 + self.scrollx, 1190 + self.scrolly))
        self.game.display.blit(self.reactor_part7, (-939 + self.scrollx, 1150 + self.scrolly))
        self.game.display.blit(self.reactor_part12, (-939 + self.scrollx, 1075 + self.scrolly))
        self.game.display.blit(self.reactor_task1, (-835 + self.scrollx, 1000 + self.scrolly))
        self.game.display.blit(self.reactor_part4, (-875 + self.scrollx, 1035 + self.scrolly))
        self.game.display.blit(self.reactor_part5, (-900 + self.scrollx, 1000 + self.scrolly))
        self.game.display.blit(self.reactor_part6, (-860 + self.scrollx, 995 + self.scrolly))
        self.game.display.blit(self.reactor_base2, (-963 + self.scrollx, 644 + self.scrolly))
