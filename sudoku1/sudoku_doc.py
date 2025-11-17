# SUDOKU documentation
# program to generate SUDOKU pretty print documentation
# Version 0.00.00, WSC, 26-Dec-2024

from sudoku_np1 import sudoku
from sudoku_io import sudoku_io

# read the input file into arrays suText, suComment
myIo = sudoku_io()
myIo.readFile("sudoku_1.txt")
suText, suComment = myIo.getSudokuList()

SU_NUM = 2
MAX_GUESS_NUM = 100

# now create a sudoku class and provide SUDOKU to that class
mySudoku = sudoku()
mySudoku.setSuArray(suText[SU_NUM])
mySudoku.setComment(suComment[SU_NUM])
mySudoku.printRst()

solved1 = mySudoku.solver1(False)
if not solved1:
    solved2, num_guesses = mySudoku.solver2(MAX_GUESS_NUM)

mySudoku.printRst()

