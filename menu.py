# import statements
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



