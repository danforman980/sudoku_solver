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
    if row < 4:
        x = 0
    elif row <7:
        x = 3
    else:
        x = 6
    if col < 4:
        y = 0
    elif col <7:
        y = 3
    else:
        y = 6
       
    for i in range(0,2):
        for j in range(0,2):
            if(board[x + i][y + j] == number):
                return False
    return True
           
def validpos(board, row, col, number):
    if rowcheck(board, row, number):
        if vertcheck(board, col, number):
            if boxcheck(board, row, col, number):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

               
def empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return "complete"


def sudoku_solver(bc):
    if empty(bc) == "complete":
        return True
    else:
        row, col = empty(bc)
    for i in range (1,10):
        if validpos(bc, row, col, i):
            bc[row][col] = i
            print("\n", bc)
            if sudoku_solver(bc):
                return True
            bc[row][col] = 0
    return False
