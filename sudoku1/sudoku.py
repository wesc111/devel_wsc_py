#!/usr/local/bin/python3
""" program to solve SUDOKUs that can be read from a file
For command description, start $python3 sudoku.py -help
Version 0.11, WSC, 3-Jan-2025"""
VERSION = "0.12"
VERSION_DATE = "3-Jan-2025"

# numbering of SUDOKUS in input file:
# first line is line number 1
# that way, the number in the argument -num, -start, -stop is exactly the line number shown in a text editor 

from sudoku_np1 import sudoku_np1
from sudoku_io import sudoku_io
import sys

# basic definitions (parts are overwritten by optional command line arguments)
DEBUG_FLAG=False
SU_NUM_START=0
SU_NUM_STOP=SU_NUM_START+1
SU_NUM_ALL=False
PRINT_FLAG=True
MAX_GUESS_NUM=50
USE_SOLVER2=True
SU_FILE_NAME="sudoku_1.txt"

def printList(text1,list1):
    """function to print number lists"""
    print(text1, end="")
    for elem in list1:
        print(f"{elem} ",end="")
    print("")

# parse input arguments
# example usage: $python sudoku_ex1.py -num=4
if len(sys.argv)>=2:
    for i in range(1,len(sys.argv)):
        actArg = sys.argv[i]
        if "-debug" in actArg:
            DEBUG_FLAG=True
        if DEBUG_FLAG:
            print(f"... processing argument: {actArg}")
        if "-f=" in actArg:
            fname = actArg.replace("-f=", "")
            if len(fname)>0:
                 SU_FILE_NAME=fname
        if "-num=" in actArg:
            n = int(actArg.replace("-num=", ""))-1
            if n<0:
                n=0
            SU_NUM_START=n
            SU_NUM_STOP=SU_NUM_START+1
        if "-start=" in actArg:
            n = int(actArg.replace("-start=", ""))-1        
            if n<0:
                n=0
            SU_NUM_START=n
            SU_NUM_STOP=SU_NUM_START+1
        if "-stop=" in actArg:
            n = int(actArg.replace("-stop=", ""))-1
            if n<0:
                n=0
            SU_NUM_STOP=n+1
        if "-all" in actArg:
            SU_NUM_ALL=True
        if "-noprint" in actArg:
            PRINT_FLAG=False
        if "-h" in actArg:
            print("Optional arguments for sudoku_ex1:")
            print("    -h               ... print help")
            print("    -v               ... show program version")
            print("    -debug           ... show detailed debug info")
            print("    -num=3           ... solve SUDOKU #3")
            print("    -start=3 -stop=8 ... solve SUDOKU #3 to #8")
            print("    -all             ... solve all SUDOKUs read from input file")
            print("    -noprint         ... no print of SUDOKU solution, just print PASS/FAIL results")
            print("    -f=sudoku_1.txt  ... read SUDOKUs from file sudoku_1.txt")
            sys.exit()
        if "-v" in actArg:
            print(f"    Welcome to sudoku_ex1, this is version {VERSION} from {VERSION_DATE}")
            sys.exit()

# read the input file into arrays suText, suComment
myIo = sudoku_io()
print(f"... reading file name {SU_FILE_NAME}")
numRead = myIo.readFile(SU_FILE_NAME)
suText, suComment = myIo.getSudokuList()

# now create a sudoku class and provide SUDOKU to that class
mySudoku = sudoku_np1()

if SU_NUM_ALL:
    SU_NUM_START=0
    SU_NUM_STOP=SU_NUM_START+numRead

solver1Count = 0
solved1List = []
solver2Count = 0
solved2List = []
notSolvedCount = 0
notSolvedList = []
for i in range(SU_NUM_START,SU_NUM_STOP):
    # set the sudoku by providing it in string/text form
    print(f"Reading sudoku number: {i+1}")
    mySudoku.setSuArray(suText[i])
    mySudoku.setComment(suComment[i])
    # print the unsolved SUDOKU
    if PRINT_FLAG:
        print(f"\nInput SUDOKU array #{i+1}")
        mySudoku.print(1)

    # now call a solver method
    solved1 = mySudoku.solver1(DEBUG_FLAG)
    # if solver1 does not succeed, call solver2
    if solved1:
        if mySudoku.checkSudokuIsValid()==False:
            print(f"\n=====> ERROR in solver1 solution for SUDOKU array #{i+1}: SUDOKU is not valid",end="")
            solved1=False
        else:
            print(f"\n=====> PASS: Solved SUDOKU #{i} with solver1")
            solver1Count+=1
            solved1List.append(i+1)

    if not solved1 and USE_SOLVER2:
        solved2, num_guesses = mySudoku.solver2(MAX_GUESS_NUM,DEBUG_FLAG)
        if solved2:
            if mySudoku.checkSudokuIsValid()==False:
                print(f"\n=====> ERROR in solver2 solution for SUDOKU array #{i+1}: SUDOKU is not valid",end="")
                solved2=False
            else:
                print(f"\n=====> PASS: Solved SUDOKU #{i+1} with solver2")
                solver2Count+=1
                solved2List.append(i+1)

    solved = solved1 or solved2
    if not solved:
        notSolvedCount+=1
        notSolvedList.append(i+1)
        print(f"\n=====> FAIL: No solution found for SUDOKU #{i+1} with selected solver algorithms")
    # finally check if the solution is valied

    # print the solved SUDOKU
    if PRINT_FLAG:
        if mySudoku.checkSudokuIsSolved():
            print(f"\nSolution SUDOKU array for #{i+1}")
            mySudoku.print(1)
        else:
            print(f"\nERROR: NO Solution found for SUDOKU array #{i+1}")
            mySudoku.print(2)    

# print overall statistics for all SUDOKUs that were selected
if solver1Count>0:
    print(f"Number of SUDOKUs solved with solver1: {solver1Count}")
    printList("List of solved SUDOKUs with solver1: ", solved1List)
if solver2Count>0:
    print(f"Number of SUDOKUs solved with solver2: {solver2Count}")
    printList("List of solved SUDOKUs with solver2: ", solved2List)
if notSolvedCount==0:
    print(f"All selected SUDOKUs solved")
else:
    print(f"Number of unsolved SUDOKUs : {notSolvedCount}")
    printList("List of unsolved SUDOKUs: ", notSolvedList)