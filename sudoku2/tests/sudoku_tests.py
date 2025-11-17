# sudoku_tests.py
# Tests for the Sudoku class
# Werner Schoegler, 11-Nov-2025

import sys, os
import numpy as np

# Adjust the path to import sudoku2 module
home_dir = os.path.expanduser("~")
python_dir = home_dir + "/OneDrive/devel_wsc_private/python"
if python_dir not in sys.path:
    sys.path.append(python_dir + "/sudoku2")  # to allow import from sibling directory

from sudoku2 import Sudoku
from tester import Tester
from util.string2array import string2array

trialSudokus = {
    "easy 1": "003020600900305001001806400008102900700000008006708200002609500800203009005010300",
    "easy 2": "530070000600195000098000060800060003400803001700020006060000280000419005000080079",
    "medium": "005300000800000020070010500400005300001070006003200080060500009004000030000009700",
    "hard": "000000907000420180000705026100904000050000040000507009920108000034059000507000000",
    "evil": "300200000000107000706030500070009080900020004010800050009040301000702000000008006"
}

if __name__ == '__main__':

    # Initialize tester (simple test framework)
    tester = Tester()

    # Sample Sudoku grid for testing
    sudoku = Sudoku(np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]))

    tester.setTestGroup("Sudoku Class isValid() Tests")
    tester.test_checker(sudoku.isValid()==True, "Sudoku validity test")


    sudoku.setValue(0, 2, 4)  # Set a value that keeps the Sudoku valid
    tester.test_checker(sudoku.isValid()==True, "Sudoku validity after setting (0,2) to 4")

    sudoku.setValue(0, 1, 5)  #     
    tester.test_checker(sudoku.isValid()==False, "Sudoku invalidity after setting (0,1) to 5")

    sudoku.setValue(0, 1, 0)  # Set a value that makes the Sudoku valid again
    tester.test_checker(sudoku.isValid()==True, "Sudoku validity after setting (0,1) to 0")

    sudoku.setValue(2, 3, 9)  # Set a value that makes the Sudoku valid again
    tester.test_checker(sudoku.isValid()==False, "Sudoku invalidity after setting (2,3) to 9")

    sudoku.setValue(2, 3, 0)  # Set a value that makes the Sudoku valid again
    tester.test_checker(sudoku.isValid()==True, "Sudoku validity after setting (2,3) to 0")

    sudoku.setValue(6, 8, 3)  # Set a value that makes the Sudoku valid again
    tester.test_checker(sudoku.isValid()==False, "Sudoku invalidity after setting (6,8) to 3")

    sudoku.setValue(6, 8, 0)  # Set a value that makes the Sudoku valid again
    tester.test_checker(sudoku.isValid()==True, "Sudoku validity after setting (6,8) to 0")

    tester.setTestGroup("Sudoku Class getBlockNumber() and getBlock() Tests")
    for row in range(9):
        for col in range(9):
            blockNumber = sudoku.getBlockNumber(row, col)
            expectedBlockNumber = (row // 3) * 3 + (col // 3)
            tester.test_checker(blockNumber == expectedBlockNumber, 
                                f"Get block number for cell ({row},{col}) == {expectedBlockNumber}")

    sudoku.setGrid(np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]))

    for block_row in range(3):
        for block_col in range(3):
            for i in range(3):
                for j in range(3):
                    row = block_row * 3 + i
                    col = block_col * 3 + j
                    block = sudoku.getBlock(row, col)
                    expected_block = sudoku.grid[block_row*3:(block_row+1)*3, block_col*3:(block_col+1)*3].flatten()
                    tester.test_checker(np.array_equal(block, expected_block), f"Get block for cell ({row},{col}) == {expected_block}")

    tester.setTestGroup("Sudoku Class solveSingles() and isSolved() Tests")

    for level, grid_str in trialSudokus.items():
        if level.startswith("easy"):
            grid = string2array(grid_str)
            sudoku.setGrid(grid)
            sudoku.solveSingles()
            tester.test_checker(sudoku.isSolved()==True, f"Sudoku is solved after singles for {level} puzzle")
    # now some more complex tests with string representation of grids

    for level, grid_str in trialSudokus.items():
        if level.startswith("medium") or level.startswith("easy 1") or level.startswith("easy 2"):
            grid = string2array(grid_str)
            sudoku.setGrid(grid)
            sudoku.solveHiddenSingles()
            sudoku.solver1()
            tester.test_checker(sudoku.isSolved()==False, f"Sudoku is not yet solved after singles for {level} puzzle")
            print(sudoku)
 

    print("\n" + "="*50)
    print(tester)
