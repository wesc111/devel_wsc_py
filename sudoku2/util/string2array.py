# string2array.py
# Werner Schoegler, 17-Nov-2025

import numpy as np

def string2array(s: str) -> np.ndarray:
    """Convert a string representation of a Sudoku grid to a 2D numpy array."""
    s1 = s.strip()
    if len(s1) != 81:
        raise ValueError("Input string must have exactly 81 characters representing the Sudoku grid.")
    grid = np.zeros((9, 9), dtype=int)
    r = 0
    c = 0
    for char in s1:
        if char.isdigit():
            grid[r, c] = int(char)
        else:
            grid[r, c] = 0
        c += 1
        if c == 9:
            c = 0
            r += 1
    return grid