import pygame
from spritesheet import *
from character import *


class menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.display_W / 2, self.game.display_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -250
        self.menu_background = pygame.image.load(
            "images/background/menu/MainMenu.png")

    def draw_cursor(self):
        self.game.draw_text("*", 100, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 75
        self.settingsx, self.settingsy = self.mid_w, self.mid_h + 200
        self.quitx, self.quity = self.mid_w, self.mid_h + 325
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

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


class skinMenu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = "Black"
        self.img_scale = (200, 241)  # original Dimension: 440, 482
        self.blackx, self.blacky = self.mid_w - 825, self.mid_h
        self.black_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Black.png"), self.img_scale)
        self.whitex, self.whitey = self.mid_w - 675, self.mid_h
        self.white_img = pygame.transform.scale(pygame.image.load(
            "images/characters/White.png"), self.img_scale)
        self.brownx, self.browny = self.mid_w - 525, self.mid_h
        self.brown_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Brown.png"), self.img_scale)
        self.redx, self.redy = self.mid_w - 375, self.mid_h
        self.red_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Red.png"), self.img_scale)
        self.orangex, self.orangey = self.mid_w - 225, self.mid_h
        self.orange_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Orange.png"), self.img_scale)
        self.yellowx, self.yellowy = self.mid_w - 75, self.mid_h
        self.yellow_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Yellow.png"), self.img_scale)
        self.limex, self.limey = self.mid_w + 75, self.mid_h
        self.lime_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Lime.png"), self.img_scale)
        self.greenx, self.greeny = self.mid_w + 225, self.mid_h
        self.green_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Green.png"), self.img_scale)
        self.cyanx, self.cyany = self.mid_w + 375, self.mid_h
        self.cyan_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Cyan.png"), self.img_scale)
        self.bluex, self.bluey = self.mid_w + 525, self.mid_h
        self.blue_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Blue.png"), self.img_scale)
        self.purplex, self.purpley = self.mid_w + 675, self.mid_h
        self.purple_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Purple.png"), self.img_scale)
        self.pinkx, self.pinky = self.mid_w + 825, self.mid_h
        self.pink_img = pygame.transform.scale(pygame.image.load(
            "images/characters/Pink.png"), self.img_scale)
        self.vert_offset = 15
        self.hori_offset = 115
        self.cursor_vert_offset = 250
        self.cursor_rect.midtop = (
            self.blackx, self.blacky + self.cursor_vert_offset)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
            self.game.draw_text(
                "Skins", 150, self.game.display_W / 2, (self.game.display_H / 2) - 100)
            self.game.draw_text("Black", 50, self.blackx, self.blacky)
            self.game.display.blit(
                self.black_img, (self.blackx - self.hori_offset, self.blacky + self.vert_offset))
            self.game.draw_text("White", 50, self.whitex, self.whitey)
            self.game.display.blit(
                self.white_img, (self.whitex - self.hori_offset, self.whitey + self.vert_offset))
            self.game.draw_text("Brown", 50, self.brownx, self.browny)
            self.game.display.blit(
                self.brown_img, (self.brownx - self.hori_offset, self.browny + self.vert_offset))
            self.game.draw_text("Red", 50, self.redx, self.redy)
            self.game.display.blit(
                self.red_img, (self.redx - self.hori_offset, self.redy + self.vert_offset))
            self.game.draw_text("Orange", 50, self.orangex, self.orangey)
            self.game.display.blit(
                self.orange_img, (self.orangex - self.hori_offset, self.orangey + self.vert_offset))
            self.game.draw_text("Yellow", 50, self.yellowx, self.yellowy)
            self.game.display.blit(
                self.yellow_img, (self.yellowx - self.hori_offset, self.yellowy + self.vert_offset))
            self.game.draw_text("Lime", 50, self.limex, self.limey)
            self.game.display.blit(
                self.lime_img, (self.limex - self.hori_offset, self.limey + self.vert_offset))
            self.game.draw_text("Green", 50, self.greenx, self.greeny)
            self.game.display.blit(
                self.green_img, (self.greenx - self.hori_offset, self.greeny + self.vert_offset))
            self.game.draw_text("Cyan", 50, self.cyanx, self.cyany)
            self.game.display.blit(
                self.cyan_img, (self.cyanx - self.hori_offset, self.cyany + self.vert_offset))
            self.game.draw_text("Blue", 50, self.bluex, self.bluey)
            self.game.display.blit(
                self.blue_img, (self.bluex - self.hori_offset, self.bluey + self.vert_offset))
            self.game.draw_text("Purple", 50, self.purplex, self.purpley)
            self.game.display.blit(
                self.purple_img, (self.purplex - self.hori_offset, self.purpley + self.vert_offset))
            self.game.draw_text("Pink", 50, self.pinkx, self.pinky)
            self.game.display.blit(
                self.pink_img, (self.pinkx - self.hori_offset, self.pinky + self.vert_offset))
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
            self.game.draw_text(
                "Host or Join Game", 150, self.game.display_W / 2, self.game.display_H / 2 - 50)
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
            self.game.draw_text(
                "Controls", 200, self.game.display_W / 2, self.game.display_H / 2 - 100)
            self.game.draw_text("Menu Navigation", 100,
                                self.menu_navx, self.menu_navy)
            self.game.draw_text("Navigate Menu's using the arrow keys, enter and backspace",
                                50, self.menu_navx, self.menu_navy + self.offset)
            self.game.draw_text("Player controls", 100,
                                self.player_controlsx, self.player_controlsy)
            self.game.draw_text("Control the player using WASD and enter keys",
                                50, self.player_controlsx, self.player_controlsy + self.offset)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.settings
        self.run_display = False


class graphics_menu(menu):  # TODO
    def __init__(self, game):
        menu.__init__(self, game)
        self.displayx, self.displayy = self.mid_w - 500, self.mid_h + 50
        self.audiox, self.audioy = self.mid_w + 500, self.mid_h + 50
        self.offset = 100
        # self.cursor_rect.midtop = (self.hostx, self.hosty + self.offset)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
            self.game.draw_text(
                "Graphics and Audio", 200, self.game.display_W / 2, self.game.display_H / 2 - 100)
            self.game.draw_text("Graphics", 100, self.displayx, self.displayy)
            self.game.draw_text("Audio", 100, self.audiox, self.audioy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.settings
        self.run_display = False


class pregame_lobby(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.black = (0, 0, 0)
        self.stars = pygame.image.load(
            "images/background/game/pregame/stars.png")
        Spritesheet = spritesheet(
            "images/background/game/pregame/spritesheet.png")
        self.box = Spritesheet.parse_sprite('box.png', self.black)
        self.ship = Spritesheet.parse_sprite('ship.png', self.black)
        self.front = Spritesheet.parse_sprite('front.png', self.black)
        self.computers = [Spritesheet.parse_sprite(
            'computer1.png', self.black), Spritesheet.parse_sprite('computer2.png', self.black)]
        self.rocket = [Spritesheet.parse_sprite('rocket1.png', self.black), Spritesheet.parse_sprite('rocket3.png', self.black), Spritesheet.parse_sprite(
            'rocket3.png', self.black), Spritesheet.parse_sprite('rocket4.png', self.black), Spritesheet.parse_sprite('rocket5.png', self.black), Spritesheet.parse_sprite('rocket6.png', self.black)]
        self.left_rocket = []
        for rocket in self.rocket:
            self.left_rocket.append(pygame.transform.rotate(rocket, 23))
        self.index = 0
        self.counter = 0
        Spritesheet = spritesheet(
            "images/characters/character_spritesheet.png")
        self.idle1 = Spritesheet.parse_sprite('idle1.png', self.black)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            if self.counter == 3:
                self.counter = 0
                self.index = (self.index + 1) % len(self.rocket)

            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.stars, (0, 0))
            self.game.display.blit(self.ship, (320, 10))
            self.game.display.blit(pygame.transform.scale(
                self.front, (640, 361)), (612, 646))
            self.game.display.blit(self.box, (725, 450))
            self.game.display.blit(self.computers[0], (730, 430))
            self.game.display.blit(self.left_rocket[self.index], (340, 707))
            self.game.display.blit(self.rocket[self.index], (1326, 736))
            self.game.display.blit(self.idle1, (800, 500))

            self.blit_screen()
            self.counter += 1

    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu

        self.run_display = False
