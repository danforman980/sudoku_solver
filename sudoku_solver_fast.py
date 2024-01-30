import math as math

#checks to identify if a number is already present in a row, column or box
def rowcheck(board, row, number):
    for i in range(0,9):
        if (board[row][i] == number):
            return False 
    return True

def vertcheck(board, col, number):
    for i in range(0,9):
        if (board[i][col] == number):
            return False
    return True
    
def boxcheck(board, row, col, number):
    
    x = (math.floor(row/3))*3
    y = (math.floor(col/3))*3
        
    for i in range(0,3):
        for j in range(0,3):
            if(board[x + i][y + j] == number):
                return False
    return True

#checks to identify if a number can be placed at a specific position 
#it does this by checking if the number is present in all three possible value lists for row, column and box
def validpos(board, row, col, posval_row, posval_col, posval_box, number):
    if number in posval_row[row]:
        if number in posval_col[col]:
            if number in posval_box[math. floor(row/3), math. floor(col/3)]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

#intial check to see if the board being solved is valid
#ie whether any contradictions are present in locations that do not contain an empty
#this is needed as the backtracking algorithm does not check any spaces that are empty
def validboard(board):
            
    for z in range (3):
        for x in range (3):
            i = (z*3)+x
            values1 = []
            values2 = []
            values3 = []
            for c in range (3):
                for v in range (3):
                    j = (c*3)+v
                    a = x*3+v 
                    b = z*3+c
                    if board[i][j] != 0:
                        values1.append(board[i][j])
                    if board[j][i] != 0:
                        values2.append(board[j][i])   
                    if board[a][b] != 0:
                        values3.append(board[a][b])
      
                    if len(values1) != len(set(values1)) or len(values2) != len(set(values2)) or len(values3) != len(set(values3)):
                        return False
            
    return True

#function to find the amount of other empty states each empty state affects (constraints)
def getaffected(board, row, col):
    
    aff = 0
    
    x = (math.floor(row/3))*3
    y = (math.floor(col/3))*3
        
    for i in range(0,3):
        for j in range(0,3):

            z = (i*3)+j
  
            if (board[z][y] == 0):
                aff +=1
            if (board[x][z] == 0):
                aff +=1
            if board[x + i][y + j] != 0:
                aff +=1
    return aff

#backtracking algorithm that takes in the board copy (bc), the three columns detemining possible values
#and the values needing to be checked at each position (checked)
def solver(bc, posval_row, posval_col, posval_box, checked, affected):

    store = {}
    #checked if the sudoku has been solved 
    if not checked:
        return True
    else:
        #ordering the positions by fewest possible options and trying these first
        #for the values with the minimum number options, finding the empty state affecting the most other empty states
        z = len(checked[min(checked, key=lambda k: len(checked[k]))])
        
        for l in checked:
            if len(checked[l]) == z:
                g, h = l
                store[l] = affected[g, h]
                
        row, col = min(store, key=lambda k: store[k])  
                
        #getting these values and then updating the possible values for this position in case any have been used
        #This behaves as a forward check, as if no values are present the function will return false
            
        checked[row,col] = list(set(posval_row[row]).intersection(posval_col[col], posval_box[math.floor(row/3), math.floor(col/3)]))
        #holding the value in case we need to backtrack to this state and add them again to the possible values
        temphold =  checked[row, col]      
    #looping through the possible values for this position  
    for i in checked[row,col]:
        #setting the empty state to the value being tried
        bc[row][col] = i 
            
        #removing the value from the possible  values lists
        posval_row[row].remove(i)
        posval_col[col].remove(i)
        posval_box[math.floor(row/3), math.floor(col/3)].remove(i)
            
        #removing the checked position value 
            
        del checked[(row, col)]
        
        #applying the backtrack

        if solver(bc, posval_row, posval_col, posval_box, checked, affected): 
            return True
         
        #reverting the changes made if the attempt is a dead end 
        bc[row][col] = 0
        checked[row, col] = temphold 
        posval_row[row].append(i)  
        posval_col[col].append(i) 
        posval_box[math.floor(row/3), math.floor(col/3)].append(i) 
        
    return False

def sudoku_solver(sudoku):
    
    #making a copy of the sudoku board
    solved = np.copy(sudoku)
    
    #creating the dictionaries for use in the algorithm
    posval_row = {}
    posval_col = {}
    posval_box = {}
    values = {}
    affected = {}
    
    #finding the intial possible values for each row, column and box and adding the values to the array
    for z in range (3):
        for x in range (3):
            i = (z*3)+x
            posval_row[i] = []
            posval_col[i] = []
            posval_box[z,x] = []
            
            for n in range(1,10):
                a = z*3
                b = x*3
                
                if rowcheck(solved, i, n):
                    posval_row[i].append(n)

                if vertcheck(solved, i, n):
                    posval_col[i].append(n)

                if boxcheck(solved, a, b, n):
                    posval_box[z,x].append(n)

    #calculating the possible values at each empty space
    #calculating the amount of constraints at each empty space
    for row in range(0,9):
        for col in range(0,9):
            if sudoku[row][col] == 0:
                values[row,col] = list(set(posval_row[row]).intersection(posval_col[col], posval_box[math.floor(row/3), math.floor(col/3)]))
                affected[row,col] = getaffected(sudoku, row, col)
        
    #valid board check
    if not validboard(solved):
        solvable = False
    #starting the algorithm if the board is valid
    else:
        solvable = solver(solved, posval_row, posval_col, posval_box, values, affected)
    #if the board isnt solvable returning the board with -1. at every spot.
    if not solvable:
        solved.fill(-1.)
        
    
    sudoku_solver = solved
    return sudoku_solver
