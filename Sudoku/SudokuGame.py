import numpy as np
import json
import random

from .SudokuSettings import *

class Sudoku():
      def __init__(self, x, difficulty):
            self.sudokuArray = np.zeros([9,9], dtype = int)

            if x == 1:
                  self.basicSudokuArray = self.__generateDiagonalSudoku()
                  self.__generateRest()
                  self.__generateEmptySpaces(difficulty)
                  self.sudokuArray = np.copy(self.basicSudokuArray)
            elif x == 2:
                  self.basicSudokuArray = self.getSudokuFromFile(difficulty)
                  self.sudokuArray = np.copy(self.basicSudokuArray)
            else:
                  self.basicSudokuArray = np.zeros([9,9], dtype = int)
                  self.sudokuArray = np.zeros([9,9], dtype = int)

      
      def __del__(self):
            self.sudokuArray = []
            self.sudokuArray = []

      def getBasicSudokuArray(self):
            '''
            Return basic Sudoku Matrix.
            '''
            return self.basicSudokuArray

      def getSudokuArray(self):
            '''
            Return main Sudoku Matrix.
            '''
            return self.sudokuArray

      def updateSudokuArray(self, row, col, value):
            '''
            Update main Sudoku Matrix with a given value.
            '''
            if not isinstance(value, (int)):
                  raise TypeError("Error: Cell value must be a number.")
            self.sudokuArray[row][col] = value
            return

      def restartSudokuTable(self):
            '''
            Restart Sudoku, copy from basic Matrix.
            '''
            self.sudokuArray = np.copy(self.basicSudokuArray)







      def getSudokuFromFile(self, difficulty):
            '''
            Opens JSON file and return Sudoku Matrix depend on difficulty
            '''
            f = open('Sudoku\\sudoku.json')
            data = json.load(f)
            retSudoku = np.zeros([0,0], dtype = int)

            sudokuVariant = random.randint(0, len(data[difficulty])-1)

            for arr in data[difficulty][sudokuVariant]:
                  for row in arr:
                        retSudoku = np.append(retSudoku, row)

            retSudoku = np.resize(retSudoku, (9,9))
            return retSudoku

      def __generateDiagonalSudoku(self):
            '''
            Generates numbers in Matrix diagonally
            '''
            retSudoku = np.zeros([9,9], dtype = int)

            for i in range(0, 3):
                  freeNumbers = list(range(1, 10))
                  for row in range(0 + 3*i, 3 + 3*i):
                        for col in range(0 + 3*i, 3 + 3*i):
                              number = random.choice(freeNumbers)
                              freeNumbers.remove(number)
                              retSudoku[row][col] = number

            return retSudoku
      
      def __generateEmptySpaces(self, difficulty):
            '''
            Sets empty spaces in the matrix.
            Count depend on difficulty.
            '''

            r1, r2 = SudokuSettings.DIFFICULTY_DICT[difficulty]
            spaces = random.randint(r1, r2)

            while(spaces != 0):
                  randRow = random.randint(0, len(self.basicSudokuArray)-1)
                  randCol = random.randint(0, len(self.basicSudokuArray)-1)
                  if self.basicSudokuArray[randRow][randCol] != 0:
                        self.basicSudokuArray[randRow][randCol] = 0
                        spaces -= 1

            return

      def findEmptySpaces(self):
            '''
            Finds the first empty space in the matrix - 0
            '''
            for row in range(len(self.basicSudokuArray)):
                  for col in range(len(self.basicSudokuArray[row])):
                        if self.basicSudokuArray[row][col] == 0:
                              return (row, col)

            return False

      def solveBasicSudoku(self): 
            '''
            Solves the matrix (use recursion)
            '''
            spacesAvailable = self.findEmptySpaces()
            if spacesAvailable == False:
                  return True
            
            row, col = spacesAvailable

            for n in range(1, 10):
                  if self.checkSpace(n, row, col):
                        self.basicSudokuArray[row][col] = n
                        
                        if self.solveBasicSudoku():
                              return True
                        
                        self.basicSudokuArray[row][col] = 0

            return False

      def checkSpace(self, num, row, col):
            '''
            Checks if we can enter a number in a given position in the matrix.
            '''
            if self.basicSudokuArray[row][col] != 0:
                  return False

            for tempcol in range(len(self.basicSudokuArray)):
                  if self.basicSudokuArray[row][tempcol] == num:
                        #if tempcol != col:
                        return False

            for temprow in range(len(self.basicSudokuArray)):
                  if self.basicSudokuArray[temprow][col] == num:
                        return False
            
            modRow = (row // 3) * 3
            modCol = (col // 3) * 3

            for i in range(modRow, modRow+3):
                  for j in range(modCol, modCol+3):
                        if self.basicSudokuArray[i][j] == num:
                              return False
            
            return True
      
      def __generateRest(self):
            '''
            Generate rest of the matrix
            '''
            for row in range(len(self.basicSudokuArray)):
                  for col in range(len(self.basicSudokuArray[row])):
                        if self.basicSudokuArray[row][col] == 0:
                              randNum = random.randint(1, 9)

                              if self.checkSpace(randNum, row, col):
                                    self.basicSudokuArray[row][col] = randNum
                                    
                                    if self.solveBasicSudoku():
                                          return self.basicSudokuArray

                                    self.basicSudokuArray[row][col] = 0

            return False
      
      def checkSudokuPosition(self, num, row, col):
            '''
            Checks if we can enter a number in a given position in the matrix.
            Checks by row and column.
            '''
            for tempcol in range(len(self.basicSudokuArray)):
                  if self.basicSudokuArray[row][tempcol] == num and tempcol != col:
                        return False

            for temprow in range(len(self.basicSudokuArray)):
                  if self.basicSudokuArray[temprow][col] == num and temprow != row:
                        return False
            
            return True






      def checkSpaceMainTable(self, num, row, col):
            '''
            Checks if we can enter a number into a given position in main matrix.
            '''
            for tempcol in range(len(self.sudokuArray)):
                  if self.sudokuArray[row][tempcol] == num:
                        if tempcol != col:
                              return False

            for temprow in range(len(self.sudokuArray)):
                  if self.sudokuArray[temprow][col] == num:
                        if temprow != row:
                              return False

            modRow = (row // 3) * 3
            modCol = (col // 3) * 3

            for i in range(modRow, modRow+3):
                  for j in range(modCol, modCol+3):
                        if self.sudokuArray[i][j] == num:
                              if i != row and j != col:
                                    return False
            
            return True

      def validateSudoku(self):
            '''
            Validate the correctness of main Sudoku matrix row by row, column by column.
            '''
            for row in range(len(self.sudokuArray)):
                  for col in range(len(self.sudokuArray[row])):
                        if self.checkSudokuPositionMainTable(self.sudokuArray[row][col], row, col) != True:
                              return False
            
            return True

      def getValidateErrors(self):
            '''
            Return position of errors in main Sudoku matrix.
            '''
            errors = []
            
            for row in range(len(self.sudokuArray)):
                  for col in range(len(self.sudokuArray[row])):
                        if self.checkSudokuPositionMainTable(self.sudokuArray[row][col], row, col) != True:
                              if self.basicSudokuArray[row][col] == 0:
                                    if self.sudokuArray[row][col] != 0:
                                          errors.append((row, col))
            
            return errors
      
      def checkSudokuPositionMainTable(self, num, row, col):
            '''
            Checks if we can enter a number in a given position in the main matrix.
            Checks by row, column, and square.
            '''
            for tempcol in range(len(self.sudokuArray)):
                  if self.sudokuArray[row][tempcol] == num and tempcol != col:
                        return False

            for temprow in range(len(self.sudokuArray)):
                  if self.sudokuArray[temprow][col] == num and temprow != row:
                        return False
            
            row_start = (row // 3) * 3
            col_start = (col // 3) * 3

            for temprow in range(row_start, row_start + 3):
                  for tempcol in range(col_start, col_start + 3):
                        if temprow != row and tempcol != col:
                              if self.sudokuArray[temprow][tempcol] == num:
                                    return False
            
            return True

      def findEmptySpacesMainTable(self):
            '''
            Finds the first empty space in main matrix - 0
            '''
            for row in range(len(self.sudokuArray)):
                  for col in range(len(self.sudokuArray[row])):
                        if self.sudokuArray[row][col] == 0:
                              return (row, col)

            return False


      def solveMainTable(self): 
            '''
            Solves main matrix (use recursion) in Sudoku solver
            '''
            spacesAvailable = self.findEmptySpacesMainTable()
            if spacesAvailable == False:
                  return True
            
            row, col = spacesAvailable

            for n in range(1, 10):
                  if self.checkSpaceMainTable(n, row, col):
                        self.sudokuArray[row][col] = n
                        
                        if self.solveMainTable():
                              return True
                        
                  self.sudokuArray[row][col] = 0

            return False

      
      def validateSudokuSolver(self):
            '''
            Validate the correctness of main Sudoku matrix row by row, column by column.
            '''
            for row in range(len(self.sudokuArray)):
                  for col in range(len(self.sudokuArray[row])):
                        if self.sudokuArray[row][col] != 0:
                              if self.checkSudokuPositionMainTable(self.sudokuArray[row][col], row, col) != True:
                                    return False
            
            return True