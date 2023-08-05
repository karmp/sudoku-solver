import pygame, sys, copy
from board import Sudoku

# Constants for the game window
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 500
GRID_SIZE = 9
CELL_SIZE = 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
SELECTED_COLOR = (100, 100, 255)
INCORRECT_COLOR = (255, 0, 0)

# Mapping Key presses to numbers
KEY_PRESS= {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
            pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
            pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9,
            }


def draw_board(game_screen, solve_button_x, solve_button_y):
    for i in range(GRID_SIZE + 1):
        line_thickness = 2 if i % 3 == 0 else 1
        pygame.draw.line(game_screen, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), line_thickness)
        pygame.draw.line(game_screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT - CELL_SIZE), line_thickness)
    
    pygame.draw.rect(game_screen, BLACK, (solve_button_x, solve_button_y, 80, 30), 3)
    font = pygame.font.SysFont("Comic Sans", 14)
    solve_rect_text = font.render("Solve Board", True, BLACK)
    game_screen.blit(solve_rect_text, (solve_button_x , solve_button_y))

def draw_numbers(game_screen, board):
    font = pygame.font.Font(None, 36)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] != 0:
                number = font.render(str(board[row][col]), True, BLACK)
                x = col * CELL_SIZE + CELL_SIZE // 2 - number.get_width() // 2
                y = row * CELL_SIZE + CELL_SIZE // 2 - number.get_height() // 2
                game_screen.blit(number, (x, y))

def draw_selected_cell(game_screen, row, col):
    if row <= 8:
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        pygame.draw.rect(game_screen, SELECTED_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 4)

def handle_key_press(game_screen, sudoku, event: pygame.event, solved_sudoku, selected_row, selected_col) -> int:
    key_pressed = KEY_PRESS.get(event.key)
    board = sudoku.get_board()
    if key_pressed is not None and board[selected_row][selected_col] == 0:
        solved_board = solved_sudoku.get_board()
        if solved_board[selected_row][selected_col] == key_pressed:
            sudoku.place_value(selected_row, selected_col, key_pressed)
            return 0
        else:
            #incorrect value was given
            return 1

def draw_incorrect_input(game_screen):
    pygame.draw.line(game_screen, INCORRECT_COLOR, (0, SCREEN_HEIGHT - 50), (50, SCREEN_HEIGHT), 3)
    pygame.draw.line(game_screen, INCORRECT_COLOR, (0, SCREEN_HEIGHT), (50, SCREEN_HEIGHT - 50), 3)

def main():
    pygame.init()
    game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku")
    sudoku = Sudoku()
    solved_sudoku = Sudoku(copy.deepcopy(sudoku._board))
    solved_sudoku.solve_board()
    selected_row, selected_col = 0, 0
    correct_input = 0
    solve_button_x = (SCREEN_WIDTH // 2) - 40
    solve_button_y = SCREEN_HEIGHT - 40

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                selected_rect = pygame.mouse.get_pos() # Top left is 0,0
                selected_row = selected_rect[1] // CELL_SIZE
                selected_col = selected_rect[0] // CELL_SIZE
            
            if event.type == pygame.KEYUP:
                correct_input = handle_key_press(game_screen, sudoku, event, solved_sudoku, 
                                                 selected_row, selected_col)

        game_screen.fill(WHITE)
        draw_board(game_screen, solve_button_x, solve_button_y)
        if selected_row ==  9 and 3 <= selected_col <= 5:
            sudoku.set_board(solved_sudoku.get_board())
        
        draw_numbers(game_screen, sudoku.get_board())
        draw_selected_cell(game_screen, selected_row, selected_col)
        if correct_input == 1:
            draw_incorrect_input(game_screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
