# Sudoku Solver

A comprehensive Python-based Sudoku solver implementing multiple solving techniques, from logical deduction methods to advanced backtracking algorithms.

## 🎯 Features

- **Multiple Solving Algorithms:**
  - **Naked Singles** - Cells with only one possible candidate value
  - **Hidden Singles** - Values that appear only once in a row, column, or block
  - **Backtracking** - Recursive brute-force with validation
  - **Optimized Backtracking** - MRV (Minimum Remaining Values) heuristic for dramatic performance gains
  
- **Grid Management:**
  - Comprehensive validation of Sudoku rules
  - Clean grid display with visual block separators
  - Access to rows, columns, and 3x3 blocks
  - Candidate value calculation for empty cells

- **Testing & Analysis:**
  - Custom testing framework with pass/fail tracking
  - 100+ real-world test puzzles from various sources
  - Performance benchmarking and timing statistics
  - Difficulty-based puzzle collections (easy, medium, hard, evil)

- **Debug Support:**
  - Configurable debug levels for solving visualization
  - Step-by-step solving output
  - Candidate tracking and display

## 📋 Requirements

- Python 3.10 or higher
- NumPy

```bash
pip install numpy
```

## 🚀 Quick Start

### Basic Usage

```python
from sudoku2 import Sudoku
import numpy as np

# Create a Sudoku puzzle (0 represents empty cells)
grid = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])

sudoku = Sudoku(grid)
print("Original puzzle:")
print(sudoku)

# Solve using logical techniques first
if sudoku.solver1(enableHiddenSingles=True):
    print("Solved with logical techniques!")
else:
    # Fall back to backtracking if needed
    print("Logical solving incomplete, using backtracking...")
    sudoku.solveBacktrackOptimized()

if sudoku.isSolved():
    print("\n✓ Solved puzzle:")
    print(sudoku)
else:
    print("\n✗ Could not solve puzzle")
```

### Using String Input

```python
from util.string2array import string2array

# 81 characters: digits 1-9 for values, 0 or '.' for empty cells
puzzle_string = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
grid = string2array(puzzle_string)

sudoku = Sudoku(grid)
sudoku.solver1()
print(sudoku)
```

## 📖 API Reference

### Core Methods

#### Creating a Sudoku

```python
sudoku = Sudoku(grid: np.ndarray)
```
- **Parameters:** 9x9 NumPy array with integers 0-9 (0 = empty cell)

#### Solving Methods

```python
# Logical solving (naked + hidden singles)
success = sudoku.solver1(enableHiddenSingles: bool = True) -> bool

# Individual techniques
success = sudoku.solveSingles() -> bool         # Only naked singles
success = sudoku.solveHiddenSingles() -> bool   # Only hidden singles

# Backtracking methods
success = sudoku.solveBacktrack() -> bool                # Standard recursive backtracking
success = sudoku.solveBacktrackOptimized() -> bool       # With MRV heuristic (faster)
```

#### Validation and Status

```python
is_valid = sudoku.isValid() -> bool             # Check if current state is valid
is_solved = sudoku.isSolved() -> bool           # Check if completely solved
empty_count = sudoku.count_empty_cells() -> int # Count remaining empty cells
```

#### Grid Access

```python
row = sudoku.getRow(row: int) -> np.ndarray         # Get specific row
col = sudoku.getCol(col: int) -> np.ndarray         # Get specific column
block = sudoku.getBlock(row: int, col: int) -> np.ndarray  # Get 3x3 block
block_num = sudoku.getBlockNumber(row: int, col: int) -> int  # Get block number (0-8)
```

#### Candidate Methods

```python
candidates = sudoku.getCandidates(row: int, col: int) -> list[int]
row_candidates = sudoku.getCandidatesInRow(row: int) -> np.ndarray
col_candidates = sudoku.getCandidatesInCol(col: int) -> np.ndarray
block_candidates = sudoku.getCandidatesInBlock(blockNumber: int) -> np.ndarray
```

#### Grid Manipulation

```python
sudoku.setValue(row: int, col: int, value: int, description: str = "")
sudoku.setGrid(grid: np.ndarray)
```

#### Display and Debug

```python
print(sudoku)                    # Display grid with nice formatting
sudoku.printCandidates()         # Print all candidates for empty cells
sudoku.debugLevel = 1            # Enable debug output (0=off, 1=basic, 2=detailed)
```

## 📁 Project Structure

```
sudoku2/
├── README.md                   # This file
├── sudoku2.py                  # Main Sudoku class
├── candidate.py                # Candidate value management (legacy)
├── tester.py                   # Custom testing framework
├── data/                       # Test puzzle collections
│   ├── test_data.py           # Programmatic test data
│   ├── easy_50.txt            # 50 easy puzzles
│   ├── hardest.txt            # Hardest known puzzles
│   ├── top95.txt              # Top 95 difficult puzzles
│   └── ...
├── tests/                      # Test suites
│   ├── sudoku_test2.py        # Comprehensive test suite with statistics
│   ├── sudoku_tests.py        # Basic tests
│   └── candidate_tests.py     # Candidate class tests
├── util/                       # Utility functions
│   └── string2array.py        # Convert string puzzles to arrays
└── doc/                        # Additional documentation
    └── ALGORITHMS.md           # Detailed algorithm explanations
```

## 🧪 Running Tests

### Comprehensive Test Suite

```bash
cd tests
python sudoku_test2.py
```

This runs 100+ puzzles and provides:
- Pass/fail statistics
- Algorithm comparison (solver1 vs solver1+HS vs backtracking)
- Performance timing for each puzzle
- Summary table showing which algorithm solved each puzzle

### Basic Tests

```bash
python tests/sudoku_tests.py
```

## 🎯 Algorithm Details

> **📖 For detailed algorithm explanations, complexity analysis, and examples, see [ALGORITHMS.md](doc/ALGORITHMS.md)**

### Naked Singles
Identifies cells where only one candidate value is possible after eliminating values that appear in the same row, column, or 3x3 block.

**Time Complexity:** O(n²) where n=9

### Hidden Singles
Finds values that can only appear in one cell within a row, column, or block, even if that cell has multiple candidates initially.

**Time Complexity:** O(n³)

### Backtracking
Classic recursive depth-first search that tries each candidate value and backtracks on conflicts.

**Time Complexity:** O(9^m) where m is the number of empty cells (worst case)

### Optimized Backtracking (MRV Heuristic)
Always selects the cell with the **minimum remaining values** (fewest candidates) to fill next. This dramatically reduces the search space by making early mistakes that fail fast.

**Performance Improvement:** 10-100x faster on hard puzzles compared to standard backtracking

**Learn more:** See the [complete algorithm documentation](doc/ALGORITHMS.md) for:
- Step-by-step algorithm walkthroughs with examples
- Pseudocode and implementation details
- Performance benchmarks and complexity analysis
- Future enhancement roadmap (Naked Pairs, X-Wing, etc.)

## 📊 Performance Benchmarks

Typical solving times on standard hardware:

| Difficulty | Naked Singles | + Hidden Singles | + Backtracking |
|------------|---------------|------------------|----------------|
| Easy       | < 0.01s ✓     | < 0.01s ✓        | < 0.01s ✓      |
| Medium     | ✗             | 0.01-0.05s ✓     | 0.01-0.05s ✓   |
| Hard       | ✗             | ~50% solved      | 0.05-0.5s ✓    |
| Evil       | ✗             | ✗                | 0.5-5s ✓       |

Note: Optimized backtracking (MRV heuristic) is recommended for hard and evil puzzles.

## 🔧 Advanced Usage

### Custom Test Framework

```python
from tester import Tester

tester = Tester()
tester.setTestGroup("Validation Tests")

# Test with custom checker
tester.test_checker(sudoku.isValid(), "Grid is valid")
tester.test_checker(sudoku.isSolved(), "Grid is solved")

print(tester)  # Print pass/fail summary
```

### Debug Mode

```python
sudoku = Sudoku(grid)
sudoku.debugLevel = 1  # Show which values are being set and why

# Output example:
# Single candidate set at position: (0, 2): 4
# Hidden single in row 3 set at position: (3, 5): 7
```

### Cascading Solver Strategy

```python
def solve_with_fallback(sudoku):
    """Try logical methods first, fall back to backtracking if needed."""
    # Try naked singles only
    if sudoku.solver1(enableHiddenSingles=False):
        return "Solved with naked singles"
    
    # Try hidden singles
    if sudoku.solver1(enableHiddenSingles=True):
        return "Solved with hidden singles"
    
    # Use optimized backtracking
    if sudoku.solveBacktrackOptimized():
        return "Solved with backtracking"
    
    return "Unsolvable"
```

## 🛠️ Development

### Code Style
- Follows Python PEP 8 conventions
- Uses type hints throughout
- Snake_case for variables and functions
- Comprehensive docstrings

### Future Enhancements
- [ ] Naked Pairs/Triples elimination
- [ ] Pointing Pairs (Box-Line Reduction)
- [ ] X-Wing and Swordfish techniques
- [ ] Puzzle generator
- [ ] GUI interface
- [ ] Puzzle difficulty rating
- [ ] Step-by-step solution explanations

## 👤 Author

**Werner Schoegler**

Started: November 2025

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

Test puzzles sourced from:
- [Der Standard](https://www.derstandard.at) (Austria)
- [Kleine Zeitung](https://www.kleinezeitung.at) (Austria)
- [Sudoku.com](https://sudoku.com)
- Various Sudoku puzzle books and collections
- Top 95 hardest puzzles collection
- AI Escargot and other challenging puzzles

## 📚 References

- [Sudoku Solving Techniques](https://www.sudokuwiki.org/sudoku.htm)
- [Constraint Satisfaction Problems](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem)
- [Backtracking Algorithms](https://en.wikipedia.org/wiki/Backtracking)

---

**Happy Solving! 🧩**
