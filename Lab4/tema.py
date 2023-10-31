import copy
from termcolor import colored
 
def getEmptyCells(board):
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0 or board[i][j] == -1:
                empty_cells.append((i, j))
    return empty_cells

def isComplete(board):
    for i in range(9):
        for j in range(9):
            if(board[i][j] == 0) or board[i][j] == -1:
                return False;
    return True;

def initializeDomain(board, row, col):
    if board[row][col] == 0:
        values = set(range(1, 10))
    elif board[row][col] == -1:
        values = [2, 4, 6, 8]

    updateDomain(board, row, col, values)

    return list(values)

def updateDomain(board, row, col, domain):
    # row
    for i in range(9):
        if board[row][i] in domain:
            domain.remove(board[row][i])

    # col
    for i in range(9):
        if board[i][col] in domain:
            domain.remove(board[i][col])

    # box check
    box_corner_row = (row // 3) * 3
    box_corner_col = (col // 3) * 3
    for i in range(box_corner_row, box_corner_row + 3):
            for j in range(box_corner_col, box_corner_col + 3):
                if board[i][j] in domain:
                    domain.remove(board[i][j])

def isAnyDomainEmpty(domain, empty_cells):
    for cell in empty_cells:
        if(len(domain[cell])) == 0:
            return False;

    return True;

def forwardChecking(board, empty_cells, domain):
    new_domain = copy.deepcopy(domain)
    for cell in empty_cells:
        row, col = cell
        values = new_domain[(row, col)]
        
        updateDomain(board, row, col, values)

        new_domain[(row, col)] = values
    return new_domain

def mrv(empty_cells, domain):
    min_cell = None
    min_values = float('inf')
    for cell in empty_cells:
        values = domain[cell]
        if len(values) < min_values:
            min_cell = cell
            min_values = len(values)
    return min_cell

def solve(board, empty_cells, domain):
    if isComplete(board) == True:
        return board
    
    current_cell = mrv(empty_cells, domain)
    values = domain[current_cell]
    for value in values:
        new_board = copy.deepcopy(board)
        new_board[current_cell[0]][current_cell[1]] = value
        new_empty_cells = empty_cells.copy()
        new_empty_cells.remove(current_cell)
        new_domain = forwardChecking(new_board, new_empty_cells, domain)
        if isAnyDomainEmpty(new_domain, new_empty_cells) == True:
            result = solve(new_board, new_empty_cells, new_domain)
            if result:
                return result
    return None

def initialize(board):
    empty_cells = getEmptyCells(board)
    domain = {}
    for cell in empty_cells:
        domain[cell] = initializeDomain(board, cell[0], cell[1])
    
    return empty_cells, domain

colored_cells = []

def printSudoku(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            if board[i][j] == -1:
                print(colored("x", "red"), end=" ")
                colored_cells.append((i, j))
            elif (i, j) in colored_cells:
                print(colored(board[i][j], "red"), end=" ")
            else:
                print(f"{board[i][j]}", end=" ")
        print()
    print()

initial_board = [
    [ 8,  4,  0,  0,  5,  0, -1,  0,  0],
    [ 3,  0,  0,  6,  0,  8,  0,  4,  0],
    [ 0,  0, -1,  4,  0,  9,  0,  0, -1],
    [ 0,  2,  3,  0, -1,  0,  9,  8,  0],
    [ 1,  0,  0, -1,  0, -1,  0,  0,  4],
    [ 0,  9,  8,  0, -1,  0,  1,  6,  0],
    [-1,  0,  0,  5,  0,  3, -1,  0,  0],
    [ 0,  3,  0,  1,  0,  6,  0,  0,  7],
    [ 0,  0, -1,  0,  2,  0,  0,  1,  3]
]

print("Initial sudoku:")
printSudoku(initial_board)

empty_cells, domain = initialize(initial_board)
solution = solve(initial_board, empty_cells, domain)

if solution:
    print("Solved sudoku:")
    printSudoku(solution)
else:
    print("No solution.")