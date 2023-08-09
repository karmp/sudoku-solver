"""
This module contains the functions needed to process and extract a Sudoku
board from an image.
"""

import cv2, torch
import numpy as np
from pathlib import Path
from .mnist_cnn import model, transform
from typing import List


def extract_board_image(img_path: str) -> np.ndarray:
    """Extracts a Sudoku board from the image pass as a path.
    
    Args:
        img_path: path to image.
    
    Returns:
        Processed image as an numpy array.
    """
    img = cv2.imread(img_path)
    gray_scaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    assert gray_scaled is not None

    # Helps remove noise 
    blurred = cv2.GaussianBlur(gray_scaled, (9, 9), 0)

    # Converts img to only have black and white pixels using threshold value 255
    # Inverted to make grid findable when getting contours
    black_and_white = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find largest contour to locate Sudoku board
    contours, _ = cv2.findContours(black_and_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    sudoku_board = None

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx_polynomial = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        if len(approx_polynomial) == 4: # Found board
            sudoku_board = contour
            break
    
    if sudoku_board is None:
        raise Exception("Could not find Sudoku Board in image.") 

    # Represent contour as a simpliefied shape with 4 points
    contour_shape = cv2.convexHull(sudoku_board)
    perimeter = 0.02 * cv2.arcLength(contour_shape, True)
    simplified_shape = cv2.approxPolyDP(contour_shape, perimeter, True)
    _, _, width, height = cv2.boundingRect(simplified_shape)

    # Transform the Sudoku board part of the img to face it directly
    dst_points = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)
    transform_matrix = cv2.getPerspectiveTransform(simplified_shape.astype(np.float32), dst_points)
    direct_view = cv2.warpPerspective(black_and_white, transform_matrix, (width, height))
    
    # Fix orientation of final image
    direct_view = cv2.transpose(direct_view)
    direct_view = cv2.flip(direct_view, flipCode=1)

    # Uncomment to visualize before and after imgs
    # NOTE: The execution of the program will be stopped until the shown images are closed
    # cv2.drawContours(img, [sudoku_board], -1 , 255, 2)
    # cv2.imshow('Before', img)
    # cv2.imshow('After', direct_view)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return direct_view

def predict_number(cell: np.array, model: torch.nn.Sequential, device: str) -> int:
    """Predicts a number from an image using a trained CNN model.
    
    Args:
        cell: current cell on Sudoku image.
        model: trained CNN model.
        device: device name that torch will use.
    
    Returns:
        A number representing the prediction made by the model.
    """
    cell = cv2.bitwise_not(cv2.resize(cell, (28, 28)))
    cell = (255 - np.expand_dims(np.array(cell), -1)) / 255
    with torch.no_grad():
        pred = model(torch.unsqueeze(transform(cell), axis=0).float().to(device))
        pred = torch.argmax(pred, dim=1).item()
    # print(pred, end=" ")
    # cv2.imshow('Cell', cell)
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()
    return pred

def get_digits(sudoku_img: np.array, model: torch.nn.Sequential, 
               device: str) -> List[List[int]]:
    """Extracts the numbers on a Sudoku board image.

    Args:
        sudoku_img: numpy array representing the image.
        model: trained CNN model.
        deivce: device name that torch will use.
    
    Returns:
        A nested list representing a Sudoku board.
    """
    board = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):
            cur_cell = sudoku_img[i * 50: (i + 1) * 50, j * 50: (j + 1) * 50]
            if cur_cell.sum() > 120000: # Ignore empty cells
                board[i][j] = predict_number(cur_cell, model, device)
    return board

def get_sudoku(img_path: str) -> List[List[int]]:
    """Gets Sudoku board from an image. Returns a nested list of integers.
    
    Args:
        img_path: path to image.
    
    Returns:
        Nested list of integers representing a Sudoku Board.
    """
    img_path = str(Path(img_path))
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")
        # print("No Cuda Available")
    
    mnist_model = model.to(device)
    mnist_model.load_state_dict(torch.load(Path("img_processing", "trained_mnist_cnn.pth")))
    mnist_model.eval()
    sudoku = extract_board_image(img_path)
    sudoku = cv2.resize(sudoku, (450, 450))
    return get_digits(sudoku, mnist_model, device)

if __name__ == "__main__":
    TEST_PATH = str(Path("rsrc", "test.png"))
    get_sudoku(TEST_PATH)
