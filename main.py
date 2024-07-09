# import required modules
import pygame
from pygame.locals import *
import os
import sys

# other file imports
import sudoku
import scrolling_text

# attempt at reworking to functioning pyinstaller exe situation
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# center the window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# display and font initialization
if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()

display_width = 1000
display_height = 700
# set game window size, special type of surface
game_display = pygame.display.set_mode((display_width,display_height))

# blue dragon icon to match azure dragon title
# load image using the path
icon_url =  resource_path('data/pixel_dragon.jpg')
icon = pygame.image.load(icon_url).convert_alpha()
# sets color white as completely transparent
icon.set_colorkey((255, 255, 255))
pygame.display.set_icon(icon)

# set window name
pygame.display.set_caption("青龍 (セイリュウ)")

clock = pygame.time.Clock()

background_clr = (51,51,51)
text_clr = (241, 236, 206)
selected_clr = (64, 121, 140)

# class creating selection menu
class Menu:
    lists = []
    fields = []

    font_size = 48
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font

    dest_surface = pygame.Surface
    ilosc_pol = 0

    background_color = background_clr
    text_color =  text_clr
    selected_color = selected_clr

    pos_selected = 0
    pos_change = (0,0)

    menu_width = 0
    menu_height = 0

    ch_font_path = 'data/noto/NotoSansJP-Regular.otf'

    ch_font_size = 64
    jp_font_size = 32

    ch_font = pygame.font.Font(ch_font_path, ch_font_size)
    jp_font = pygame.font.Font(ch_font_path, jp_font_size)

    # game name: 青龍 (セイリュウ)
    ch_title = "青龍"
    jp_title = "セイリュウ"

    class Field:
        text = ''
        field = pygame.Surface
        field_rect = pygame.Rect
        selected_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pos_change = (top,left)

    def set_colors(self, text, selection, background):
        self.background_color = background
        self.text_color =  text
        self.selected_color = selection

    def set_fontsize(self, font_size):
        self.font_size = font_size

    def set_font(self, path):
        self.font_path = path

    def get_position(self):
        return self.pos_selected

    def init(self, lists, dest_surface):
        self.lists = lists
        self.dest_surface = dest_surface
        self.ilosc_pol = len(self.lists)
        self.create_structure()

    def draw(self, displace = 0):
        ch_text = self.ch_font.render(self.ch_title, True, text_clr)
        ch_text_rect = ch_text.get_rect(center=(display_width/2, display_height/4))
        game_display.blit(ch_text, ch_text_rect)

        jp_text = self.jp_font.render(self.jp_title, True, text_clr)
        jp_text_rect = jp_text.get_rect(center=(display_width/2, display_height/4 + self.ch_font_size))
        game_display.blit(jp_text, jp_text_rect)

        if displace:
            self.pos_selected += displace
            if self.pos_selected == -1:
                self.pos_selected = self.ilosc_pol - 1
            self.pos_selected %= self.ilosc_pol

        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.background_color)
        selected_rect = self.fields[self.pos_selected].selected_rect
        pygame.draw.rect(menu, self.selected_color, selected_rect)

        for i in range(self.ilosc_pol):
            menu.blit(self.fields[i].field, self.fields[i].field_rect)

        self.dest_surface.blit(menu, self.pos_change)

        return self.pos_selected

    def create_structure(self):
        displacement = 0
        self.menu_height = 0

        self.font = pygame.font.Font(self.font_path, self.font_size)
        for i in range(self.ilosc_pol):
            self.fields.append(self.Field())
            self.fields[i].text = self.lists[i]
            self.fields[i].field = self.font.render(self.fields[i].text, True, self.text_color)

            self.fields[i].field_rect = self.fields[i].field.get_rect()

            displacement = int(self.font_size * 0.2)

            height = self.fields[i].field_rect.height

            self.fields[i].field_rect.top = displacement + (displacement * 2 + height) * i

            width = self.fields[i].field_rect.width + displacement * 2
            height = self.fields[i].field_rect.height + displacement * 2
            top = self.fields[i].field_rect.top - displacement

            # horizontally centers text and selection box of menu items
            # based on the widest menu item __before__ current item
            # BUG: (iterates, wider menus need to be above smaller ones for
            # code to work properly, FIX: separate loop to check find biggest one)
            if self.menu_width > width:
                add_displacement = (self.menu_width - width) / 2
                self.fields[i].field_rect.left = displacement + add_displacement
            else:
                self.fields[i].field_rect.left = displacement

            left = self.fields[i].field_rect.left - displacement

            self.fields[i].selected_rect = (left, top, width, height)

            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height

        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2

        mx, my = self.pos_change
        self.pos_change = (x + mx, y + my)

screen = 0

def menu_screen():
    global screen

    menu = True

    game_display.fill(background_clr)

    main_menu = Menu() # necessary
    #menu.set_colors((255,255,255), (0,0,255), (0,0,0)) # optional
    #menu.set_fontsize(64) # optional
    #menu.set_font('data/couree.fon') # optional
    #menu.move_menu(100, 99) # optional
    main_menu.init(['Start','Quit'], game_display) # necessary
    #menu.move_menu(0, 0) # optional
    main_menu.draw() # necessary

    pygame.key.set_repeat(199,69)#(delay,interval)

    while menu:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    main_menu.draw(-1) # here is the Menu class function

                if event.key == K_DOWN:
                    main_menu.draw(1) # here is the Menu class function

                if event.key == K_RETURN:
                    if main_menu.get_position() == 0:
                        # clears the display
                        game_display.fill(background_clr)


                        if screen == 0:
                            print("intro_loop running")
                            scrolling_text.text_loop(game_display, screen, 'raw_texts/intro.txt')
                            screen = scrolling_text.get_screen()

                            game_display.fill(background_clr)
                            # TO DO
                            # Show "decrypting..."
                            # then launch text
                            # intro.intro_loop(game_display, screen)
                            # screen = intro.get_screen()

                            print("running decryption key")
                            scrolling_text.text_loop(game_display, screen, 'raw_texts/decrypting.txt')
                            screen = scrolling_text.get_screen()

                            game_display.fill(background_clr)
                            print("running letter")
                            scrolling_text.text_loop(game_display, screen, 'raw_texts/first_message.txt')
                            screen = scrolling_text.get_screen()

                        # runs the sudoku_loop
                        elif screen == 1:
                            print("sudoku_loop running")
                            sudoku.sudoku_loop(game_display)

                        # after exiting, the menu is loaded again
                        game_display.fill(background_clr)
                        main_menu.draw()
                        pygame.display.update()
                        break

                    if main_menu.get_position() == 1: # here is the Menu class function
                        print("quiting")
                        pygame.quit()
                        quit()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
            elif event.type == QUIT:
                pygame.quit()
                quit()

        clock.tick(15)
        pygame.display.update()

menu_screen()
#sudoku.sudoku_loop()
pygame.quit()
quit()
