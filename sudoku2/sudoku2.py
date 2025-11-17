# sudoku.py

# new version of sudoku class started in Q4/2025
# basic functionality for representing and manipulating Sudoku puzzles
# currently supports:
# - uses numpy for grid representation
# - prints grid in readable format
# - checks validity of current grid
# - provides access to rows, columns, and blocks
# - allows setting values in the grid
# - allows setting the entire grid
# - provides candidate values for empty cells
# - finds and solves single candidates
# - checks if the Sudoku is completely solved
# - basic framework for further solving techniques

# Werner Schoegler, 11-Nov-2025

# pylint: disable=invalid-name

import numpy as np
from io import StringIO  
from collections import Counter

class Sudoku:
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.debugLevel = 0  # global debug level for printing debug information

    def count_empty_cells(self) -> int:
        return np.sum(self.grid == 0)

    def isValid(self) -> bool:
        """Check if the current Sudoku grid is valid."""
        for i in range(9):
            if not self._is_valid_unit(self.grid[i, :]):  # Check rows
                return False
            if not self._is_valid_unit(self.grid[:, i]):  # Check columns
                return False
            if not self._is_valid_unit(self.grid[3*(i//3):3*(i//3)+3, 3*(i%3):3*(i%3)+3].flatten()):  # Check boxes
                return False
        return True
    def _is_valid_unit(self, unit: np.ndarray) -> bool:
        """Check if a row, column, or box contains no duplicates (ignoring zeros)."""
        unit = unit[unit != 0]  # Remove zeros
        return len(unit) == len(set(unit))
    
    def _getRowColFromBlockNumber(self, blockNumber: int) -> tuple[int, int]:
        """Get the starting row and column for a given block number."""
        block_row = (blockNumber // 3) * 3
        block_col = (blockNumber % 3) * 3
        return block_row, block_col
    
    def getBlockNumber(self, row: int, col: int) -> int:
        """Get the block number (0-8) for a given cell."""
        return (row // 3) * 3 + (col // 3)
    
    def getBlock(self, row: int, col: int) -> np.ndarray:
        """Get the 3x3 block for a given cell."""
        block_row = (row // 3) * 3
        block_col = (col // 3) * 3
        return self.grid[block_row:block_row+3, block_col:block_col+3].flatten()
    
    def getRow(self, row: int) -> np.ndarray:
        """Get a specific row."""
        return self.grid[row, :]
    
    def getCol(self, col: int) -> np.ndarray:
        """Get a specific column."""
        return self.grid[:, col]
    
    def getCandidates(self, row: int, col: int) -> list[int]:
        """Get possible candidate values for a specific cell."""
        if self.grid[row, col] != 0:
            return []  # Cell is already filled
        # a set has the property of unique values only, so we can use it to find used values
        used_values = set(self.getRow(row)) | set(self.getCol(col)) | set(self.getBlock(row, col))
        return [val for val in range(1, 10) if val not in used_values]
    
    def getCandidatesInRow(self, row: int) -> list[int]:
        """Get candidates for all empty cells in a specific row."""
        candidates = np.array([], dtype=int)
        for col in range(9):
            if self.grid[row, col] == 0:
                candidates = np.append(candidates, self.getCandidates(row, col))
        return np.sort(candidates)
    
    def findFirstCandidateInRow(self, row: int, candidate: int) -> tuple[int, int, int] | None:
        """Find the first occurrence of a specific candidate in a row."""
        for col in range(9):
            if self.grid[row, col] == 0:
                candidates = self.getCandidates(row, col)
                if candidate in candidates:
                    return (row, col, int(candidate))
        return None

    def getCandidatesInCol(self, col: int) -> list[int]:
        """Get candidates for all empty cells in a specific column."""
        candidates = np.array([], dtype=int)
        for row in range(9):
            if self.grid[row, col] == 0:
                candidates = np.append(candidates, self.getCandidates(row, col))
        return np.sort(candidates)
    
    def findFirstCandidateInCol(self, col: int, candidate: int)  -> tuple[int, int, int] | None:
        """Find the first occurrence of a specific candidate in a column."""
        for row in range(9):
            if self.grid[row, col] == 0:
                candidates = self.getCandidates(row, col)
                if candidate in candidates:
                    return (row, col, int(candidate))
        return None
    
    def getCandidatesInBlock(self, blockNumber: int)  -> list[int]:
        """Get candidates for all empty cells in a specific block."""
        candidates = np.array([], dtype=int)
        block_row = (blockNumber // 3) * 3
        block_col = (blockNumber % 3) * 3
        for i in range(3):
            for j in range(3):
                row = block_row + i
                col = block_col + j
                if self.grid[row, col] == 0:
                    candidates = np.append(candidates, self.getCandidates(row, col))
        return np.sort(candidates)
    
    def findFirstCandidateInBlock(self, blockNumber: int, candidate: int) -> tuple[int, int, int] | None:
        """Find the first occurrence of a specific candidate in a block."""
        block_row = (blockNumber // 3) * 3
        block_col = (blockNumber % 3) * 3
        for i in range(3):
            for j in range(3):
                row = block_row + i
                col = block_col + j
                if self.grid[row, col] == 0:
                    candidates = self.getCandidates(row, col)
                    if candidate in candidates:
                        return (row, col, int(candidate))
        return None
    
    def findHiddenSingle(self, candidates: list[int]) -> int | None:
        """Find a hidden single in a list of candidates."""
        counts = Counter(candidates)
        for candidate, count in counts.items():
            if count == 1:
                return candidate
        return None

    def setValue(self, row: int, col: int, value: int, description: str = "") -> None:
        """Set a value in the Sudoku grid."""
        if self.debugLevel >= 1:
            print(f"    {description} set at position: {row, col}: {value}")
        self.grid[row, col] = value

    def setGrid(self, grid: np.ndarray) -> None:
        """Set the entire Sudoku grid."""
        self.grid = grid

    def __str__(self) -> str:
        """Print the Sudoku grid in a nicely readable format."""
        buf = StringIO()
        for row in range(9):
            if row % 3 == 0 and row != 0:
                buf.write("-" * 21 + "\n")
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    buf.write("| ")
                buf.write(str(self.grid[row, col]) if self.grid[row, col] != 0 else ".")
                buf.write(" ")
            buf.write("\n")
        return buf.getvalue()
    
    def printCandidates(self) -> None:
        """Print candidates for all empty cells."""
        for row in range(9):
            for col in range(9):
                if self.grid[row, col] == 0:
                    candidates = self.getCandidates(row, col)
                    print(f"Cell ({row}, {col}): Candidates = {candidates}")    

    def findSingleCandidates(self) -> list[tuple[int, int, int]]:
        """Find all cells with a single candidate and return their positions and values."""
        singles = []
        for row in range(9):
            for col in range(9):
                if self.grid[row, col] == 0:
                    candidates = self.getCandidates(row, col)
                    if len(candidates) == 1:
                        singles.append((row, col, candidates[0]))
        return singles
    
    def solver1(self, enableHiddenSingles: bool = True) -> bool:
        # Simple solver that repeatedly applies hidden singles and singles until no more can be found
        if self.debugLevel >= 1:
            print("="*10 + f" solver1 started")
        foundHiddenSingles = False
        foundSingles = True
        i = 0
        while foundHiddenSingles or foundSingles:
            i += 1
            if self.debugLevel >= 1:
                print("="*10 + f" solver1 iteration {i}")
            foundSingles = self.solveSingles()
            # search for hidden singles only if no singles were found
            if not foundSingles and enableHiddenSingles:
                foundHiddenSingles = self.solveHiddenSingles()
            else:
                foundHiddenSingles = False
        if self.isSolved():
            if self.debugLevel >= 1:
                print("="*10 + f" solver1 finished: Sudoku is solved")
            return True
        else:
            if self.debugLevel >= 1:
                print("="*10 + f" solver1 finished: Sudoku is NOT solved")
            return False
            
    def solveSingles(self) -> bool:
        """Fill in all cells that have a single candidate."""
        # run a loop until no more singles are found
        singles = self.findSingleCandidates()
        numOfSingles = len(singles) 
        if numOfSingles == 0:
            return False
        while numOfSingles > 0:
            for row, col, value in singles:
                self.setValue(row, col, value, description="Single candidate")
            singles = self.findSingleCandidates()
            numOfSingles = len(singles)
        return True

    def solveHiddenSingles(self) -> bool:
        """Fill in all cells that have hidden singles in rows, columns, and blocks."""
        returnValue = False
        # Check all rows
        for i in range(9):
            candidatesinRow = self.getCandidatesInRow(i)
            findHiddenSingle = self.findHiddenSingle(candidatesinRow)
            if findHiddenSingle is not None:
                result = self.findFirstCandidateInRow(i, findHiddenSingle)
                if result is not None:
                    row, col, value = result
                    self.setValue(row, col, value, description=f"Hidden single in row {i}")
                    returnValue = True
                # Consider: should you recalculate after each placement?
                # Or continue and get all hidden singles in one pass?
        # Check all columns
        for i in range(9):
            candidatesinCol = self.getCandidatesInCol(i)
            findHiddenSingle = self.findHiddenSingle(candidatesinCol)
            if findHiddenSingle is not None:
                result = self.findFirstCandidateInCol(i, findHiddenSingle)
                if result is not None:                
                    row, col, value = result
                    self.setValue(row, col, value, description="Hidden single in col")
                    returnValue = True
        # Check all blocks
        for i in range(9):
            candidatesinBlock = self.getCandidatesInBlock(i)
            findHiddenSingle = self.findHiddenSingle(candidatesinBlock)
            if findHiddenSingle is not None:
                result = self.findFirstCandidateInBlock(i, findHiddenSingle)
                if result is not None:                
                    row, col, value = result
                    self.setValue(row, col, value, description="Hidden single in block")
                    returnValue = True
        return returnValue

    def isSolved(self) -> bool:
        """Check if the Sudoku is completely solved."""
        # test that there are no zeros and that it is valid
        return np.all(self.grid != 0) and self.isValid()
    
    # Basic backtracking solver (not optimized)
    def solveBacktrack(self) -> bool:
        """Solve using recursive backtracking algorithm."""
        # Find empty cell
        for row in range(9):
            for col in range(9):
                if self.grid[row, col] == 0:
                    candidates = self.getCandidates(row, col)
                    for value in candidates:
                        self.grid[row, col] = value
                        if self.solveBacktrack():  # Recursive call
                            return True
                        self.grid[row, col] = 0  # Backtrack
                    return False
        return True  # No empty cells, solved!
    
    # Optimized backtracking that always fills the cell with the fewest candidates first
    def solveBacktrackOptimized(self) -> bool:
        """Optimized backtracking: always fill cell with fewest candidates first."""
        # Find cell with minimum candidates
        min_candidates = 10
        best_cell = None
        best_candidates = []
        
        for row in range(9):
            for col in range(9):
                if self.grid[row, col] == 0:
                    candidates = self.getCandidates(row, col)
                    if len(candidates) == 0:
                        return False  # Dead end
                    if len(candidates) < min_candidates:
                        min_candidates = len(candidates)
                        best_cell = (row, col)
                        best_candidates = candidates
        
        if best_cell is None:
            return True  # Solved!
        
        row, col = best_cell
        for value in best_candidates:
            self.grid[row, col] = value
            if self.solveBacktrackOptimized():  # Still recursive but MUCH faster
                return True
            self.grid[row, col] = 0
        
        return False
