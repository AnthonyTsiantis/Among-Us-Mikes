import pygame
from spritesheet import *
import math
import random

# menu class that will be inherited to furture classes
class menu():
    # initilize menu class
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.display_W / 2, self.game.display_H / 2 # middle of the display
        self.run_display = True     # run the display
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) # initilize the display
        self.offset = -250 # cursor offset
        self.menu_background = pygame.image.load("images/background/menu/MainMenu.png") # load the menu background into RAM

    # draw cursor function
    def draw_cursor(self):
        self.game.draw_text("*", 100, self.cursor_rect.x, self.cursor_rect.y)

    # update screen function
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()



# main menu class
class MainMenu(menu):
    def __init__(self, game):
        menu.__init__(self, game)   # inherit the menu class
        self.state = "Start"    # initilize the state to "Start"

        # initilize the cursor locations for the following options
        self.startx, self.starty = self.mid_w, self.mid_h + 75 
        self.settingsx, self.settingsy = self.mid_w, self.mid_h + 200
        self.quitx, self.quity = self.mid_w, self.mid_h + 325
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    # input checking function
    def check_input(self):
        self.move_cursor()
        if self.game.start_key:
            if self.state == "Start":
                self.game.curr_menu = self.game.host_join
                # self.game.playing = True
            elif self.state == "Settings":
                self.game.curr_menu = self.game.settings
            elif self.state == "Quit Game":
                self.game.running, self.game.playing = False, False
            self.run_display = False

    # display menu: updates display (game loop)
    def display_menu(self):
        self.run_display = True     # enables the loop
        while self.run_display:
            self.game.check_events()    # runs the check events function
            self.check_input()  # runs the check input function
            self.game.display.blit(self.menu_background, (0, 0))    # blits the menu background to the screen
            self.game.draw_text("Main Menu", 250, self.mid_w, self.mid_h - 75)  # draws the Main Menu button to the screen
            self.game.draw_text("Play Game", 100, self.startx, self.starty)     # draws the play game button to the screen
            self.game.draw_text("Settings", 100, self.settingsx, self.settingsy)    # draws the settings button to the screen
            self.game.draw_text("Quit Game", 100, self.quitx, self.quity)   # draws the quit game button to the screen
            self.draw_cursor()  # draws/updates cursor
            self.blit_screen()  # Updates everything to the screen

    # move the cursor if input is detected
    def move_cursor(self):
        # moves the cursor according to key input
        if self.game.down_key:
            if self.state == "Start":
                self.cursor_rect.midtop = (
                    self.settingsx + self.offset, self.settingsy)
                self.state = "Settings"

            elif self.state == "Settings":
                self.cursor_rect.midtop = (
                    self.quitx + self.offset, self.quity)
                self.state = "Quit Game"

            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = "Start"

        # moves the cursor according to key input
        elif self.game.up_key:
            if self.state == "Start":
                self.cursor_rect.midtop = (
                    self.quitx + self.offset, self.quity)
                self.state = "Quit Game"

            elif self.state == "Settings":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = "Start"

            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (
                    self.settingsx + self.offset, self.settingsy)
                self.state = "Settings"




# settings menu, allows the user to change skin, audio and graphics, and controls
class settingsMenu(menu):
    # initilize the settings menu
    def __init__(self, game):
        menu.__init__(self, game) # inherit menu class
        self.state = 'Skin' # initilize the cursor state

        # Initilize the location of the cursor for each option
        self.skinx, self.skiny = self.mid_w, self.mid_h + 75 
        self.graphicsx, self.graphicsy = self.mid_w, self.mid_h + 200
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 325
        self.cursor_rect.midtop = (self.skinx + self.offset, self.skiny)

    # Game loop
    def display_menu(self):
        self.run_display = True # enable game loop
        while self.run_display:
            self.game.check_events()    # check events (button clicks)
            self.check_input()  # if button inputs occur, update cursor
            self.game.display.blit(self.menu_background, (0, 0))    # blit the menu background
            self.game.draw_text("Settings", 250, self.game.display_W / 2, self.game.display_H / 2 - 75)     # draw the settings text to the screen
            self.game.draw_text("Select Skin", 100, self.skinx, self.skiny)     # draw the select skin text to the screen
            self.game.draw_text("Graphics/Audio", 100, self.graphicsx, self.graphicsy)  # draw the graphics/audio text to the screen
            self.game.draw_text("Controls", 100, self.controlsx, self.controlsy) # draw the controls text to the screen
            self.draw_cursor() # update the cursor
            self.blit_screen() # push everything onto the screen

    # check input function that updates the display and cursor
    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.up_key:
            if self.state == "Skin":
                self.state = "Controls"
                self.cursor_rect.midtop = (
                    self.controlsx + self.offset, self.controlsy)
            elif self.state == "Controls":
                self.state = "Graphics"
                self.cursor_rect.midtop = (
                    self.graphicsx + self.offset, self.graphicsy)
            elif self.state == "Graphics":
                self.state = "Skin"
                self.cursor_rect.midtop = (
                    self.skinx + self.offset, self.skiny)
        elif self.game.down_key:
            if self.state == "Skin":
                self.state = "Graphics"
                self.cursor_rect.midtop = (
                    self.graphicsx + self.offset, self.graphicsy)
            elif self.state == "Graphics":
                self.state = "Controls"
                self.cursor_rect.midtop = (
                    self.controlsx + self.offset, self.controlsy)
            elif self.state == "Controls":
                self.state = "Skin"
                self.cursor_rect.midtop = (
                    self.skinx + self.offset, self.skiny)

        elif self.game.start_key:
            if self.state == "Skin":
                self.game.curr_menu = self.game.skin_menu
            elif self.state == "Graphics":
                self.game.curr_menu = self.game.graphics_menu
            elif self.state == "Controls":
                self.game.curr_menu = self.game.controls_menu
        self.run_display = False




# skin menu allows the user to choose their skin
class skinMenu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = "Black"
        self.img_scale = (200, 241)  # original Dimension: 440, 482

        # inilize all the skins and their locations
        self.blackx, self.blacky = self.mid_w - 825, self.mid_h
        self.black_img = pygame.transform.scale(pygame.image.load("images/characters/Black/Black.png"), self.img_scale)
        self.whitex, self.whitey = self.mid_w - 675, self.mid_h
        self.white_img = pygame.transform.scale(pygame.image.load("images/characters/White/White.png"), self.img_scale)
        self.brownx, self.browny = self.mid_w - 525, self.mid_h
        self.brown_img = pygame.transform.scale(pygame.image.load("images/characters/Brown/Brown.png"), self.img_scale)
        self.redx, self.redy = self.mid_w - 375, self.mid_h
        self.red_img = pygame.transform.scale(pygame.image.load("images/characters/Red/Red.png"), self.img_scale)
        self.orangex, self.orangey = self.mid_w - 225, self.mid_h
        self.orange_img = pygame.transform.scale(pygame.image.load("images/characters/Orange/Orange.png"), self.img_scale)
        self.yellowx, self.yellowy = self.mid_w - 75, self.mid_h
        self.yellow_img = pygame.transform.scale(pygame.image.load("images/characters/Yellow/Yellow.png"), self.img_scale)
        self.limex, self.limey = self.mid_w + 75, self.mid_h
        self.lime_img = pygame.transform.scale(pygame.image.load("images/characters/Lime/Lime.png"), self.img_scale)
        self.greenx, self.greeny = self.mid_w + 225, self.mid_h
        self.green_img = pygame.transform.scale(pygame.image.load("images/characters/Green/Green.png"), self.img_scale)
        self.cyanx, self.cyany = self.mid_w + 375, self.mid_h
        self.cyan_img = pygame.transform.scale(pygame.image.load("images/characters/Cyan/Cyan.png"), self.img_scale)
        self.bluex, self.bluey = self.mid_w + 525, self.mid_h
        self.blue_img = pygame.transform.scale(pygame.image.load("images/characters/Blue/Blue.png"), self.img_scale)
        self.purplex, self.purpley = self.mid_w + 675, self.mid_h
        self.purple_img = pygame.transform.scale(pygame.image.load("images/characters/Purple/Purple.png"), self.img_scale)
        self.pinkx, self.pinky = self.mid_w + 825, self.mid_h
        self.pink_img = pygame.transform.scale(pygame.image.load("images/characters/Pink/Pink.png"), self.img_scale)
        
        # initilize skins
        self.vert_offset = 15
        self.hori_offset = 115
        self.cursor_vert_offset = 250
        self.cursor_rect.midtop = (self.blackx, self.blacky + self.cursor_vert_offset)

    # Game loop
    def display_menu(self):
        self.run_display = True # enable the game loop
        while self.run_display:
            self.game.check_events() # check events functions
            self.check_input() # Check input function
            self.game.display.blit(self.menu_background, (0, 0)) # blit background

            # draw skin titles
            self.game.draw_text("Skins", 150, self.game.display_W / 2, (self.game.display_H / 2) - 100)
            self.game.draw_text("Black", 50, self.blackx, self.blacky)
            self.game.display.blit(self.black_img, (self.blackx - self.hori_offset, self.blacky + self.vert_offset))
            self.game.draw_text("White", 50, self.whitex, self.whitey)
            self.game.display.blit(self.white_img, (self.whitex - self.hori_offset, self.whitey + self.vert_offset))
            self.game.draw_text("Brown", 50, self.brownx, self.browny)
            self.game.display.blit(self.brown_img, (self.brownx - self.hori_offset, self.browny + self.vert_offset))
            self.game.draw_text("Red", 50, self.redx, self.redy)
            self.game.display.blit(self.red_img, (self.redx - self.hori_offset, self.redy + self.vert_offset))
            self.game.draw_text("Orange", 50, self.orangex, self.orangey)
            self.game.display.blit(self.orange_img, (self.orangex - self.hori_offset, self.orangey + self.vert_offset))
            self.game.draw_text("Yellow", 50, self.yellowx, self.yellowy)
            self.game.display.blit(self.yellow_img, (self.yellowx - self.hori_offset, self.yellowy + self.vert_offset))
            self.game.draw_text("Lime", 50, self.limex, self.limey)
            self.game.display.blit(self.lime_img, (self.limex - self.hori_offset, self.limey + self.vert_offset))
            self.game.draw_text("Green", 50, self.greenx, self.greeny)
            self.game.display.blit(self.green_img, (self.greenx - self.hori_offset, self.greeny + self.vert_offset))
            self.game.draw_text("Cyan", 50, self.cyanx, self.cyany)
            self.game.display.blit(self.cyan_img, (self.cyanx - self.hori_offset, self.cyany + self.vert_offset))
            self.game.draw_text("Blue", 50, self.bluex, self.bluey)
            self.game.display.blit(self.blue_img, (self.bluex - self.hori_offset, self.bluey + self.vert_offset))
            self.game.draw_text("Purple", 50, self.purplex, self.purpley)
            self.game.display.blit(self.purple_img, (self.purplex - self.hori_offset, self.purpley + self.vert_offset))
            self.game.draw_text("Pink", 50, self.pinkx, self.pinky)
            self.game.display.blit(self.pink_img, (self.pinkx - self.hori_offset, self.pinky + self.vert_offset))
            self.draw_cursor() # update cursor
            self.blit_screen() # update screen
    
    # move cursor function
    def move_cursor(self):
        if self.game.right_key:
            if self.state == "Black":
                self.cursor_rect.midtop = (
                    self.whitex, self.whitey + self.cursor_vert_offset)
                self.state = "White"

            elif self.state == "White":
                self.cursor_rect.midtop = (
                    self.brownx, self.browny + self.cursor_vert_offset)
                self.state = "Brown"

            elif self.state == "Brown":
                self.cursor_rect.midtop = (
                    self.redx, self.redy + self.cursor_vert_offset)
                self.state = "Red"

            elif self.state == "Red":
                self.cursor_rect.midtop = (
                    self.orangex, self.orangey + self.cursor_vert_offset)
                self.state = "Orange"

            elif self.state == "Orange":
                self.cursor_rect.midtop = (
                    self.yellowx, self.yellowy + self.cursor_vert_offset)
                self.state = "Yellow"

            elif self.state == "Yellow":
                self.cursor_rect.midtop = (
                    self.limex, self.limey + self.cursor_vert_offset)
                self.state = "Lime"

            elif self.state == "Lime":
                self.cursor_rect.midtop = (
                    self.greenx, self.greeny + self.cursor_vert_offset)
                self.state = "Green"

            elif self.state == "Green":
                self.cursor_rect.midtop = (
                    self.cyanx, self.cyany + self.cursor_vert_offset)
                self.state = "Cyan"

            elif self.state == "Cyan":
                self.cursor_rect.midtop = (
                    self.bluex, self.bluey + self.cursor_vert_offset)
                self.state = "Blue"

            elif self.state == "Blue":
                self.cursor_rect.midtop = (
                    self.purplex, self.purpley + self.cursor_vert_offset)
                self.state = "Purple"

            elif self.state == "Purple":
                self.cursor_rect.midtop = (
                    self.pinkx, self.pinky + self.cursor_vert_offset)
                self.state = "Pink"

            elif self.state == "Pink":
                self.cursor_rect.midtop = (
                    self.blackx, self.blacky + self.cursor_vert_offset)
                self.state = "Black"

        elif self.game.left_key:
            if self.state == "Black":
                self.cursor_rect.midtop = (
                    self.pinkx, self.pinky + self.cursor_vert_offset)
                self.state = "Pink"

            elif self.state == "Pink":
                self.cursor_rect.midtop = (
                    self.purplex, self.purpley + self.cursor_vert_offset)
                self.state = "Purple"

            elif self.state == "Purple":
                self.cursor_rect.midtop = (
                    self.bluex, self.bluey + self.cursor_vert_offset)
                self.state = "Blue"

            elif self.state == "Blue":
                self.cursor_rect.midtop = (
                    self.cyanx, self.cyany + self.cursor_vert_offset)
                self.state = "Cyan"

            elif self.state == "Cyan":
                self.cursor_rect.midtop = (
                    self.greenx, self.greeny + self.cursor_vert_offset)
                self.state = "Green"

            elif self.state == "Green":
                self.cursor_rect.midtop = (
                    self.limex, self.limey + self.cursor_vert_offset)
                self.state = "Lime"

            elif self.state == "Lime":
                self.cursor_rect.midtop = (
                    self.yellowx, self.yellowy + self.cursor_vert_offset)
                self.state = "Yellow"

            elif self.state == "Yellow":
                self.cursor_rect.midtop = (
                    self.orangex, self.orangey + self.cursor_vert_offset)
                self.state = "Orange"

            elif self.state == "Orange":
                self.cursor_rect.midtop = (
                    self.redx, self.redy + self.cursor_vert_offset)
                self.state = "Red"

            elif self.state == "Red":
                self.cursor_rect.midtop = (
                    self.brownx, self.browny + self.cursor_vert_offset)
                self.state = "Brown"

            elif self.state == "Brown":
                self.cursor_rect.midtop = (
                    self.whitex, self.whitey + self.cursor_vert_offset)
                self.state = "White"

            elif self.state == "White":
                self.cursor_rect.midtop = (
                    self.blackx, self.blacky + self.cursor_vert_offset)
                self.state = "Black"

    # check game input function
    def check_input(self):
        self.move_cursor()
        if self.game.back_key:
            self.game.curr_menu = self.game.settings
            self.run_display = False

        elif self.game.start_key:
            self.game.skin = self.state
            self.game.curr_menu = self.game.settings
            self.run_display = False




# host/join menu #TODO
class host_join_menu(menu):
    # initilize text and cursor locations
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = 'Host'
        self.hostx, self.hosty = self.mid_w - 500, self.mid_h + 200
        self.joinx, self.joiny = self.mid_w + 500, self.mid_h + 200
        self.offset = 100
        self.cursor_rect.midtop = (self.hostx, self.hosty + self.offset)
    
    # Menu display loop
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
            self.game.draw_text("Host or Join Game", 150, self.game.display_W / 2, self.game.display_H / 2 - 50)
            self.game.draw_text("Host", 200, self.hostx, self.hosty)
            self.game.draw_text("Join", 200, self.joinx, self.joiny)
            self.draw_cursor()
            self.blit_screen()

    # update cursor and menu display
    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.right_key or self.game.left_key:
            if self.state == "Host":
                self.cursor_rect.midtop = (
                    self.joinx, self.joiny + self.offset)
                self.state = "Join"
            elif self.state == "Join":
                self.cursor_rect.midtop = (
                    self.hostx, self.hosty + self.offset)
                self.state = "Host"
        elif self.game.start_key:
            if self.state == "Host":
                self.game.curr_menu = self.game.pregame
            elif self.state == "Join":
                # TODO
                pass
            self.run_display = False




# controls menu, explains how to navigate menu and play the game
class controls_menu(menu):
    # initilize menu
    def __init__(self, game):
        menu.__init__(self, game)
        self.menu_navx, self.menu_navy = self.mid_w - 500, self.mid_h + 50
        self.player_controlsx, self.player_controlsy = self.mid_w + 500, self.mid_h + 50
        self.offset = 100

    # Menu loop
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
            self.game.draw_text("Controls", 200, self.game.display_W / 2, self.game.display_H / 2 - 100)
            self.game.draw_text("Menu Navigation", 100,self.menu_navx, self.menu_navy)
            self.game.draw_text("Navigate Menu's using the arrow keys, enter and backspace", 50, self.menu_navx, self.menu_navy + self.offset)
            self.game.draw_text("Player controls", 100, self.player_controlsx, self.player_controlsy)
            self.game.draw_text("Control the player using WASD and enter keys", 50, self.player_controlsx, self.player_controlsy + self.offset)
            self.draw_cursor()
            self.blit_screen()

    # update menu
    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.settings
        self.run_display = False


# Graphics and audio menu, allows the user to resize screen and control game volume # TODO
class graphics_menu(menu):  
    def __init__(self, game):
        menu.__init__(self, game)
        self.displayx, self.displayy = self.mid_w - 500, self.mid_h + 50
        self.audiox, self.audioy = self.mid_w + 500, self.mid_h + 50
        self.offset = 100

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
            self.game.draw_text("Graphics and Audio", 200, self.game.display_W / 2, self.game.display_H / 2 - 100)
            self.game.draw_text("Graphics", 100, self.displayx, self.displayy)
            self.game.draw_text("Audio", 100, self.audiox, self.audioy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.settings
        self.run_display = False



# Pregame lobby
class pregame_lobby(menu):
    # initilize lobby
    def __init__(self, game):
        menu.__init__(self, game)
        self.stars = pygame.image.load("images/background/game/pregame/stars.png")
        Spritesheet = spritesheet("images/background/game/pregame/spritesheet.png", "Character")
        self.box = Spritesheet.parse_sprite('box.png',)
        self.ship = Spritesheet.parse_sprite('ship.png')
        self.front = Spritesheet.parse_sprite('front.png')
        self.computers = [Spritesheet.parse_sprite('computer1.png'), Spritesheet.parse_sprite('computer2.png')]
        self.rocket = [Spritesheet.parse_sprite('rocket1.png'), Spritesheet.parse_sprite('rocket2.png'), Spritesheet.parse_sprite('rocket3.png'), Spritesheet.parse_sprite('rocket4.png'), Spritesheet.parse_sprite('rocket5.png'), Spritesheet.parse_sprite('rocket6.png')]
        self.left_rocket = []
        for rocket in self.rocket:
            self.left_rocket.append(pygame.transform.rotate(rocket, 23))
        
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
        self.num_usersx, self.num_usersy = 932, 900
        self.num_of_players = 1
        self.boxx, self.boxy = 725, 450
        self.moved_left = False

    # game loop
    def display_menu(self):
        self.run_display = True
        self.get_character()
        self.spawned = False
        while self.run_display:
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

            self.game.draw_text("Players: " + str(self.num_of_players) + "/30", 100, self.num_usersx, self.num_usersy)
            self.game.draw_text("Game Code: XYZ", 65, self.num_usersx, self.num_usersy - 75)
            self.game.draw_text("*Host must start game by hitting the enter key*", 30, self.num_usersx, self.num_usersy + 85)

            self.blit_screen()
        self.playerx = 800
        self.playery = 240
        
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
        
        if self.game.move_f:
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
        
        if self.game.move_b:
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
                           
        if self.game.move_r:
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
        
        if self.game.move_l:
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
        self.load_sprites()
        self.status = "idle_r"
        self.playerx, self.playery = (910, 463)
        self.scrollx, self.scrolly = (0, 0)
        self.walk_counter = 0
        """self.spawn_coords = [(145, 13), (-6, -75), (-158, 13), (-6, 133)]
        rand_coords = self.spawn_coords[random.randint(0,3)]
        self.scrollx, self.scrolly = rand_coords"""
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
        self.border_color = (255, 0, 0, 100) 
        self.player_hitbox = pygame.Rect(self.playerx, self.playery, 50, 77)
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
                self.screen_index = (self.screen_index + 1) % len(self.weapons_screen)
                self.oxygen_index = (self.oxygen_index + 1) % len(self.oxygen_fans)
                self.comms_index = (self.comms_index + 1) % len(self.comms_tape)
                self.engine_index = (self.engine_index + 1) % len(self.engine_base)
                self.engine_bolt_index = (self.engine_bolt_index + 1) % len(self.engine_bolt)
                self.engine_puff_index = (self.engine_puff_index + 1) % len(self.engine_puff)
                self.medbay_scan_index = (self.medbay_scan_index + 1) % len(self.medbay_scan)
                self.security_screen_index = (self.security_screen_index + 1) % len(self.security_screen)
                self.security_server_index = (self.security_server_index + 1) % len(self.security_server)
                
            # print(self.scrollx, self.scrolly)
            self.check_status()
            self.blit_screen()
    
    
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

    # check keyboard input # TODO
    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
        self.run_display = False

        boundary = self.boundaries()
        print(boundary)

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
                return True, 'f'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_hallway_br_s):
                return True, 'b'
            
            elif pygame.Rect.colliderect(self.player_hitbox, self.caf_hallway_bl_s):
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
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_tr):
                if pygame.Rect.colliderect(self.player_hitbox,self.l_engine_rt):
                    return True, 'rfc'
                return True, 'f'

            elif pygame.Rect.colliderect(self.player_hitbox,self.l_engine_rt):
                return True, 'r'



            return False, 'N/A'
        
        result = lower_engine_boundaries(self)
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
        self.game.display.blit(self.storage_fuel, (750 + self.scrollx, 1700 + self.scrolly))
        self.game.display.blit(self.storage_task1, (1069 + self.scrollx, 1925 + self.scrolly))
        self.game.display.blit(self.storage_task2, (835 + self.scrollx, 1285 + self.scrolly))

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
        if bolt:
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
        self.game.display.blit(self.medbay_scan[self.medbay_scan_index], (350 + (self.medbay_scan_index * 7) + self.scrollx, 980 + -(self.medbay_scan_index * 20) + self.scrolly))

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
