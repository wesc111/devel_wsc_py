""" sudoku_np1 sudoku class
A class implementing algorithms based on algorithms used by humans to solve SUDOKUs
Version 0.11, WSC, 3-Jan-2025"""

import numpy as np
from enum import Enum
import random
import time

# some very basic classes for SUDOKUs are defined in following package
from sudoku_p import *

USE_RANDOM_SEED = False

class sudoku_np1:
    """python class to solve SUDOKUs in a human way (without backtracking)"""
    # a house is a group inside the Sudoku that is either row, col or block
    HOUSE_T_ROW = 0
    HOUSE_T_COL = 1
    HOUSE_T_BLOCK = 2
    def __init__(self):
        # arrays containing sudoku information
        self.suArray = np.zeros((9,9), dtype=np.int8)
        self.suArrayType = np.zeros((9,9), dtype=suElemT)
        # arrays for store/recall
        self.suArrayStore = np.zeros((9,9), dtype=np.int8)
        self.suArrayTypeStore = np.zeros((9,9), dtype=suElemT)
        if USE_RANDOM_SEED:
            t = int(time.time()*1000)
            rs = ((t & 0xff000000) >> 24) + \
                ((t & 0x00ff0000) >>  8) + \
                ((t & 0x0000ff00) <<  8) + \
                ((t & 0x000000ff) << 24)
            print(f"setting random seed to {rs}")
            random.seed(rs)

    def setComment(self,string):
        """Set comment string for actual SUDOKU"""
        self.comment = string

    def setSuArray(self,suText):
        """Set actual SUDOKU by a string suText"""
        row=col=0
        for elem in suText:
            if elem=='.' or elem=='0':
                elem='0'
                self.suArrayType[row][col] = suElemT.UNDEFINED
                self.suArray[row][col] = int(elem)
            else:
                self.suArrayType[row][col] = suElemT.FIXED
                self.suArray[row][col] = int(elem)
            if col==8:
                col=0
                if row<8:
                    row+=1
                else:
                    break
            else:
                col+=1
        self.calcAllCandidateList()

    def store(self):
        """Store SUDOKU to buffer suArrayTypeStore"""
        for row in range(0,9):
            for col in range(0,9):
                self.suArrayStore[row][col] =self.suArray[row][col]
                self.suArrayTypeStore[row][col] = self.suArrayType[row][col]

    def recall(self):
        """Restore SUDOKU from buffer suArrayTypeStore"""
        for row in range(0,9):
            for col in range(0,9):
                self.suArray[row][col] = self.suArrayStore[row][col]
                self.suArrayType[row][col] = self.suArrayTypeStore[row][col]

    def getSuArray(self):
        return self.suArray
    
    def calcAllCandidateList(self):
        """central calculation of the self.allCandidateList"""
        self.allCandidateList = []
        for row in range(0,9):
            for col in range(0,9):
                if self.suArrayType[row][col] == suElemT.UNDEFINED:
                    cl = candidateList(row,col,self.calcCandidateList(row,col))
                    #cl.row = row
                    #cl.col = col
                    #cl.block = self.getBlockNum(row,col)
                    #cl.list = self.calcCandidateList(row,col)
                    self.allCandidateList.append(cl)  

    def calcCandidateList(self,row,col):
        """calculate the candidate list for specific cell at row, col"""
        candidateList = [1,2,3,4,5,6,7,8,9]
        for e in self.getValListInRow(row):
            if e in candidateList:
                candidateList.remove(e)
        for e in self.getValListInCol(col):
            if e in candidateList:
                candidateList.remove(e)
        for e in self.getValListInBlock(self.getBlockNum(row,col)):
            if e in candidateList:
                candidateList.remove(e)
        return candidateList   
    
    def getCandidateList(self,row,col):
        """get the candidates of specific row, col"""
        for elem in self.allCandidateList:
            if elem.row==row and elem.col==col:
                return elem.list
        return []
    
    def getValListInRow(self,num):
        valList = []
        for i in range(0, 9):
            aVal=self.suArray[num][i]
            if aVal>0:
                valList.append(aVal) 
        valList.sort()
        return valList 
    
    def printValListInRow(self, num):
        ll = self.getValListInRow(num)
        print(f"row   #{num}: ",end='')
        for e in ll:
            print(f"{e},",end='')
        print(" ")

    def getValListInCol(self,num):
        valList = []
        for i in range(0, 9):
            aVal=self.suArray[i][num]
            if aVal>0:
                valList.append(aVal) 
        valList.sort()
        return valList 
    
    def printValListInCol(self, num):
        ll = self.getValListInCol(num)
        print(f"col   #{num}: ",end='')
        for e in ll:
            print(f"{e},",end='')
        print(" ")

    def getBlockNum(self,row,col):
        """get the block number of element defined by row, col"""
        return int(col/3) + 3*int(row/3)

    def getValListInBlock(self,blocknum):
        valList = []
        for row in range(0, 3):
            cOffset = 3 * (blocknum % 3)
            rOffset = 3 * int(blocknum / 3)
            for col in range(0,3):
                aVal=self.suArray[row+rOffset][col+cOffset]
                if aVal>0:
                    valList.append(aVal)
        valList.sort()
        return valList
    
    def printValListInBlock(self,num):
        ll = self.getValListInBlock(num)
        print(f"block #{num}: ",end='')
        for e in ll:
            print(f"{e},",end='')
        print(" ")
  
 
    def printAllCandidateList(self):
        """ print the actual list of all candidates
        note that the candidates need to be calculated before, eg with calcAllCandidateList()"""
        print("List of all candidates in actual sudoku:")
        for elem in self.allCandidateList:
            elem.print(1)
    
    def printAllCandidates(self):
        """ print all canditates and solution fields of the actual SUDOKU in matrix form"""
        print("Solution fields and candidates for actual sudoku:\n")
        for row in range(0,9):
            if row==0 or row==3 or row==6:
                print(" +-----------------------------+-----------------------------+----------------------------+")
            for col in range(0,9):
                if self.suArrayTypeStore[row][col]==suElemT.UNDEFINED:
                    myCandidateList = candidateList(row,col,self.calcCandidateList(row, col))
                    if col==0 or col==3 or col==6:
                        print(" | ",end="")
                    myCandidateList.print(1)
                    if col==8:
                        print("| ")
                else:
                    myCandidateList = candidateList(row,col,[self.suArray[row][col]])
                    if col==0 or col==3 or col==6:
                        print(" | ",end="")
                    if self.suArrayType[row][col]==suElemT.FIXED:
                        myCandidateList.print(1,True)
                    else:
                        myCandidateList.print(1,False)
                    if col==8:
                        print("| ")
        print(" +-----------------------------+-----------------------------+----------------------------+\n")

    def checkSolved(self):
        solvedFlag = True
        for row in range(0,9):
            for col in range(0,9):
                if self.suArrayType[row][col] == suElemT.UNDEFINED:
                    solvedFlag = False
        return solvedFlag
    
    def solveSingles(self):
        numSolvedSinglesFound = 0
        self.calcAllCandidateList()
        for elem in self.allCandidateList:
            row = elem.row
            col = elem.col
            if self.suArrayType[row][col] == suElemT.UNDEFINED and len(elem.list)==1:
                self.suArrayType[row][col] = suElemT.SOLVED_SINGLE
                self.suArray[row][col] = int(elem.list[0])
                numSolvedSinglesFound+=1
        return numSolvedSinglesFound

    #
    def findLonePairs(self):
        """find lone pairs: pairs within a row, col or block means that these can be removed in the candidate lists of the corresponding house
        TBD, not finished now
        i=0...row, 1...col, 2...block"""
        for i in range(0,2):
            for j in (range(0,9)):
                ddList=[]
                # iterate through all elements
                for elem in self.allCandidateList:
                    if (i==self.HOUSE_T_ROW and elem.row==j) or (i==self.HOUSE_T_COL and elem.col==j) or (i==self.HOUSE_T_BLOCK and elem.block==j):
                        if len(elem.list)==2:
                            ddList.append(elem.list)
                if len(ddList)>1:
                    dupFlag, dup = self.checkDuplicates(ddList)
                    if dupFlag:
                        if i==self.HOUSE_T_ROW:
                            print(f"LONE row={j}:  {dupFlag}, {dup}, {ddList}")
                        if i==self.HOUSE_T_COL:
                            print(f"LONE col={j}:  {dupFlag}, {dup}, {ddList}")
                        if i==self.HOUSE_T_BLOCK:
                            print(f"LONE block={j}: {dupFlag}, {dup}, {ddList}")
        return False

    
    def findSingle(self, cc):
        """find singles in the input list cc"""
        oc = [0,0,0,0,0,0,0,0,0,0]
        for elem in cc:
            oc[elem] += 1
        retVal = []
        count = 0
        for i in range(1,9):
            if oc[i]==1:
                retVal.append(i)
                count += 1
        return count, retVal
    
    def solveHiddenSingles(self,debug=False):
        """solve hidden singles
        hidden singles are elements that appear just once in a row, col or block list"""
        self.calcAllCandidateList()
        hiddenSinglesFound = 0
        for row in range(0,9):
            cc = []
            # create list cc with all elements inside of row
            for col in (range(0,9)):
                for elem in  self.getCandidateList(row,col):
                    cc.append(elem)
            cc.sort()
            count, hsList = self.findSingle(cc)
            if count>0:
                if (debug):
                    print(f"Found hidden singles {hsList} in row {row}")
                self.setHiddenSingles(0, row, hsList)
                hiddenSinglesFound += len(hsList)
        for col in range(0,9):
            cc = []
            # create list cc with all elements inside of col
            for row in (range(0,9)):
                for elem in  self.getCandidateList(row,col):
                    cc.append(elem)
            cc.sort()
            count, hsList = self.findSingle(cc)
            if count>0:
                if (debug):
                    print(f"Found hidden singles {hsList} in col {col}")
                self.setHiddenSingles(1, col, hsList)
                hiddenSinglesFound += len(hsList)
        for block in range(0,9):
            cc = []
            # create list cc with all elements inside of block
            for blockElem in self.blockIndexList(block):
                row, col = blockElem
                for elem in  self.getCandidateList(row,col):
                    cc.append(elem)
            cc.sort()
            count, hsList = self.findSingle(cc)
            if count>0:
                if (debug):
                    print(f"Found hidden singles {hsList} in block {block}")
                self.setHiddenSingles(2, block, hsList)
                hiddenSinglesFound += len(hsList)
        
        return hiddenSinglesFound
    
    def blockIndexList(self,block):
        """return a list of row,col indices for a block number"""
        if   block==0: 
            return [[0,0],[0,1],[0,2], [1,0],[1,1],[1,2], [2,0],[2,1],[2,2]]
        elif block==1: 
            return [[0,3],[0,4],[0,5], [1,3],[1,4],[1,5], [2,3],[2,4],[2,5]]
        elif block==2: 
            return [[0,6],[0,7],[0,8], [1,6],[1,7],[1,8], [2,6],[2,7],[2,8]]
 
        elif block==3: 
            return [[3,0],[3,1],[3,2], [4,0],[4,1],[4,2], [5,0],[5,1],[5,2]]
        elif block==4: 
            return [[3,3],[3,4],[3,5], [4,3],[4,4],[4,5], [5,3],[5,4],[5,5]]
        elif block==5: 
            return [[3,6],[3,7],[3,8], [4,6],[4,7],[4,8], [5,6],[5,7],[5,8]]
 
        elif block==6: 
            return [[6,0],[6,1],[6,2], [7,0],[7,1],[7,2], [8,0],[8,1],[8,2]]
        elif block==7: 
            return [[6,3],[6,4],[6,5], [7,3],[7,4],[7,5], [8,3],[8,4],[8,5]]
        elif block==8: 
            return [[6,6],[6,7],[6,8], [7,6],[7,7],[7,8], [8,6],[8,7],[8,8]]        
 
        else:           
            return [[0,0],[0,0],[0,0], [0,0],[0,0],[0,0], [0,0],[0,0],[0,0]] 
              
    def rowIndexList(self,row):
       """return a list of indices for a row"""
       return [[row,0],[row,1],[row,2], [row,3],[row,4],[row,5], [row,6],[row,7],[row,8]]
    
    def colIndexList(self,col):
       """return a list of indices for a column"""
       return [[0,col],[1,col],[2,col], [3,col],[4,col],[5,col], [6,col],[7,col],[8,col]]

   
    def setHiddenSingles(self, type, num, singleList):
        """type: row=0, col=1, block=2
        num ... row/block/col number (0-8)
        singleList ... list of hidden singles (found with findHiddenSingles)"""
        if type==0:
            for elem in singleList:
                row = num
                for col in range(0,9):
                    if self.suArray[row,col]==0 and elem in self.getCandidateList(row,col):
                        self.suArray[row,col] = elem
                        self.suArrayType[row,col] = suElemT.SOLVED_HIDDEN_SINGLE
        elif type==1:
            for elem in singleList:
                col = num
                for row in range(0,9):
                    if self.suArray[row,col]==0 and elem in self.getCandidateList(row,col):
                        self.suArray[row,col] = elem
                        self.suArrayType[row,col] = suElemT.SOLVED_HIDDEN_SINGLE
        elif type==2:
            for elem in singleList:
                block = num
                for blockElem in self.blockIndexList(block):
                    row, col = blockElem
                    if self.suArray[row,col]==0 and elem in self.getCandidateList(row,col):
                        self.suArray[row,col] = elem
                        self.suArrayType[row,col] = suElemT.SOLVED_HIDDEN_SINGLE

    def checkDuplicates(self, ll):
        """check if there are duplicates in the list ll"""
        for i in range(0,len(ll)):
            for j in range(0,len(ll)):
                if i!=j:
                    if ll[i]==ll[j]:
                        return True, ll[i]
        return False, [0,0]

   
    def solver1(self, debug=False):
        """solver algorithm to solve SUDOKU just with "paper & pencil" methods
        return value is True if sudoku is solved"""
        i=m=0
        n=1
        while n>0 or m>0:
            n = self.solveSingles()
            self.calcAllCandidateList()
            m = self.solveHiddenSingles(debug)
            if debug and (n>0 or m>0):
                print(f"i={i}: ",end="")
            if debug and n>0:
                print(f"num solved singles = {n} ",end="")
            if debug and m>0:
                print(f", num solved hidden singles = {m}",end="")
            if debug and (n>0 or m>0):
                print("")
            i+=1
        return self.checkSolved()
    
    def solver2(self, max_guess_num, debug=False):
        """ solver algorithm doing guesses and run solver 1 with that guess
        return value is True if sudoku is solved + number of guesses"""
        self.store()
        solved = False
        i=0
        # if SUDOKU is not solved, start with guesses inside of following loop:
        while solved==False and i<max_guess_num:
            if debug:
                print(f"... guess number {i}")
            self.doAGuess(debug)
            # no debug for solver1 here, as most of the trials are anyhow wrong
            solved1 = self.solver1()
            solved2 = self.checkSudokuIsValid()
            solved = solved1 and solved2
            i+=1
            if solved:
                print(f"...found solution with SOLVER2 after {i} guesses")
                return True, i
            else:
                self.recall()
                # recalc the candidate list after restored
                self.calcAllCandidateList()       
        return False, i

    def numDoubleCandidates(self):
        self.calcAllCandidateList()
        n = 0
        for elem in self.allCandidateList:
            if len(elem.list)==2:
                n+=1
        return n

    def doAGuess(self, debug=False):
        """doAGuess: first trial implementation, works not bad, but can be improved a lot (TBD)
        return value: True if guess is done, false means no guess was found"""
        # and do a new guess out of the candidate list
        self.calcAllCandidateList()
        numDoubleCandidates=self.numDoubleCandidates()
        if numDoubleCandidates>0:
            randDoubleCandNum=random.randrange(0,numDoubleCandidates)
        else:
            return False
        if debug:
            print(f"Number of double candidates: {numDoubleCandidates}")
            print(f"Randomized double candidate num: {randDoubleCandNum}")
        randDoubleCandAct=0
        for elem in self.allCandidateList:
            row = elem.row
            col = elem.col
            # guess is done on elements with 2 entries in list
            if len(elem.list)==2 and randDoubleCandAct==randDoubleCandNum:
                # select one of the two elements in candidateList
                index = random.randrange(0,2)
                val = elem.list[index]
                self.suArray[row][col] = val
                self.suArrayType [row][col] = suElemT.GUESS
                if debug:
                    print(f"doAGuess: value at row={elem.row} col={elem.col} set to {val} (index={index})")
                return True
            elif len(elem.list)==2:
                randDoubleCandAct+=1
        return False
            

    def checkValidHouse(self, houseList):
        """check if the house list is valid (each value from 1 to 9 shall be exactly one time within the list)"""
        validList=[1,2,3,4,5,6,7,8,9]
        if len(houseList)!=9:
            return False
        for i in range(0,9):
            if houseList[i]<1 or  houseList[i]>9:
                return False
            if houseList[i] in validList:
                validList.remove(houseList[i])
        if len(validList)==0:
            return True
        return False       

    def checkSudokuIsValid(self,printFlag=False):
        """check if the actual sudoku is valid by checking all rows, columns and blocks of SUDOKU
        for values 1 to 9 (each one shall exist exactly one time)"""
        retVal = True
        for i in range(0,9):
            actList=self.getValListInRow(i)
            checkResult=self.checkValidHouse(actList)
            if (checkResult==False) and printFlag:
                print(f"Check result for row  {i} failed: {checkResult}")
                return False
        for i in range(0,9):
            actList=self.getValListInCol(i)
            checkResult=self.checkValidHouse(actList)
            if (checkResult==False) and printFlag:
                print(f"Check result for col  {i} failed: {checkResult}")
                return False
        for i in range(0,9):
            actkList=self.getValListInBlock(i)
            checkResult=self.checkValidHouse(actList)
            if (checkResult==False) and printFlag:
                print(f"Check result for block {i} failed: {checkResult}")
                return False
        # if no error was found up to this point, the SUDOKU is valid
        return True
    
    def checkSudokuIsSolved(self):
        """check that SUDOKU is valid and no element is 0 (unsolved)"""
        if not self.checkSudokuIsValid():
            return False
        for row in range(0,9):
            for col in range(0,9):
                if self.suArray[row][col]==0:
                    return False
        # if no error was found up to this point, the SUDOKU is solved
        return True


    def print(self, printType=0):
        """print the sudoku array
        rstFlag ... if true, print table in restructed text format
        printType ... 0: simple output, 1: RST format, 2: RST format with candidates"""

        def printRst():
            """print the SUDOKU using restructed text format (for sphinx doc system, 
            see https://www.sphinx-doc.org/en/master/usage/quickstart.html)"""
            print("\n+---+---+---+---+---+---+---+---+---+")
            for row in self.suArray:
                i=0
                for elem in row: 
                    if i==0:
                        print("|",end="")
                    if elem==0:
                        elem='.'
                    print(f" {elem} |",end="")
                    if i<8:
                        i+=1
                    else:
                        print("\n+---+---+---+---+---+---+---+---+---+")
                        i=0
            print("")

        if len(self.comment)>0:
            print(f"===== {self.comment}")
        if printType==0:
            print(self.suArray)
        elif printType==1:
            printRst()
        elif printType==2:
            self.printAllCandidates()  

