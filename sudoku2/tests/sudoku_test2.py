# sudoku_test2.py
# Tests for the Sudoku class
# Werner Schoegler, 16-Nov-2025

# pylint: disable=import-error
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-f-string
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
# pylint: disable=too-many-nested-blocks
# pylint: disable=unused-variable
# pylint: disable=unused-import
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=consider-iterating-dictionary
# pylint: disable=consider-using-dict-items

import sys
import os
import time
# Adjust the path to import sudoku2 module
home_dir = os.path.expanduser("~")
python_dir = home_dir + "/devel_wsc_py/"
print(f"Adding {python_dir}/sudoku2 to sys.path for imports")
if python_dir not in sys.path:
    sys.path.append(python_dir + "/sudoku2")  # to allow import from sibling directory

import numpy as np
from tqdm import tqdm

from sudoku2 import Sudoku
from tester import Tester

from util.string2array import string2array
from data.test_data import trialSudokus1
from data.test_data import trialSudokus2
from data.test_data import easyTrialSudokus
from data.test_data import hardTrialSudokus
from data.test_data import evelTrialSudokus

# ============================== User Settings ==============================
# set to True to process all levels
PROCESS_ALL_LEVELS = True
# Set debug level to see detailed solving steps
DEBUG_LEVEL = 0

# select the sudokus to test
# testSudokus = trialSudokus1
# testSudokus = hardTrialSudokus
testSudokus = trialSudokus1 | trialSudokus2 | easyTrialSudokus | evelTrialSudokus
# ============================ End User Settings ============================

# Some color definitions for terminal with ANSI support
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'




if __name__ == '__main__':
    # Initialize tester (simple test framework)
    tester = Tester()

    # Sample Sudoku grid for testing
    sudoku = Sudoku(np.array([
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]))
    sudoku.debugLevel = DEBUG_LEVEL
solveStatus = {}
solveAlgorithm = {}
solveTime = {}
emptyCells = {}
backtrack_counter = 0
backtrack_failure_counter = 0
solver1_counter = 0
solver1hs_counter = 0
for level, grid_str in tqdm(testSudokus.items(), desc="Solving Sudokus"):
    checkLevel = level.startswith("evil")
    if checkLevel or PROCESS_ALL_LEVELS:
        grid = string2array(grid_str)
        sudoku.setGrid(grid)
        emptyCells[level] = sudoku.count_empty_cells()
        print("="*40 + f" {level} " + "="*40)
        if sudoku.debugLevel > 0:
            print(sudoku)
        start_time = time.time()
        solver1_success = sudoku.solver1(enableHiddenSingles=False)
        end_time = time.time()
        elapsed_time = end_time - start_time
        solveTime[level] = f"{elapsed_time:.4f}"
        if solver1_success:
            tester.test_checker(sudoku.isSolved() is True, f"Sudoku is solved for {level} puzzle by solver1 without hidden singles")
            solveStatus[level] = "solved"
            solveAlgorithm[level] = "solver1"
            solver1_counter += 1
        else:
            sudoku.setGrid(grid)
            start_time = time.time()
            solver1hs_success = sudoku.solver1(enableHiddenSingles=True)
            end_time = time.time()
            elapsed_time = end_time - start_time
            solveTime[level] = f"{elapsed_time:.4f}"
            if solver1hs_success:
                tester.test_checker(sudoku.isSolved() is True, f"Sudoku is solved for {level} puzzle by solver1 with hidden singles")
                solveStatus[level] = "solved"
                solveAlgorithm[level] = "solver1 HS"
                solver1hs_counter += 1
            else:
                start_time = time.time()
                # backtrack_success = sudoku.solveBacktrack()
                backtrack_success = sudoku.solveBacktrackOptimized()
                end_time = time.time()
                backtrack_time = end_time - start_time
                total_time = elapsed_time + backtrack_time
                solveTime[level] = f"{total_time:.4f}"
                if backtrack_success:
                    tester.test_checker(sudoku.isSolved() is True, f"Sudoku is solved for {level} puzzle by backtracking")
                    solveStatus[level] = "solved"
                    solveAlgorithm[level] = "backtracking"
                    backtrack_counter += 1
                else:
                    tester.test_checker(False, f"Sudoku could not be solved for {level} puzzle")
                    solveStatus[level] = "unsolved"
                    solveAlgorithm[level] = "Backtracking failed"
                    backtrack_failure_counter += 1
        if sudoku.debugLevel > 0:
            print(sudoku)

# Print summary table for solving status and time
print("="*80 + "\nSummary of solving status:")
print(f"Total puzzles processed: {len(solveStatus)}")
print(f"Total solved by solver1 without hidden singles: {solver1_counter}")
print(f"Total solved by solver1 with hidden singles: {solver1hs_counter}")
print(f"Total solved by backtracking: {backtrack_counter}")
if backtrack_failure_counter > 0:
    print(f"Total backtracking failures: {backtrack_failure_counter}")

str1 = "Level"
print(f"{str1:12}", end=" | ")
str1 = "Empty"
print(f"{str1:6}", end=" | ")
str1 = "Status"
print(f"{str1:12}", end=" | ")
str1 = "Algorithm"
print(f"{str1:24}", end=" | ")
str1 = "Time [seconds   ]"
print(f"{str1:24}")
print("-"*80)
for item in solveStatus.items():
    if solveStatus[item[0]] == "solved":
        color = GREEN
        print(f"{GREEN}", end="")
    else:
        color = RED
        print(f"{RED}", end="")
    print(f"{item[0]:12}", end=" | ")
    print(f"{emptyCells[item[0]]:6}", end=" | ")
    print(f"{solveStatus[item[0]]:12}", end=" | ")
    print(f"{solveAlgorithm[item[0]]:24}", end=" | ")
    print(f"{solveTime[item[0]]:24}")
    print(f"{RESET}", end="")
print("-"*80)

# average time calculation
total_time = sum(float(t) for t in solveTime.values())
avg_time = total_time / len(solveTime)
print(f"\nTotal time: {total_time:.4f}s | Average: {avg_time:.4f}s")
# ============================== End of File ===============================
