import cv2
import numpy as np


def extract_board_image(img_path: str) -> np.ndarray:
    """Extracts a Sudoku board from the image pass as a path.
    
    Args:
        img_path: String to an image path
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
    # NOTE: The execution of the program will be stopped until the shown images are exited
    cv2.drawContours(img, [sudoku_board], -1 , 255, 2)
    cv2.imshow('Before', img)
    cv2.imshow('After', direct_view)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return direct_view


if __name__ == "__main__":
    TEST_PATH1 = "K:\\Coding\\Python\\sudoku-solver\\rsrc\\test.png"
    TEST_PATH2 = "K:\\Coding\\Python\\sudoku-solver\\rsrc\\test2.png"
    extract_board_image(TEST_PATH2)
