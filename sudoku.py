import pygame
from pygame.locals import *
import itertools
from time import sleep

pygame.font.init()

background_clr = (51,51,51)
text_clr = (241, 236, 206)
selected_clr = (64, 121, 140)
sud_clr = (27, 82, 153)

# displace everything 50px from top and 50 from left
display_width = 1000
display_height = 700
sudoku_size = 500
horizontal_displace = (display_width - sudoku_size) // 2
vertical_displace = 50

class Sudoku:
    font_size = 48
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font(font_path, font_size)

    ch_font_path = 'data/noto/NotoSansJP-Regular.otf'

    ch_font_size = 48
    jp_font_size = 16

    ch_font = pygame.font.Font(ch_font_path, ch_font_size)
    jp_font = pygame.font.Font(ch_font_path, jp_font_size)

    # sudoku in chinese and japanese according to wikipedia
    ch_title = "数独"
    jp_title = "すうどく"

    # sets size of each sudoku block
    diff = sudoku_size / 9
    defaultgrid = [
            [7, 0, 0, 0, 0, 8, 0, 5, 0],
            [0, 0, 0, 3, 0, 0, 8, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 9, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 3, 0, 0],
            [6, 0, 0, 0, 0, 2, 0, 0, 1],
            [0, 0, 0, 0, 5, 0, 0, 2, 4],
            [1, 0, 0, 0, 0, 7, 5, 0, 0],
            [8, 4, 0, 0, 0, 6, 1, 0, 0],
        ]
    grid = [
            [7, 0, 0, 0, 0, 8, 0, 5, 0],
            [0, 0, 0, 3, 0, 0, 8, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 9, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 3, 0, 0],
            [6, 0, 0, 0, 0, 2, 0, 0, 1],
            [0, 0, 0, 0, 5, 0, 0, 2, 4],
            [1, 0, 0, 0, 0, 7, 5, 0, 0],
            [8, 4, 0, 0, 0, 6, 1, 0, 0],
        ]
    solved_grid = [
            [7, 3, 1, 6, 4, 8, 2, 5, 9],
            [2, 9, 4, 3, 7, 5, 8, 1, 6],
            [5, 8, 6, 1, 2, 9, 7, 4, 3],
            [4, 5, 8, 9, 1, 3, 6, 7, 2],
            [9, 1, 2, 7, 6, 4, 3, 8, 5],
            [6, 7, 3, 5, 8, 2, 4, 9, 1],
            [3, 6, 7, 8, 5, 1, 9, 2, 4],
            [1, 2, 9, 4, 3, 7, 5, 6, 8],
            [8, 4, 5, 2, 9, 6, 1, 3, 7],
        ]
    x = 0
    z = 0

    sudoku_surface = pygame.Surface((sudoku_size, sudoku_size))
    sudoku_surface.fill(background_clr)

    def set_defaultgrid(self, grid):
        self.defaultgrid = grid.copy()

    def set_grid(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid

    def set_fontsize(self, font_size):
        self.font_size = font_size

    def set_font(self, path):
        self.font_path = path

    def set_gridvalue(self, value):
        # checks if the selected square is one of the default values
        if self.defaultgrid[int(self.x)][int(self.z)] == 0:
            self.grid[int(self.x)][int(self.z)] = value

    def draw_title(self, display):
        ch_text = self.ch_font.render(self.ch_title, True, text_clr)
        ch_text_rect = ch_text.get_rect(center=(display_width/2, vertical_displace))
        display.blit(ch_text, ch_text_rect)

        jp_text = self.jp_font.render(self.jp_title, True, text_clr)
        jp_text_rect = jp_text.get_rect(center=(display_width/2, vertical_displace + self.ch_font_size))
        display.blit(jp_text, jp_text_rect)

    # highlights selected cell by the user
    def highlightbox(self, display):
        for k in range(2):
            pygame.draw.line(self.sudoku_surface, text_clr, (self.x * self.diff-3, (self.z + k) * self.diff), (self.x * self.diff + self.diff + 3, (self.z + k) * self.diff), 7)
            pygame.draw.line(self.sudoku_surface, text_clr, ((self.x + k) * self.diff, self.z * self.diff ), ((self.x + k) * self.diff, self.z * self.diff + self.diff), 7)

        display.blit(self.sudoku_surface, (horizontal_displace, vertical_displace * 2 + vertical_displace // 2))

        # the highlights were staying in the background because they were still
        # on sudoku_surface, then drawn over in drawlines(), hence make the drawlines
        # match the background color
        for k in range(2):
            pygame.draw.line(self.sudoku_surface, background_clr, (self.x * self.diff-3, (self.z + k) * self.diff), (self.x * self.diff + self.diff + 3, (self.z + k) * self.diff), 7)
            pygame.draw.line(self.sudoku_surface, background_clr, ((self.x + k) * self.diff, self.z * self.diff ), ((self.x + k) * self.diff, self.z * self.diff + self.diff), 7)

    # draws the lines of the sudoku grid
    def drawlines(self, display):
        for i in range (9):
            for j in range (9):
                if self.grid[i][j] != 0:
                    if self.defaultgrid[i][j] != 0:
                        pygame.draw.rect(self.sudoku_surface, sud_clr, (i * self.diff, j * self.diff, self.diff + 1, self.diff + 1))
                    else:
                        pygame.draw.rect(self.sudoku_surface, selected_clr, (i * self.diff, j * self.diff, self.diff + 1, self.diff + 1))

                    # renders the font
                    text1 = self.font.render(str(self.grid[i][j]), 1, text_clr)

                    # copies content from one surface to another
                    self.sudoku_surface.blit(text1, (i * self.diff + 20, j * self.diff + 20))
                elif self.grid[i][j] == 0:
                    pygame.draw.rect(self.sudoku_surface, background_clr, (i * self.diff, j * self.diff, self.diff + 1, self.diff + 1))

        for l in range(10):
            if l % 3 == 0 :
                thick = 7
            else:
                thick = 1
            pygame.draw.line(self.sudoku_surface, (0, 0, 0), (0, l * self.diff), (500, l * self.diff), thick)
            pygame.draw.line(self.sudoku_surface, (0, 0, 0), (l * self.diff, 0), (l * self.diff, 500), thick)

        display.blit(self.sudoku_surface, (horizontal_displace, vertical_displace * 2 + vertical_displace // 2))

        self.draw_title(display)

def sudoku_ok(line):
    line = list(filter(lambda num: num != 0, line))
    return (len(line) == 9 and sum(line) == sum(set(line)))

def check_sudoku(grid):
    bad_rows = [row for row in grid if not sudoku_ok(row)]

    grid = list(zip(*grid))
    bad_cols = [col for col in grid if not sudoku_ok(col)]

    squares = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):

            square = list(itertools.chain(row[j:j+3] for row in grid[i:i+3]))

            new_square = []
            for k in range(len(square)):
                for l in range(len(square[k])):
                    new_square.append(list(square[k])[l])
            square = new_square

            squares.append(square)
    bad_squares = [square for square in squares if not sudoku_ok(square)]

    return not (bad_rows or bad_cols or bad_squares)

class Buttons:
    fields = []
    btn_texts = ["Menu", "Reset", "Check"]

    displacement = int(32 * 0.2)

    pos_selected = -1
    pos_change = (0,0)

    def set_pos_selected(self, pos):
        self.pos_selected = pos

    def get_pos_selected(self):
        return self.pos_selected

    class Field:
        text = ''
        field = pygame.Surface
        field_rect = pygame.Rect
        selected_rect = pygame.Rect

    def create_buttons(self, sudoku, display):
        for i in range(len(self.btn_texts)):
            self.fields.append(self.Field())

            self.fields[i].text = self.btn_texts[i]
            self.fields[i].field = sudoku.font.render(self.btn_texts[i], True, text_clr)

            self.fields[i].field_rect = self.fields[i].field.get_rect()

            height = self.fields[i].field_rect.height + self.displacement * 2
            width = self.fields[i].field_rect.width + self.displacement * 2

            self.fields[i].field_rect.top = display_height - vertical_displace // 2 - height + self.displacement

            top = self.fields[i].field_rect.top - self.displacement

            if i == 0:
                self.fields[i].field_rect.left = display_width // 4 + self.displacement
            elif i == 1:
                self.fields[i].field_rect.left = (display_width // 2) - (width // 2) + self.displacement
            elif i == 2:
                self.fields[i].field_rect.left = display_width - display_width // 4 - (width) + self.displacement

            left = self.fields[i].field_rect.left - self.displacement

            self.fields[i].selected_rect = (left, top, width, height)

    def draw_buttons(self, display):
        if self.pos_selected > -1:
            selected_rect = self.fields[self.pos_selected].selected_rect
            pygame.draw.rect(display, selected_clr, selected_rect)

        for i in range(3):
            display.blit(self.fields[i].field, (self.fields[i].field_rect.left, self.fields[i].field_rect.top))


def sudoku_loop(display):
    # used for running the window
    running_sudoku = True
    value = 0

    print("Running Sudoku loop")

    # initialize sudoku class instance
    sudoku = Sudoku()

    buttons = Buttons()

    buttons.create_buttons(sudoku, display)

    while running_sudoku:
        display.fill(background_clr)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if (sudoku.x > 0 and not sudoku.z > 8):
                        sudoku.x -= 1
                    elif sudoku.z > 8 and not buttons.get_pos_selected() == 0:
                        buttons.set_pos_selected(buttons.get_pos_selected() - 1)
                if event.key == pygame.K_RIGHT:
                    if (sudoku.x < 8 and not sudoku.z > 8):
                        sudoku.x += 1
                    elif sudoku.z > 8 and not buttons.get_pos_selected() == 2:
                        buttons.set_pos_selected(buttons.get_pos_selected() + 1)

                if event.key == pygame.K_UP:
                    if (sudoku.z > 8):
                        if buttons.get_pos_selected() == 0:
                            sudoku.x = 1
                        elif buttons.get_pos_selected() == 1:
                            sudoku.x = 4
                        elif buttons.get_pos_selected() == 2:
                            sudoku.x = 7
                        buttons.set_pos_selected(-1)
                    if (sudoku.z > 0):
                        sudoku.z -= 1

                if event.key == pygame.K_DOWN:
                    if (sudoku.z < 8):
                        sudoku.z += 1
                    elif sudoku.z == 8:
                        sudoku.z += 1
                        if sudoku.x < 3:
                            buttons.set_pos_selected(0)
                        elif sudoku.x > 5:
                            buttons.set_pos_selected(2)
                        else:
                            buttons.set_pos_selected(1)

                # changes "value" depending on key pressed
                # sets grid value at every key press
                if event.key == pygame.K_0:
                    value = 0
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_1:
                    value = 1
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_2:
                    value = 2
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_3:
                    value = 3
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_4:
                    value = 4
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_5:
                    value = 5
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_6:
                    value = 6
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_7:
                    value = 7
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_8:
                    value = 8
                    sudoku.set_gridvalue(value)
                if event.key == pygame.K_9:
                    value = 9
                    sudoku.set_gridvalue(value)

                if event.key == K_RETURN:
                    if buttons.get_pos_selected() == 0:
                        running_sudoku = False
                        break
                    if buttons.get_pos_selected() == 1:
                        # .copy() still retains link to original object
                        # BUG: going to menu and back doesn't keep resetted grid somehow
                        # After resetting, it does not save your current grid?
                        # But does before resetting? And I have no clue why it behaves like that
                        # Somehow initiates with state of grid before reset
                        # Can be circumvented, but also, this is a mess of a code
                        # And there seems to be no end in sight for the mess
                        # Fuck.
                        sudoku.set_grid([
                                [7, 0, 0, 0, 0, 8, 0, 5, 0],
                                [0, 0, 0, 3, 0, 0, 8, 0, 0],
                                [0, 0, 6, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 9, 0, 0, 0, 0, 0],
                                [0, 0, 2, 0, 0, 0, 3, 0, 0],
                                [6, 0, 0, 0, 0, 2, 0, 0, 1],
                                [0, 0, 0, 0, 5, 0, 0, 2, 4],
                                [1, 0, 0, 0, 0, 7, 5, 0, 0],
                                [8, 4, 0, 0, 0, 6, 1, 0, 0],
                            ])
                        sudoku.sudoku_surface.fill(background_clr)
                    if buttons.get_pos_selected() == 2:
                        print("Checking if sudoku is correct")
                        print(check_sudoku(sudoku.get_grid()))


                        if check_sudoku(sudoku.get_grid() == True):
                            running_sudoku = False
                        break
                        


                if event.key == K_ESCAPE:
                    running_sudoku = False
                    pygame.quit()
                    quit()

            elif event.type == QUIT:
                running_sudoku = False
                pygame.quit()
                quit()

        sudoku.drawlines(display)

        if not sudoku.z > 8:
            sudoku.highlightbox(display)

        buttons.draw_buttons(display)

        pygame.display.update()
