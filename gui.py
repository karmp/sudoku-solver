"""This module contains the helper functions needed to run the Sudoku GUI."""

import pygame
from sudoku import Sudoku
from tkinter import filedialog, messagebox, Tk
from typing import List
from img_processing.sudoku_extractor import get_sudoku

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

# Set of valid key presses
KEY_PRESS= {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5, 
            pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9, pygame.K_DELETE: 10}


def draw_board(game_screen: pygame.display, solve_button_coord: tuple[int, int],
               upload_button_coord: tuple[int, int], edit_button_coord: tuple[int, int], 
               edit_mode: bool) -> None:
    """Draws the lines and buttons for Sudoku.
    
    Args:
        game_screen: pygame display object that the board will be draw on.
        solve_button_coord: coordinates of solve Sudoku Board button.
        upload_button_coord: coordinateese of upload box button.
        edit_utton_coord: coordinateese of edit box button.
        edit_mode: edit mode is enable or not
    """
    solve_button_x, solve_button_y = solve_button_coord
    upload_box_x, upload_box_y = upload_button_coord
    edit_button_x, edit_button_y = edit_button_coord

    for i in range(GRID_SIZE + 1):
        line_thickness = 2 if i % 3 == 0 else 1
        pygame.draw.line(game_screen, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), line_thickness)
        pygame.draw.line(game_screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT - CELL_SIZE), line_thickness)
    
    pygame.draw.rect(game_screen, BLACK, (solve_button_x, solve_button_y, 90, 30), 2)
    pygame.draw.rect(game_screen, BLACK, (upload_box_x, upload_box_y, 98, 30), 2)
    pygame.draw.rect(game_screen, BLACK, (edit_button_x, edit_button_y, 98, 30), 2)

    font = pygame.font.SysFont("Comic Sans", 14)
    solve_rect_text = font.render("Solve Board", True, BLACK)
    upload_text = font.render("Upload Image", True, BLACK)
    edit_text = font.render(f"Edit Mode: {'on' if edit_mode is True else 'off'}", True, BLACK)

    game_screen.blit(solve_rect_text, (solve_button_x + 5 , solve_button_y))
    game_screen.blit(upload_text, (upload_box_x + 5, upload_box_y))
    game_screen.blit(edit_text, (edit_button_x + 2, edit_button_y))


def draw_numbers(game_screen: pygame.display, board: List[List[int]]) -> None:
    """Draws the Sudoku numbers.
    
    Args:
        board: A standard 9x9 Sudoku board.
    """
    
    font = pygame.font.SysFont("Comic Sans", 36)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] != 0:
                number = font.render(str(board[row][col]), True, BLACK)
                x = col * CELL_SIZE + CELL_SIZE // 2 - number.get_width() // 2
                y = row * CELL_SIZE + CELL_SIZE // 2 - number.get_height() // 2
                game_screen.blit(number, (x, y))

def draw_selected_cell(game_screen: pygame.display, cell_coord: tuple[int,int]) -> None:
    """Draws a box around the Sudoku cell clicked on by the user.
    
    Args:
        game_screen: pygame display object that the board will be draw on.
        cell_coord: coordinate of the Sudoku cell that was clicked on.
    """
    # Ignore clicks made outside of the Sudoku grid
    if cell_coord[0] <= 8:
        x = cell_coord[1] * CELL_SIZE
        y = cell_coord[0] * CELL_SIZE
        pygame.draw.rect(game_screen, SELECTED_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 4)

def handle_key_press(sudoku: Sudoku, event: pygame.event,
                     selected_cell_coord: tuple[int, int], edit_mode: bool) -> bool:
    """Updates the board in the Sudoku object if the value inputted was valid.
    
    Args:
        sudoku: An instance of the Sudoku class.
        event: A pygame event representing the key that was pressed.
        selected_cell_coord: Coordinates of currently selected cell.
    
    Returns:
        True if value on the board was modified successfully, otherwise False.
    """
    key_pressed = KEY_PRESS.get(event.key)
    selected_row, selected_col = selected_cell_coord

    # Do not allow deleting values outside edit mode
    if event.key == pygame.K_DELETE and edit_mode is False:
        return False

   # Checked that the selected cell is empty and a non-valid key has not been pressed
    if key_pressed is not None:
        board = sudoku.get_board()
        if key_pressed != pygame.K_DELETE and board[selected_row][selected_col] == 0:
            solved_board = sudoku.get_solved_board()
            if solved_board[selected_row][selected_col] == key_pressed or edit_mode is True:
                sudoku.place_value(selected_row, selected_col, key_pressed)
                return True
            else:
                # Incorrect value was given that is not a part of solution
                return False
            
        elif event.key == pygame.K_DELETE:
            sudoku.place_value(selected_row, selected_col, 0)
            return True
        
    return False

def draw_incorrect_input(game_screen: pygame.display) -> None:
    """Draws an 'X' on game screen to indicate wrong value was inputted into a Sudoku Cell.
    
    Args:
        game_screen: pygame display object that the board will be draw on.
    """
    pygame.draw.line(game_screen, INCORRECT_COLOR, (0, SCREEN_HEIGHT - 50), (50, SCREEN_HEIGHT), 3)
    pygame.draw.line(game_screen, INCORRECT_COLOR, (0, SCREEN_HEIGHT), (50, SCREEN_HEIGHT - 50), 3)

def upload_and_process_image(sudoku: Sudoku) -> None:
    """Prompts user to upload an image file. Stores the file path of the image and processes
    the image and converts it into a nested list that will be used to update the board of
    Sudoku object.
    
    Args:
        sudoku: An instance of the Sudoku class.
    """
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    if filename == "":
        return
    file_extension = filename.split(".")
    if file_extension[-1] not in ["png", "jpg", "jpeg"]:
        messagebox.showinfo(title="Invalid file.", message="Please upload a .png or .jpg/jpeg file.")
    try:
        messagebox.showinfo(title= "Processing", message="Processing image.")
        board = get_sudoku(filename)
        sudoku.set_board(board)

    except Exception as e:
        print(e)
        messagebox.showinfo("An error occured.")
