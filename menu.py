import pygame
from spritesheet import *
import math
import random

# menu class that will be inherited to furture classes
class menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.display_W / 2, self.game.display_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -250
        self.menu_background = pygame.image.load("images/background/menu/MainMenu.png")

    # draw cursor function
    def draw_cursor(self):
        self.game.draw_text("*", 100, self.cursor_rect.x, self.cursor_rect.y)

    # update screen
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

# main menu class
class MainMenu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 75
        self.settingsx, self.settingsy = self.mid_w, self.mid_h + 200
        self.quitx, self.quity = self.mid_w, self.mid_h + 325
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    # check for input
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

    # display menu
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
            self.game.draw_text("Main Menu", 250, self.mid_w, self.mid_h - 75)
            self.game.draw_text("Play Game", 100, self.startx, self.starty)
            self.game.draw_text(
                "Settings", 100, self.settingsx, self.settingsy)
            self.game.draw_text("Quit Game", 100, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

    # move the cursor
    def move_cursor(self):
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

# settings menu
class settingsMenu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = 'Skin'
        self.skinx, self.skiny = self.mid_w, self.mid_h + 75
        self.graphicsx, self.graphicsy = self.mid_w, self.mid_h + 200
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 325
        self.cursor_rect.midtop = (self.skinx + self.offset, self.skiny)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
            self.game.draw_text(
                "Settings", 250, self.game.display_W / 2, self.game.display_H / 2 - 75)
            self.game.draw_text("Select Skin", 100, self.skinx, self.skiny)
            self.game.draw_text("Graphics/Audio", 100,
                                self.graphicsx, self.graphicsy)
            self.game.draw_text(
                "Controls", 100, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

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

# skin menu
class skinMenu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = "Black"
        self.img_scale = (200, 241)  # original Dimension: 440, 482
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
        self.vert_offset = 15
        self.hori_offset = 115
        self.cursor_vert_offset = 250
        self.cursor_rect.midtop = (self.blackx, self.blacky + self.cursor_vert_offset)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
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
            self.draw_cursor()
            self.blit_screen()

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

    def check_input(self):
        self.move_cursor()
        if self.game.back_key:
            self.game.curr_menu = self.game.settings
            self.run_display = False

        elif self.game.start_key:
            self.game.skin = self.state
            self.game.curr_menu = self.game.settings
            self.run_display = False

# host/join menu
class host_join_menu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = 'Host'
        self.hostx, self.hosty = self.mid_w - 500, self.mid_h + 200
        self.joinx, self.joiny = self.mid_w + 500, self.mid_h + 200
        self.offset = 100
        self.cursor_rect.midtop = (self.hostx, self.hosty + self.offset)

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


# controls menu
class controls_menu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.menu_navx, self.menu_navy = self.mid_w - 500, self.mid_h + 50
        self.player_controlsx, self.player_controlsy = self.mid_w + 500, self.mid_h + 50
        self.offset = 100

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

    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.settings
        self.run_display = False


# Graphics menu
class graphics_menu(menu):  # TODO
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

    def get_character(self):
        Spritesheet = spritesheet("images/characters/"+ self.game.skin + "/" + self.game.skin + "_character_spritesheet.png", "Character")
        self.idle = [Spritesheet.parse_sprite('idle1.png'), Spritesheet.parse_sprite('idle2.png')]
        self.walk = []
        for i in range(12): 
            self.walk.append(Spritesheet.parse_sprite('walk' + str(i + 1) + '.png'))
        
        self.spawn_in = []
        for i in range(14):
            self.spawn_in.append(Spritesheet.parse_sprite('spawn-in' + str(i + 1) + '.png'))
    
    def box_collision(self):
        xvalues = False
        yvalues = False
        if self.playerx > 682 and self.playerx < 820:
            xvalues = True
        
        if self.playery > 380 and self.playery < 532:
            yvalues = True
        
        if xvalues and yvalues:
            return True
        else:
            return False
    
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

    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        
        if self.game.start_key:
            self.game.curr_menu = self.game.game_screen
            self.run_display = False
        
        if self.game.move_f:
            if self.playery < 273:
                pass
            elif self.box_collision():
                pass
            else:
                self.playery -= 7
                self.status = "walking_r"
                self.input = True
            
            while self.box_collision():
                    self.playery += 1
        
        if self.game.move_b:
            if self.playery > 546:
                pass
            elif self.box_collision():
                pass
            else:
                self.input = True
                self.playery += 7
                self.status = "walking_r"
            
            while self.box_collision():
                    self.playery -= 1
        
        if self.game.move_r:
            if self.playerx > 1158:
                pass
            elif self.box_collision():
                pass
            else:   
                self.input = True
                self.playerx += 7
                self.status = "walking_r"
            
            while self.box_collision():
                    self.playerx -= 1
        
        if self.game.move_l:
            if self.playerx < 661:
                pass
            elif self.box_collision():
                pass
            else:
                self.input = True
                self.playerx -= 7
                self.status = "walking_l"
            
            while self.box_collision():
                    self.playerx += 1
        
        if not self.game.move_l and not self.game.move_r and not self.game.move_f and not self.game.move_b:
            self.input = False
        
        if not self.input:
            self.status = "idle_r"


# TODO
class game_lobby(pregame_lobby):
    def __init__(self, game):
        menu.__init__(self, game)
        self.stars = pygame.image.load("images/background/game/pregame/stars.png")
        self.cafeteria = pygame.image.load("images/background/game/game_map/cafeteria/Cafeteria.png")
        self.cafeteria_hallway_left = pygame.image.load("images/background/game/game_map/cafeteria/Cafeteria_Upper_Engine_Medbay_Hallway.png") 
        self.load_background()
        self.status = "idle_r"
        self.playerx = 0
        self.playery = 0
        self.scrollx = 0
        self.scrolly = 0
        self.walk_counter = 0
        self.spawn_coords = [(920, 330), (1070, 450), (920, 540), (770, 450)]
        self.spawned = False
        self.screen_index = 0
        self.oxygen_index = 0
        self.animation_index = 0
    
    def load_background(self):
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
            
            if self.animation_index == 0:
                self.oxygen_index = (self.oxygen_index + 1) % len(self.oxygen_fans)
            self.check_status()
            self.blit_screen()
    
    def background(self):
        self.game.display.blit(self.stars, (0, 0))
        self.game.display.blit(self.cafeteria, (467 + self.scrollx, 0 + self.scrolly))
        self.game.display.blit(self.cafeteria_hallway_left, (-253 + self.scrollx, 353 + self.scrolly))
        self.load_nav()
        self.game.display.blit(self.O2_nav_weap_hallway, (1675 + self.scrollx, 660 + self.scrolly))
        self.load_weapons()
        self.game.display.blit(self.O2_nav_weap_task, (2210 + self.scrollx, 890 + self.scrolly))
        self.load_oxygen()
        self.load_shield()

    def spawn(self):
        rand_coords = self.spawn_coords[random.randint(0,3)]
        self.playerx, self.playery = rand_coords
        self.game.display.blit(pygame.transform.scale(self.idle[0], (50, 77)), rand_coords)
        self.spawned = True

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
        
        # TODO
        # blit the blaster to the display "self.weapons_gun"
    
    def load_oxygen(self):
        self.game.display.blit(self.oxygen, (1342 + self.scrollx, 717 + self.scrolly))
        self.game.display.blit(self.oxygen_fans[self.oxygen_index], (1358 + self.scrollx, 785 + self.scrolly))
        self.game.display.blit(self.oxygen_vent, (1475 + self.scrollx, 810 + self.scrolly))
        self.game.display.blit(self.oxygen_plant, (1535 + self.scrollx, 729 + self.scrolly))
        self.game.display.blit(self.oxygen_task2, (1410 + self.scrollx, 835 + self.scrolly))
        self.game.display.blit(self.oxygen_task1, (1558 + self.scrollx, 811 + self.scrolly))

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


    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
        self.run_display = False

        if self.game.move_f:
            self.scrolly += 10
            self.status = "walking_r"
            self.input = True
            
        if self.game.move_b:
            self.input = True
            self.scrolly -= 10
            self.status = "walking_r"
            
        if self.game.move_r:
            self.input = True
            self.scrollx -= 10
            self.status = "walking_r"
        
        if self.game.move_l:
            self.input = True
            self.scrollx += 10
            self.status = "walking_l"
    
        if not self.game.move_l and not self.game.move_r and not self.game.move_f and not self.game.move_b:
            self.input = False
        
        if not self.input:
            self.status = "idle_r"
        
    def check_status(self):
        if self.status == "idle_r":
            self.game.display.blit(pygame.transform.scale(self.idle[0], (50, 77)), (self.playerx, self.playery))

        if self.status == "idle_l":
            self.game.display.blit(pygame.transform.scale(self.idle[1], (50, 77)), (self.playerx, self.playery))
        
        if self.status == "walking_r":
            self.game.display.blit(pygame.transform.scale(self.walk[self.walk_counter], (50, 77)), (self.playerx, self.playery))
            self.walk_counter = (self.walk_counter + 1) % len(self.walk)
        
        if self.status == "walking_l":
            self.game.display.blit(pygame.transform.flip(pygame.transform.scale(self.walk[self.walk_counter], (50, 77)), True, False), (self.playerx, self.playery))
            self.walk_counter = (self.walk_counter + 1) % len(self.walk)