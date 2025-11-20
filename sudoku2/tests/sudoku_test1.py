
import sys
import os
import time
import numpy as np

# Adjust the path to import sudoku2 module
home_dir = os.path.expanduser("~")
python_dir = home_dir + "/devel_wsc_py/"
print(f"Adding {python_dir}/sudoku2 to sys.path for imports")
if python_dir not in sys.path:
    sys.path.append(python_dir + "/sudoku2")  # to allow import from sibling directory

from sudoku2 import Sudoku
from util.string2array import string2array

# 81 characters: digits 1-9 for values, 0 or '.' for empty cells
puzzle_string = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
grid = string2array(puzzle_string)

sudoku = Sudoku(grid)
print(sudoku)
sudoku.solver1()
print(sudoku)