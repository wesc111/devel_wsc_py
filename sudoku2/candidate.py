# sudoku2.py

# a candidate class for a sudoku solver
class Candidate:
    """Represents a cell in a Sudoku puzzle with possible candidate values."""
    
    def __init__(self, row: int, col: int, values: list[int]):
        self.row = row
        self.col = col
        self.values = values.copy()  # Copy to avoid external mutation
    
    def __str__(self) -> str:
        return f"Candidate(row: {self.row}, col: {self.col}, values: {self.values})"
    
    def __repr__(self) -> str:
        return f"Candidate({self.row}, {self.col}, {self.values})"
    
    def set_values(self, values: list[int]) -> None:
        """Replace all candidate values with a new list."""
        self.values = values.copy()

    def add_value(self, value: int) -> None:
        """Add a value to candidates if not already present."""
        if value not in self.values:
            self.values.append(value)

    def remove_value(self, value: int) -> None:
        """Remove a value from candidates if present."""
        if value in self.values:
            self.values.remove(value)

    # compare values checks the values of two candidates for equality, ignoring order and ignoring row, col
    def compare_values(self, other: 'Candidate') -> bool:
        """Check if two candidates have the same set of values (order-independent)."""
        return set(self.values) == set(other.values)


    