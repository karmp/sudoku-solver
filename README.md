# Sudoku Solver with GUI
A Python Sudoku solver that uses Backtracking Search to solve a Sudoku board.
A connvolutional neural network is used to process an image of a Sudoku board that 
the user inputs and displays it on the GUI.

# Installation
Check requirements.txt for external libraries that are required.
Install using pip.

# Usage
Run main.py to start the GUI of the Sudoku solver. It will create a default Sudoku board and display it in the GUI.
To manually solve the Sudoku board:
  1. Click on an empty cell. After successfully selecting a cell it will be highlighted blue.
  2. Input a number
  3. If the number is part of the solution, the number will be successfully inserted in the board and will be displayed
  4. If the number is not a part of the solution, a red X will be shown in the bottom left corner of the window.

To automatically solve the board click on the Solve Board button , this will automatically solve the current state of the
Sudoku board and the display will update.

To import an image of a Sudoku board to solve it, click on the Upload Image button in the bottom right and upload a .png 
or .jpg/jpeg image of a Sudoku board. The image will be processed and the neural network will be used to extract the numbers
from the Sudoku board. The resulting board will be displayed on the GUI.


<img width="338" alt="image" src="https://github.com/karmp/sudoku-solver/assets/62309862/a806bbb0-9c96-4d7f-ad0f-d90ffdc4860d">

# Important Note with Uploading Image
It is not recommended to manually solve the Sudoku board after uploading an image as the solution to the uploaded board
will not be generate until the user fixes any issues with the numbers on the board and presses the Solve Board button.
This means that the solution to the uploaded board in incorrect until the errors on the game board are fixed and the Solve
Board button is pressed.

# Fixing incorrect numbers from image import
If a number in a given cell is incorrect after uploading the Sudoku image, you can fix this by turning on Edit Mode
with the button in the bottom left. Note this is automatically turned on after uploading an image.
  1. Click on the cell you want to fix
  2. Press the Delete key. This will remove that number from the board.
  3. Input the correct number

To remove an already placed number on the board, Edit Mode must be turned on after which you can delete the number
using the Delete key.

