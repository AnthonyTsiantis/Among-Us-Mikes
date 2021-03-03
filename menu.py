import pygame

class menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.display_W / 2, self.game.display_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -250
        self.menu_background = pygame.image.load("images/background/menu/MainMenu.png")


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
                self.game.playing = True
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
            self.game.draw_text("Settings", 100, self.settingsx, self.settingsy)
            self.game.draw_text("Quit Game", 100, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()
    
    def move_cursor(self):
        if self.game.down_key:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.settingsx + self.offset, self.settingsy)
                self.state = "Settings"
            
            elif self.state == "Settings":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = "Quit Game"
            
            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        
        elif self.game.up_key:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = "Quit Game"
            
            elif self.state == "Settings":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            
            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (self.settingsx + self.offset, self.settingsy)
                self.state = "Settings"

class settingsMenu(menu):
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = 'Skin'
        self.skinx, self.skiny = self.mid_w, self.mid_h + 150
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 300
        self.cursor_rect.midtop = (self.skinx + self.offset, self.skiny)
    
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.menu_background, (0, 0))
            self.game.draw_text("Settings", 200, self.game.display_W / 2, self.game.display_H / 2)
            self.game.draw_text("Select Skin", 100, self.skinx, self.skiny)
            self.game.draw_text("Controls", 100, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        if self.game.back_key:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.up_key or self.game.down_key:
            if self.state == "Skin":
                self.state = "Controls"
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == "Controls":
                self.state = "Skin"
                self.cursor_rect.midtop = (self.skinx + self.offset, self.skiny)
        elif self.game.start_key:
            # TODO
            pass










