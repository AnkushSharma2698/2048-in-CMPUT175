import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self._grid = self.createGrid(row, col)    # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells

        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)


    def createGrid(self, row, col):
        myGrid = []
        #initial While loop creates the four rows
        i = 0
        while i <row:
            myGrid.append([])
            i+=1
            #This for loop creates the 4 columns
        for item in myGrid:
            j=0
            while j <col:
                item.append(0)
                j+=1   
        return myGrid         



    def setCell(self, cell, val):
        count = 0
        for i in range(0,self.row):
            for j in range(0,self.col):
                if cell == count:
                    self._grid[i][j] = val
                    count+=1
                else:
                    count +=1  


    def getCell(self, cell):
        
        count = 0
        for i in range(0,self.row):
            for j in range(0,self.col):
                if cell == count:
                    count+=1
                    return self._grid[i][j]
                else:
                    count +=1    


    def assignRandCell(self, init=False):

        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)


    def drawGrid(self):

        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + j)).center(5) + '|'
            print(line)


    def updateEmptiesSet(self):
        list1 = []
        for item in range(16): 
            x = list1.append(self.getCell(item))
        index = 0
        self.emptiesSet = []
        for item in list1:
            if item == 0:
                self.emptiesSet.append(index)
            index +=1
    
        

    def collapsible(self):
        #Check if There are zeroes in the grid
        for i in range(0,16):
            if self.getCell(i) == 0:
                return True
        #Check for side to side,skip the rightmost cells in each row
        skipped_cells= [3,7,11,15]
        for item in range(16):
            if not item in skipped_cells:
                if self.getCell(item) == self.getCell(item+1):
                    return True
        #Check Down the grid
        for item in range(0,13):
            if self.getCell(item) == self.getCell(item+4):
                return True 
        return False

    def collapseRow(self, lst):
        #https://codereview.stackexchange.com/questions/103764/2048-merge-function
        #used this link to get aid on the Truth condition for the collapse row function
        
        #Gets the list from the specified Collapse Function
        self.ListNumber = lst
    
        #The cases in which the output of collapse row would return FALSE
        zero_list = []
        for i in range(1,4):
            if self.ListNumber[i] == 0:
                zero_list.append(self.ListNumber[i])
        if zero_list ==[0,0,0] or self.ListNumber == [0,0,0,0]:
            return self.ListNumber,False   
        
        #True Condition
        change_list = [] 
        for item in self.ListNumber:
            #Append the non-zero values first because a left collapse requires empty spaces to be on the left.
            if item != 0:
                change_list.append(item)
        for item in self.ListNumber:
            #Append the zeroes here.
            if item == 0:
                change_list.append(item)
        #Checks for similar values and sees whether to combine or not
        Join = []
        for i, item in enumerate(change_list):
            if i == len(change_list)-1:
                Join.append(item)
                if len(Join) != len(self.ListNumber):
                    Join.append(0)
                break
            #Check if the current item is the same as the following item
            if item == change_list[i+1]:
                if item != 0:
                    #multiplies that item that appeard consecutively by 2 to get the value.
                    new_num = item*2
                    #For every Collapse that occurs. We increment the score by that much here.
                    self.score  = self.score + new_num
                    Join.append(new_num)
                    change_list[i+1] -= change_list[i+1]
                else:
                    Join.append(item)
            else:
                    Join.append(item)  
        change_list = []  
        for item in Join:
            if item != 0:
                change_list.append(item)
        for item in self.ListNumber:
            if item == 0:
                change_list.append(item)
        #Add in zeroes for all remaining values after the left Collapse
        for _ in range(len(self.ListNumber) - len(change_list)):
            if len(self.ListNumber) != len(change_list):
                change_list.append(0)
        #Return the Collapsed List, and also return True
        return change_list,True 



    def collapseLeft(self):
        self.collapsed = False
        self.newgrid = []
        #First get the cells from the grid and put it into a new list that we can manipulate.
        for i in range(0,16):
            self.x = self.getCell(i)
            self.newgrid.append(self.x)
        #self.splitgrid is going to be Identical to original grid
        self.splitgrid = []
        for i in range(0,16,self.row):
            self.splitgrid.append(self.newgrid[i:i+4])
         
        self.splittedLst = []   
        #Collapse each row in the splitgrid. Then return it and append it to a new list.
        self.truth_val = []
        for row in self.splitgrid:
            x = self.collapseRow(row)
            self.splittedLst.append(x[0])
            self.truth_val.append(x[1])
       #Set the cells now
        count = 0
        for i in range(0,4):
            for j in range(0,4):
                self.setCell(count,self.splittedLst[i][j])
                count +=1
        if True in self.truth_val:
            self.collapsed = True
            return True


    def collapseRight(self):
        self.collapsed = False
        self.newgrid = []
        #First get the cells from the grid and put it into a new list that we can manipulate.
        for i in range(0,16):
            self.x = self.getCell(i)
            self.newgrid.append(self.x)
        #self.splitgrid is going to be Identical to original grid
        self.splitgrid = []
        for i in range(0,16,self.row):
            self.splitgrid.append(self.newgrid[i:i+4])
         
        self.splittedLst = [] 
        self.truth_val = []
        #Collapse each row in the splitgrid. Then return it and append it to a new list.
        for row in self.splitgrid:
            rev = row[::-1]
            x = self.collapseRow(rev)
            rev2 = x[0]
            right = rev2[::-1]
            self.splittedLst.append(right)
            self.truth_val.append(x[1])
       #Set the cells now
        count = 0
        for i in range(0,4):
            for j in range(0,4):
                self.setCell(count,self.splittedLst[i][j])
                count +=1
        if True in self.truth_val:
            self.collapsed = True
            return True                  
        

        """
        This function should use collapseRow() to collapse all the rows
        in the grid to the RIGHT.

        This function should return True if any row of the grid is collapsed
        and False otherwise.
        """



    def collapseUp(self):
        
        self.mylist = []
        self.collapsed = False
        #first we want to get every value from the grid so we can perform manipulations on it.
        for i in range(0,16):
            self.mylist.append(self.getCell(i))
        #split my list by 4
        self.split = []
        for i in range(0,16,4):
                self.split.append(self.mylist[i:i+4])
        #Convert the splitted list into a list containing the columns
        self.colList = []
        for j in range(0,4):
            self.innerlist = []
            for i in range(0,4):
                self.innerlist.append(self.split[i][j])
            self.colList.append(self.innerlist)
        
        #Now Collapse the Column
        self.collapsedrow = []
        self.truth_val = []
        for row in self.colList:
            x = self.collapseRow(row)
            self.collapsedrow.append(x[0])
            self.truth_val.append(x[1])
            #set the cells back
        cell = 0
        for j in range(0,4):
            for i in range(0,4):
                self.setCell(cell,self.collapsedrow[i][j])
                cell+=1
        if True in self.truth_val:
            self.collapsed = True
            return True   


    def collapseDown(self):
        
        self.mylist = []
        self.collapsed = False
        #first we want to get every value from the grid so we can perform manipulations on it.
        for i in range(0,16):
            self.mylist.append(self.getCell(i))
        #split my list by 4
        self.split = []
        for i in range(0,16,4):
                self.split.append(self.mylist[i:i+4])
        #Convert the splitted list into a list containing the columns
        self.colList = []
        for j in range(0,4):
            self.innerlist = []
            for i in range(0,4):
                self.innerlist.append(self.split[i][j])
            self.colList.append(self.innerlist)
                                                                                                                                                                                               
        #now we must reverse then collapse the rows one by one.
       
        self.collapsedrow = []
        self.truth_val = []
        for row in self.colList:
            #reversed row
            self.rev = row[::-1]
            #collapse the reversed row
            x = self.collapseRow(self.rev)
            #get the row back from x and reverse it again
            self.rev2 = x[0]
            self.right = self.rev2[::-1]
            self.collapsedrow.append(self.right)
            self.truth_val.append(x[1])
            
        #set the cells back
        cell = 0
        for j in range(0,4):
            for i in range(0,4):
                self.setCell(cell,self.collapsedrow[i][j])
                cell+=1
        if True in self.truth_val:
            self.collapsed = True
            return True   
        
class Game():
    def __init__(self, row=4, col=4, initial=2):

        """
        Creates a game grid and begins the game
        """

        self.game = Grid(row, col, initial)
        self.play()


    def printPrompt(self):

        """
        Prints the instructions and the game grid with a move prompt
        """

        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")

        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')
            

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')


def main():
    game = Game()
    grid = Grid()
    grid.drawGrid()
    game.play()

main()
