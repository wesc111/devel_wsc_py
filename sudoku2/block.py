

# list of tuples representing the (row, column) indices of cells in a specified 3x3 block of a Sudoku grid.
from typing import List, Tuple
from unittest import case

import numpy as np

# the normal definition of blocks in a Sudoku grid
block_norm_index_0: List[Tuple[int, int]] = [
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2),
    (2, 0), (2, 1), (2, 2)      
]
block_norm_index_1: List[Tuple[int, int]] = [
    (0, 3), (0, 4), (0, 5),
    (1, 3), (1, 4), (1, 5),
    (2, 3), (2, 4), (2, 5)      
]
block_norm_index_2: List[Tuple[int, int]] = [
    (0, 6), (0, 7), (0, 8),
    (1, 6), (1, 7), (1, 8),
    (2, 6), (2, 7), (2, 8)      
]
block_norm_index_3: List[Tuple[int, int]] = [
    (3, 0), (3, 1), (3, 2),
    (4, 0), (4, 1), (4, 2),
    (5, 0), (5, 1), (5, 2)      
]
block_norm_index_4: List[Tuple[int, int]] = [
    (3, 3), (3, 4), (3, 5),
    (4, 3), (4, 4), (4, 5),
    (5, 3), (5, 4), (5, 5)      
]
block_norm_index_5: List[Tuple[int, int]] = [
    (3, 6), (3, 7), (3, 8),
    (4, 6), (4, 7), (4, 8),
    (5, 6), (5, 7), (5, 8)      
]
block_norm_index_6: List[Tuple[int, int]] = [
    (6, 0), (6, 1), (6, 2),
    (7, 0), (7, 1), (7, 2),
    (8, 0), (8, 1), (8, 2)      
]
block_norm_index_7: List[Tuple[int, int]] = [
    (6, 3), (6, 4), (6, 5),
    (7, 3), (7, 4), (7, 5),
    (8, 3), (8, 4), (8, 5)      
]
block_norm_index_8: List[Tuple[int, int]] = [
    (6, 6), (6, 7), (6, 8),
    (7, 6), (7, 7), (7, 8),
    (8, 6), (8, 7), (8, 8)      
]

# an alternative 1 definition of blocks for a jiggsaw Sudoku grid
block_alt1_index_0: List[Tuple[int, int]] = [
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2),
    (2, 0), (2, 1), 
    (3, 0)      
]
block_alt1_index_1: List[Tuple[int, int]] = [
                   (0, 3), 
                   (1, 3),
           (2, 2), (2, 3),
    (3,1), (3, 2), (3, 3), (3,4),
    (4,1)
]
block_alt1_index_2: List[Tuple[int, int]] = [
    (0, 4), (0, 5), (0, 6), (0,7),
    (1, 4), (1, 5), (1, 6),
    (2, 4), (2, 5)      
]
block_alt1_index_3: List[Tuple[int, int]] = [
                    (0, 8), 
            (1, 7), (1, 8),
    (2, 6), (2, 7), (2, 8),
            (3, 7), (3, 8),
                    (4, 8)     
]
block_alt1_index_4: List[Tuple[int, int]] = [
    (4, 0),
    (5, 0), (5, 1),
    (6, 0), (6, 1), (6, 2),
    (7, 0), (7, 1),
    (8, 0)      
]
block_alt1_index_5: List[Tuple[int, int]] = [
    (3, 5), (3, 6),
    (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
    (5, 2), (5, 3)      
]
block_alt1_index_6: List[Tuple[int, int]] = [
    (6, 3), (6, 4),
    (7, 2), (7, 3), (7, 4),
    (8, 1), (8, 2), (8, 3), (8, 4)      
]
block_alt1_index_7: List[Tuple[int, int]] = [
                            (4, 7),
    (5, 4), (5, 5), (5, 6), (5, 7),
            (6, 5), (6, 6),
            (7, 5),
            (8, 5)   
]
block_alt1_index_8: List[Tuple[int, int]] = [
                    (5, 8),
            (6, 7), (6, 8),
    (7, 6), (7, 7), (7, 8),
    (8, 6), (8, 7), (8, 8)      
]

def get_block_indices(block_number, block_index_selection: str) -> List[Tuple[int, int]]:   
    '''Returns the list of (row, column) indices for the specified block number and block index selection.'''
    blocks = eval(f"{block_index_selection}{block_number}")
    return blocks

def print_block_indices(block_index_selection) -> None:
    '''Prints a visual representation of the Sudoku blocks based on the provided block index selection.'''
    RED = "\033[91m"
    BLACK = "\033[90m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m" 
    PURPLE ="\033[94m"
    CYAN = "\033[96m"
    LIGHT_GRAY = "\033[97m"
    WHITE = "\033[98m"
    RESET_COLOR = "\033[0m"
    cell = np.zeros((9,9), dtype=int)

    for row in range(9):
        for col in range(9):
            found_in_some_block = False
            for i in range(9):
                if (row, col) in eval(f"{block_index_selection}{i}"):
                    cell[row, col] = i


    for row in range(9):
        for col in range(9):
            if cell[row, col]==0:
                print(RED + str(cell[row, col]), end=' ')
            elif cell[row, col]==1:
                print(GREEN + str(cell[row, col]), end=' ')
            elif cell[row, col]==2:
                print(YELLOW + str(cell[row, col]), end=' ')
            elif cell[row, col]==3:
                print(PURPLE + str(cell[row, col]), end=' ')
            elif cell[row, col]==4:
                print(CYAN + str(cell[row, col]), end=' ')
            elif cell[row, col]==5:
                print(LIGHT_GRAY + str(cell[row, col]), end=' ')
            elif cell[row, col]==6:
                print(RED + str(cell[row, col]), end=' ')
            elif cell[row, col]==7:
                print(GREEN + str(cell[row, col]), end=' ')
            elif cell[row, col]==8:
                print(YELLOW + str(cell[row, col]), end=' ')
            else:
                print(RESET_COLOR + str(cell[row, col]), end=' ')
        print(RESET_COLOR + " ")




if __name__ == "__main__":
    print(" ")
    print("Sudoku normal block definition:")
    print_block_indices("block_norm_index_")
    print(" ")
    print("Sudoku block alternative 1 jiggsaw block definition:")
    print_block_indices("block_alt1_index_")
