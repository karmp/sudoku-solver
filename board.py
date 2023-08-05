from typing import List, Optional

class SudokuBoard:
    """Sudoku Board class that stores a sudoku board. Member functions
    can be called on to solve the stored board, print the board, get the
    board, or replace the board.
    """
    
    def __init__(self, board: Optional[List[List[int]]] = None):
        """Initializes the sudoku board.
        
        Args:
            board: An optional argument to intialize the sudoku board.
        """
        if board == None:
            self._board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                        [6, 0, 0, 1, 9, 5, 0, 0, 0],
                        [0, 9, 8, 0, 0, 0, 0, 6, 0],
                        [8, 0, 0, 0, 6, 0, 0, 0, 3],
                        [4, 0, 0, 8, 0, 3, 0, 0, 1],
                        [7, 0, 0, 0, 2, 0, 0, 0, 6],
                        [0, 6, 0, 0, 0, 0, 2, 8, 0],
                        [0, 0, 0, 4, 1, 9, 0, 0, 5],
                        [0, 0, 0, 0, 8, 0, 0, 7, 9]
                        ]
        else:
            self._board = board

    def print_board(self) -> None:
        """Prints out Sudoku Board."""
        for i in range(len(self._board)):
            if i % 3 == 0:
                print(f"{'-' * 21}")
            
            for j in range(len(self._board[0])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                
                if j == 8:
                    print(self._board[i][j])
                else:
                    print(str(self._board[i][j]) + " ", end="")
        print(f"{'-' * 21}")

    def _find_empty_cell(self) -> tuple | None:
        """Finds the postion of an empty cell on the board if it exists.
        
        Returns:
            (row, col) tuple corresponding to position of empty cell on the board.
            None if no empty cells were found.
        """
        for i in range(len(self._board)):
            for j in range(len(self._board[0])):
                if self._board[i][j] == 0:
                    return (i, j) # Row, col of empty cell
        
        return None #When no empty cells left
    
    def _check_valid_placement(self, num_placed: int, position: tuple) -> bool:
        """Checks if the placement of a number on the board was valid.
        
        Args:
            num_place: The number that was placed on the board.
            position: The postion that the number was placed on. (0, 0) is top left corner.
        
        Returns:
            True if the placement was valid otherwise False.
        """
        # Check col if it's a valid placement
        for i in range(len(self._board)):
            if position[0] != i and self._board[i][position[1]] == num_placed:
                return False
        
        # Check row if it's a valid placement
        for i in range(len(self._board[0])):
            if position[1] != i and self._board[position[0]][i] == num_placed:
                return False
            
        # Check current 3x3 if it's a valid placement
        cur_box_row, cur_box_col = position[0] // 3, position[1] // 3
        for i in range(cur_box_row * 3, cur_box_row * 3 + 3): 
            for j in range(cur_box_col * 3, cur_box_col * 3 + 3):
                if (i, j) != position and self._board[i][j] == num_placed:
                    return False
        return True

    def solve_board(self):
        """Solves the board using backtracking algorithm. Updates the member variable
        with the solved board.
        """
        found_cell = self._find_empty_cell()
        
        # Solution was found
        if found_cell is None:
            return True

        # Try to place a number in an empty cell
        for i in range(1, 10):
            if self._check_valid_placement(i, (found_cell[0], found_cell[1])) == True:
                self._board[found_cell[0]][found_cell[1]] = i
            
                # Recursively search for a solution, backtrack when current solution does not work
                if self.solve_board() == True:
                    return True
                self._board[found_cell[0]][found_cell[1]] = 0
        
        return False
    
    def get_board(self) -> List[List[int]]:
        """Returns the sudoku board."""
        return self._board

    def set_board(self, board: List[List[int]]):
        """Sets the sudoku board. Must be a 9x9 sudoku board."""
        self._board = board
    
if __name__ == "__main__":
    board = SudokuBoard()
    board.print_board()
    board.solve_board()
    print("\n\n")
    board.print_board()