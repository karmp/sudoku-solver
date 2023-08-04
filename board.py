class SudokuBoard:
    def __init__(self):
        self.board = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                      [6, 7, 2, 1, 9, 5, 3, 4, 8],
                      [1, 9, 8, 3, 4, 2, 5, 6, 7],
                      [8, 5, 9, 7, 6, 1, 4, 2, 3],
                      [4, 2, 6, 8, 5, 3, 7, 9, 1],
                      [7, 1, 3, 9, 2, 4, 8, 5, 6],
                      [9, 6, 1, 5, 3, 7, 2, 8, 4],
                      [2, 8, 7, 4, 1, 9, 6, 3, 5],
                      [3, 4, 5, 2, 8, 6, 1, 7, 9]
                      ]
    
    def print_board(self) -> None:
        """Prints out Sudoku Board."""
        for i in range(len(self.board)):
            if i % 3 == 0:
                print(f"{'-' * 21}")
            
            for j in range(len(self.board[0])):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")
        print(f"{'-' * 21}")

    def find_empty_cell(self) -> tuple:
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return (i, j) # Row, col of empty cell
        
        return (-1, -1) #When no empty cells left
    
    def check_valid_placement(self, ):
        pass

    def solve_board(self):
        pass



if __name__ == "__main__":
    board = SudokuBoard()
    board.print_board()