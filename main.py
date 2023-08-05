import pygame, sys
from sudoku import Sudoku
from gui import *


def main() -> None:
    """Runs, the Sudoku GUI."""
    # Setup game screen and sudoku object
    pygame.init()
    game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Solver")
    sudoku = Sudoku()

    # Set up variables
    selected_row, selected_col = 0, 0
    correct_input = 0
    solve_button_x = (SCREEN_WIDTH // 2) - 40
    solve_button_y = SCREEN_HEIGHT - 40
    upload_box_x = SCREEN_WIDTH - 100
    upload_box_y = solve_button_y
    show_solution, upload_image_flag = False, False

    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                selected_rect = pygame.mouse.get_pos() # Top left is 0,0
                selected_row = selected_rect[1] // CELL_SIZE
                selected_col = selected_rect[0] // CELL_SIZE
                
                # Check and update Flags
                show_solution = True if selected_row ==  9 and 3 <= selected_col <= 5 else False
                upload_image_flag = True if selected_row == 9 and 7 <= selected_col <= 8 else False
            
            if event.type == pygame.KEYUP:
                correct_input = handle_key_press(game_screen, sudoku, event, (selected_row, selected_col))

        # Redraw game board after event
        game_screen.fill(WHITE)
        draw_board(game_screen, (solve_button_x, solve_button_y), (upload_box_x, upload_box_y))
        
        # Update game board with solution if button was clicked
        if show_solution is True:
            sudoku.set_board(sudoku.get_solved_board())
        
        # Handle uploading and processing button being clicked
        if upload_image_flag is True:
            upload_and_process_image(sudoku)
        
        # Finish drawing sudoku board
        draw_numbers(game_screen, sudoku.get_board())
        draw_selected_cell(game_screen, (selected_row, selected_col))
        
        # Incorrect number inputted in Sudoku cell by user
        if correct_input is False and selected_row <= 8 and selected_col <= 8:
            draw_incorrect_input(game_screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
