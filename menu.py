import pygame

class menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.display_W / 2, self.game.display_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -250


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
        self.startx, self.starty = self.mid_w, self.mid_h
        self.settingsx, self.settingsy = self.mid_w, self.mid_h + 150
        self.quitx, self.quity = self.mid_w, self.mid_h + 300
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
    
    def check_input(self):
        self.move_cursor()
        if self.game.start_key:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Settings":
                pass
            elif self.state == "Quit Game":
                self.game.running, self.game.playing = False, False
            self.run_display = False

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            menu_background = pygame.image.load("images/background/menu/MainMenu.png")
            self.game.display.blit(menu_background, (0, 0))
            self.game.draw_text("Play Game", 150, self.startx, self.starty)
            self.game.draw_text("Settings", 150, self.settingsx, self.settingsy)
            self.game.draw_text("Quit Game", 150, self.quitx, self.quity)
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








