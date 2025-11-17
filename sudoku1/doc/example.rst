Example
========

Following example shows the simple usage of class sudoku_np1 to solve a SUDOKU.
In this example, the sudoku is read from a file using the sudoku_io class and then solved by usage of the sudoku_np1 class.

.. code-block:: python

    # parse input arguments
    # example usage: $python sudoku_ex1.py -num=4
    if len(sys.argv)==2:
        firstArg = sys.argv[1]
        if "-num" in firstArg:
            n = int(firstArg.replace("-num=", ""))
            SU_NUM=n
        else:
            SU_NUM=1

    # read the input file into arrays suText, suComment
    myIo = sudoku_io()
    myIo.readFile("sudoku_1.txt")
    suText, suComment = myIo.getSudokuList()

    MAX_GUESS_NUM = 100

    # now create a sudoku class and provide SUDOKU to that class
    mySudoku = sudoku_np1()
    # set the sudoku by providing it in string/text form
    mySudoku.setSuArray(suText[SU_NUM])
    mySudoku.setComment(suComment[SU_NUM])
    # print the unsolved SUDOKU
    print(f"\nInput SUDOKU array #{SU_NUM}")
    mySudoku.printRst()

    # now call a solver method
    solved1 = mySudoku.solver1(False)
    # if solver1 does not succeed, call solver2
    if solved1:
        print("\n=====> PASS: Solved SUDOKU with solver1")
    if not solved1:
        solved2, num_guesses = mySudoku.solver2(MAX_GUESS_NUM)
        if solved2:
            print("\n=====> PASS: Solved SUDOKU with solver2")
        else:
            print("\n=====> FAIL: No solution found for SUDOKU with solver1/solver2 algorithms")

    # print the solved SUDOKU
    print(f"\nSolution SUDOKU array for #{SU_NUM}")
    mySudoku.printRst()