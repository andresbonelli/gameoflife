import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# CONSTANTS
FPS = 30

ROWS, COLS = 30, 60

CELL_WIDTH, CELL_HEIGHT = 20, 20

WIDTH, HEIGHT = COLS * CELL_WIDTH, ROWS * CELL_HEIGHT

# COLORS
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (211, 211, 211)
SILK = (187, 173, 160)
ASH_GRAY = (205, 192, 180)
BEAR_GRAY = (119, 110, 101)

OUTLINE_COLOR = SILK
OUTLINE_THICKNESS = 2
BACKGROUND_COLOR = ASH_GRAY
FONT_COLOR = BEAR_GRAY

FONT = pygame.font.SysFont("comicsans", 10, bold=True)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Of Life - (press <SPACE> to start, <C> to clear the board, <R> to fill random)")


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = np.zeros((self.rows, self.cols), dtype=np.int0)

    def toggle_cell(self, row, col):
        self.cells[row][col] ^= 1  # bitwise swap 1 and 0

    def randomize(self):
        self.cells = [[random.choice([0, 0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]

    def clear(self):
        self.cells = np.zeros((self.rows, self.cols), dtype=np.int0)

    def next_iteration(self):
        temp_cells = np.zeros((ROWS, COLS), dtype=np.int0)
        for row in range(self.rows):
            for col in range(self.cols):
                neighbours = sum(self.cells[i][j]          # sum values of adjacent cells
                                 for i in range(max(0, row - 1), min(self.rows, row + 2))
                                 for j in range(max(0, col - 1), min(self.cols, col + 2))
                                 ) - self.cells[row][col]  # cell can't be its own neighbour!
                if self.cells[row][col] == 1 and (neighbours < 2 or neighbours > 3):
                    temp_cells[row][col] = 0
                elif self.cells[row][col] == 0 and neighbours == 3:
                    temp_cells[row][col] = 1
                else:
                    temp_cells[row][col] = self.cells[row][col]
        self.cells = temp_cells

def draw_grid(window):
    for row in range(1, ROWS):
        y = row * CELL_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
    for col in range(1, COLS):
        x = col * CELL_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw_cells(window, board):
    for row in range(ROWS):
        for col in range(COLS):
            cell_color = RED if board.cells[row][col] == 1 else WHITE
            pygame.draw.rect(window, cell_color, [col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT])

def draw(window, board):
    window.fill(WHITE)
    draw_cells(window, board)
    draw_grid(window)

    pygame.display.update()

# Main game loop
def main(window):
    clock = pygame.time.Clock()
    fps = FPS
    run = True
    run_game = False

    board = Board(ROWS, COLS)

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // CELL_HEIGHT
                col = x // CELL_WIDTH
                board.toggle_cell(row, col)  # Toggle the cell state
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB or event.key == pygame.K_RIGHT:
                    board.next_iteration()
                elif event.key == pygame.K_SPACE:
                    run_game = not run_game
                elif event.key == pygame.K_r:
                    board.randomize()
                elif event.key == pygame.K_c:
                    board.clear()
                elif event.key == pygame.K_q or event.key == pygame.K_MINUS:
                    pass
                elif event.key == pygame.K_w or event.key == pygame.K_PLUS:
                    pass

        if run_game:
            board.next_iteration()

        draw(window, board)

    pygame.quit()


if __name__ == '__main__':
    main(WINDOW)
