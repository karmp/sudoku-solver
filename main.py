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
    solve_button_x = (SCREEN_WIDTH // 2) - 45
    solve_button_y = SCREEN_HEIGHT - 45
    upload_button_x = SCREEN_WIDTH - 100
    upload_button_y = solve_button_y
    edit_button_x =  45
    edit_button_y = solve_button_y
    show_solution, upload_image_flag, edit_mode = False, False, False

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
                if selected_row == 9 and 0 <= selected_col <= 2 and edit_mode is False:
                    edit_mode = True
                elif selected_row == 9 and 0 <= selected_col <= 2 and edit_mode is True:
                    edit_mode = False
                elif edit_mode is True or upload_image_flag is True:
                    edit_mode = True
                else:
                    False

            
            if event.type == pygame.KEYUP:
                correct_input = handle_key_press(sudoku, event,
                                                 (selected_row, selected_col), edit_mode)

        # Redraw game board after event
        game_screen.fill(WHITE)
        draw_board(game_screen, (solve_button_x, solve_button_y), (upload_button_x, upload_button_y),
                   (edit_button_x, edit_button_y), edit_mode)
        
        # Update game board with solution if button was clicked
        if show_solution is True:
            sudoku.update_solved_board() # Account for any modifications made to game board 
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
        show_solution, upload_image_flag = False, False

if __name__ == "__main__":
    main()
