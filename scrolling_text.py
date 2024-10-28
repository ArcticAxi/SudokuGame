import time
import pygame
from pygame.locals import *
import sudoku

text_clr = (241, 236, 206)
selected_clr = (64, 121, 140)
background_clr = (51, 51, 51)

display_width = 1000
display_height = 700

previousWidth = 0
start = time.time()
count = 0

displace = 50

class Text:
    string = ''

    font_size = 30
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font(font_path, font_size)

    def set_text(self, str):
        self.string = str

    def draw_text(self, display):
        global previousWidth
        global start
        global count

        rect = pygame.Rect(displace // 2, displace // 2, display_width - displace, display_height - displace * 1.5)

        line_spacing = -8

        #text = self.font.render(self.string, True, text_clr)
        #text_rect = text.get_rect()

        top = rect.top
        height = self.font_size

        text = self.string

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if top + height > rect.bottom:
                break

            # determine maximum width of line
            while (self.font.size(text[:i])[0] < rect.width and i < len(text)):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            previousWidth = 0
            surfaces, positions = getSurfaces(self, text[:i], [rect.left, top])

            start = time.time()
            count = 0
            npc_running = True
            while npc_running:
                npc_running = npc_one_dialogue(surfaces, positions, display, npc_running)
                pygame.display.update()

            #image = self.font.render(text[:i], False, text_clr)
            #display.blit(image, (rect.left, top))

            top += height + line_spacing

            # remove the text we just blitted
            text = text[i:]

class Buttons:
    fields = []
    btn_texts = ["Menu", "Next"]

    displacement = int(32 * 0.2)

    pos_selected = -1

    def set_pos_selected(self, pos):
        self.pos_selected = pos

    def get_pos_selected(self):
        return self.pos_selected

    class Field:
        text = ''
        field = pygame.Surface
        field_rect = pygame.Rect
        selected_rect = pygame.Rect

    def create_buttons(self, text, display):
        for i in range(len(self.btn_texts)):
            self.fields.append(self.Field())

            self.fields[i].text = self.btn_texts[i]
            self.fields[i].field = text.font.render(self.btn_texts[i], True, text_clr)

            self.fields[i].field_rect = self.fields[i].field.get_rect()

            height = self.fields[i].field_rect.height + self.displacement * 2
            width = self.fields[i].field_rect.width + self.displacement * 2

            self.fields[i].field_rect.top = display_height - displace // 2 - height + self.displacement

            top = self.fields[i].field_rect.top - self.displacement

            if i == 0:
                self.fields[i].field_rect.left = displace // 2 + self.displacement
            elif i == 1:
                self.fields[i].field_rect.left = display_width - (displace // 2) - (width) + self.displacement

            left = self.fields[i].field_rect.left - self.displacement

            self.fields[i].selected_rect = (left, top, width, height)

    def draw_buttons(self, display):
        if self.pos_selected > -1:
            selected_rect = self.fields[self.pos_selected].selected_rect
            pygame.draw.rect(display, selected_clr, selected_rect)

            non_selected_rect = self.fields[(self.pos_selected + 1) % 2].selected_rect
            pygame.draw.rect(display, background_clr, non_selected_rect)

        for i in range(2):
            display.blit(self.fields[i].field, (self.fields[i].field_rect.left, self.fields[i].field_rect.top))

def getSurfaces(text, word, pos):
    global previousWidth

    surfaces = []
    positions  = []

    for i in range(len(word)):
        surf = text.font.render(f"{word[i]}", True, text_clr)
        surfaces.append(surf)

    for i in range(len(surfaces)):
        previousWidth += surfaces[i-1].get_rect().width
        positions.append([previousWidth + pos[0], pos[1]])

    return surfaces, positions

def npc_one_dialogue(surfaces, positions, display, running, delay=0.0000000008): # delay=0.04
    global start
    global count

    now = time.time()

    if not (count < len(surfaces)):
        running = False

    if count < len(surfaces):
        if now - start > delay:
            count += 1
            start = now

    for i in range(count):
        display.blit(surfaces[i], (positions[i][0], positions[i][1]))

    return running




scrn = -1

def set_screen(screen):
    global scrn
    scrn = screen

def get_screen():
    global scrn
    return scrn

def text_loop(display, screen, src_text):
    global scrn
    running_intro = True

    string = Text()
    buttons = Buttons()

    buttons.create_buttons(string, display)

    buttons.draw_buttons(display)

    with open(src_text, 'r') as file:
        intro_text = file.read().replace('\n', ' ').replace('  ', ' ')

    string.set_text(intro_text)

    string.draw_text(display)

    while running_intro:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if buttons.get_pos_selected() == 0:
                        buttons.set_pos_selected(1)
                    elif buttons.get_pos_selected() == -1:
                        buttons.set_pos_selected(0)
                    buttons.draw_buttons(display)
                if event.key == K_LEFT:
                    if buttons.get_pos_selected() == 1:
                        buttons.set_pos_selected(0)
                    elif buttons.get_pos_selected() == -1:
                        buttons.set_pos_selected(0)
                    buttons.draw_buttons(display)
                # Adjust this later if pressing down button is scrolling
                if event.key == K_DOWN or event.key == K_UP:
                    if buttons.get_pos_selected() == -1:
                        buttons.set_pos_selected(0)
                    buttons.draw_buttons(display)

                if event.key == K_RETURN:
                    if buttons.get_pos_selected() == 0:
                        running_intro = False
                        set_screen(screen)
                        break
                    if buttons.get_pos_selected() == 1:
                        # FIX: make more flexible, need to have each run after
                        # each other, currently a rather large mess
                        # and would require each to be added in individually
                        # rather than overarching mess of a thing going on

                        if src_text == 'raw_texts/intro.txt':
                            sudoku.sudoku_loop(display)
                            set_screen(screen + 1)
                            running_intro = False
                            break

                        elif src_text == 'raw_texts/decrypting.txt':
                            running_intro = False
                            break

                        elif src_text == 'raw_texts/first_message.txt':
                            running_intro = False
                            break

                if event.key == K_ESCAPE:
                    running_intro = False
                    pygame.quit()
                    quit()

            elif event.type == QUIT:
                running_intro = False
                pygame.quit()
                quit()

        pygame.display.update()
