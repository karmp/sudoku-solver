from typing import List, Optional
import copy


class Sudoku:
    """Sudoku class that stores a Sudoku board. Member functions
    can be called on to solve the stored board, print the board, get the
    board, or replace the board.
    """
    
    def __init__(self, board: Optional[List[List[int]]] = None):
        """Initializes the Sudoku board.
        
        Args:
            board: An optional argument to intialize the Sudoku board.
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
            self._solved_board = self.solve_board(copy.deepcopy(self._board))            
        
        else:
            self._board = board
            self._solved_board = self.solve_board(copy.deepcopy(board))

    def print_board(self, board: Optional[List[List[int]]] = None) -> None:
        """Prints out Sudoku Board.
        
        Args:
            board: A nested list of integers representing a Sudoku board. If not used
            The member variable stored by the object when intialized will be used instead.
        """
        if board == None:
            board = self._board

        for i in range(len(board)):
            if i % 3 == 0:
                print(f"{'-' * 21}")
            
            for j in range(len(board[0])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                
                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")
        print(f"{'-' * 21}")

    def _find_empty_cell(self, board: Optional[List[List[int]]] = None) -> tuple | None:
        """Finds the postion of an empty cell on the board if it exists.
        
        Args:
            board: A nested list of integers representing a Sudoku board. If not used.
            The member variable stored by the object when intialized will be used instead.
        
        Returns:
            (row, col) tuple corresponding to position of empty cell on the board.
            None if no empty cells were found.
        """
        if board == None:
            board = self._board

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j) # Row, col of empty cell
        
        return None #When no empty cells left
    
    def _check_valid_placement(self, num_placed: int, position: tuple, 
                               board: Optional[List[List[int]]] = None) -> bool:
        """Checks if the placement of a number on the board was valid.
        
        Args:
            num_place: The number that was placed on the board.
            position: The postion that the number was placed on. (0, 0) is top left corner.
            board: A nested list of integers representing a Sudoku board. If not used.
            The member variable stored by the object when intialized will be used instead.
    
        Returns:
            True if the placement was valid otherwise False.
        """
        if board == None:
            board = self._board

        # Check col if it's a valid placement
        for i in range(len(board)):
            if position[0] != i and board[i][position[1]] == num_placed:
                return False
        
        # Check row if it's a valid placement
        for i in range(len(board[0])):
            if position[1] != i and board[position[0]][i] == num_placed:
                return False
            
        # Check current 3x3 if it's a valid placement
        cur_box_row, cur_box_col = position[0] // 3, position[1] // 3
        for i in range(cur_box_row * 3, cur_box_row * 3 + 3): 
            for j in range(cur_box_col * 3, cur_box_col * 3 + 3):
                if (i, j) != position and board[i][j] == num_placed:
                    return False
        return True

    def solve_board(self, board: Optional[List[List[int]]] = None) -> List[List[int]] | bool:
        """Solves the board using backtracking algorithm. Updates the member variable
        with the solved board.

        Args:
            board: A nested list of integers representing a Sudoku board. If not used
            The member variable stored by the object when intialized will be used instead.

        Returns:
            The solved Sudoku board as a nested list of integers if successful, otherwise False.
        """
        if board == None:
            board = self._board
    
        found_cell = self._find_empty_cell(board)

        # Solution was found
        if found_cell is None:
            return board

        # Try to place a number in an empty cell
        for i in range(1, 10):
            if self._check_valid_placement(i, (found_cell[0], found_cell[1]), board) == True:
                board[found_cell[0]][found_cell[1]] = i
            
                # Recursively search for a solution, backtrack when current solution does not work
                if self.solve_board(board):
                    return board
                board[found_cell[0]][found_cell[1]] = 0
        
        return False
    
    def get_board(self) -> List[List[int]]:
        """Returns the Sudoku board."""
        return self._board

    def set_board(self, board: List[List[int]]) -> None:
        """Sets the Sudoku board. Must be a 9x9 Sudoku board."""
        self._board = board

    def place_value(self, row_index: int, col_index: int, num: int) -> None:
        """Places a value on the board."""
        self._board[row_index][col_index] = num
    
    def get_solved_board(self) -> List[List[int]]:
        "Returns solved Sudoku board."
        return self._solved_board

    
if __name__ == "__main__":
    board = Sudoku()
    board.print_board()
    board.solve_board()
    print("\n\n")
    board.print_board()