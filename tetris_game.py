# ===============================================================================================#
# Name        : Tetris.py                                                                       #
# Description : Python version of the tetris game                                               #
# Author      : Nguyen Vu Tuong Lam                                                             #
# Date        : 08.11.2017                                                                      #
# --------------------------------------------------------------------------------------------- #
# Updated     : 10.10.2019                                                                      #
# By          : Ronja Faltin                                                                    #
# ===============================================================================================#


from random import randrange as rand

import pygame
import sys

# The configuration
cell_size = 30
cell_size_inner = 30
cols = 10
rows = 22
max_fps = 30
font_size = 16
pygame.init()
pygame.mixer.init()

colors = [
    (0, 0, 0),
    (237, 80, 104),   # Pink
    (255, 176, 0),    # Orange
    (31, 163, 158),   # Bluegreen
    (35, 51, 135),    # Blue
    (250, 128, 114),  # Salmon
    (230, 220, 210),  # Cream white
    (255, 119, 0),    # Yellow
    (20, 20, 20)  # Helper color for background grid
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]


# ================================================================================================#
#                                       Function Definitions                                     #
# ================================================================================================#

def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


def remove_row(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board


def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy + off_y - 1][cx + off_x] += val
    return mat1


def board():
    board = [[0 for x in range(cols)]
             for y in range(rows)]
    board += [[1 for x in range(cols)]]
    return board


# ================================================================================================#
#                                       Main Game Part                                           #
# ================================================================================================#

class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat()  # Delay in milliseconds (250, 25) -> No delay needed?
        self.width = cell_size * (cols + 6)
        self.height = cell_size * rows
        self.r_lim = cell_size * cols
        # MAke the grid in the background, 8 and 3 is the color
        self.b_ground_grid = [[8 if x % 2 == y % 2 else 0 for x in range(cols)] for y in range(rows)]

        #  Change the font in the game
        self.default_font = pygame.font.Font(
            pygame.font.get_default_font(), font_size)

        self.screen = pygame.display.set_mode((self.width, self.height))
        # We do not need mouse movement events, so we block them.
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(cols / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    def display_msg(self, msg, top_left):
        x, y = top_left
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(line, False, (255, 255, 255), (0, 0, 0)), (x, y))
            y += 30

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, False,
                                                 (0, 0, 255), (0, 0, 0))
            msg_im_center_x, msg_im_center_y = msg_image.get_size()
            msg_im_center_x //= 2
            msg_im_center_y //= 2

            self.screen.blit(msg_image, (
                self.width // 2 - msg_im_center_x,
                self.height // 2 - msg_im_center_y + i * 22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, colors[val],
                                     pygame.Rect((off_x + x) * cell_size, (off_y + y) * cell_size, cell_size_inner,
                                                 cell_size_inner), 0)
                    pygame.draw.rect(self.screen, colors[val],
                                     pygame.Rect((off_x + x) * cell_size, (off_y + y) * cell_size, cell_size,
                                                 cell_size), 2)

    def add_cl_lines(self, n):
        line_scores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += line_scores[n] * self.level
        if self.lines >= self.level * 6:
            self.level += 1
            new_delay = 1000 - 50 * (self.level - 1)
            new_delay = 100 if new_delay < 100 else new_delay
            pygame.time.set_timer(pygame.USEREVENT + 1, new_delay)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    def drop(self, boolean):
        if not self.gameover and not self.paused:
           #self.score += 1 if boolean else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(
                    self.board,
                    self.stone,
                    (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    '''def instant_drop(self):
        if not self.gameover and not self.paused:
            while not self.drop(True):
                pass
                '''

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def get_game_score(self):
        return self.score

    def run(self):
        key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': lambda: self.drop(True),
            'UP': self.rotate_stone,
            'p': self.toggle_pause,
           # 'RETURN': self.instant_drop
        }

        self.gameover = False
        self.paused = False

        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0, 0, 0))
            if self.gameover:
                self.score -= 2
                self.center_msg("""Game Over!\nYour score: %dPress Any Key to continue""" % self.score)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()
                    elif event.type == pygame.KEYDOWN:
                        self.start_game()

            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    pygame.draw.line(self.screen,
                                     (255, 255, 255),
                                     (self.r_lim + 1, 0),
                                     (self.r_lim + 1, self.height - 1))
                    self.display_msg("Next:", (
                        self.r_lim + cell_size,
                        2))
                    self.display_msg("Score: %d\nLevel: %d\nLines: %d" % (self.score, self.level, self.lines),
                                     (self.r_lim + cell_size, cell_size * 5))
                    self.draw_matrix(self.b_ground_grid, (0, 0))
                    self.draw_matrix(self.board, (0, 0))
                    self.draw_matrix(self.stone,
                                     (self.stone_x, self.stone_y))
                    self.draw_matrix(self.next_stone,
                                     (cols + 1, 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                                             + key):
                            key_actions[key]()
            dont_burn_my_cpu.tick(max_fps)


if __name__ == '__main__':
    App = TetrisApp()
    App.run()