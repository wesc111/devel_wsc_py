""" sudoku_p sudoku package
simple functions and class definitions used by sudoku_np1
Version 0.11, WSC, 3-Jan-2025"""


from enum import Enum

# format string to be 9 characters long and centered
def formatStr9c(str):
    str1=""
    for i in range(0,5-int(len(str)/2)):
        str1=str1+" "
    str=str1+str
    for i in range(9-len(str)):
        str=str+" "
    return str

def rowcol2block(row, col):
    """return block number from row and col number"""
    if row<=2:
        if col<=2:
            return 0
        if col>=3 and col<=5:
            return 1
        if col>=6:
            return 2
    if row>=3 and row <=5:
        if col<=2:
            return 3
        if col>=3 and col<=5:
            return 4
        if col>=6:
            return 5
    if row>=6:
        if col<=2:
            return 6
        if col>=3 and col<=5:
            return 7
        if col>=6:
            return 8
    else:
        return 0     


# Class suElemT defines the type of a Sudoku element
class suElemT(Enum):
    """This is the documentation for MyClass."""
    UNDEFINED = 0
    FIXED = 1
    SOLVED_SINGLE = 2
    SOLVED_HIDDEN_SINGLE = 3
    GUESS = 4

# The candidate list for a sudoku element
class candidateList():
    row = 0
    col = 0
    block = 0
    list = []
    def __init__(self, row, col, candidates):
        self.row = row
        self.col = col
        self.block = rowcol2block(row, col)
        self.list = candidates
    def print(self, printType, leadingAsterixFlag=False):
        if printType==0:
            print(f"row={self.row}, col={self.col} block={self.block}: {self.list}")
        elif printType==1:
            if leadingAsterixFlag:
                str="*"
            else:
                str=""
            for elem in self.list:
                str=str+f"{elem}"
            print(f"{formatStr9c(str)}",end="")
