# text solver

def printGrid(grid):
    """prints the grid"""
    for row in grid:
        print(row, end='\n')


def findEmpty(grid, location):
    """finds the first empty location in grid"""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                location[0] = i
                location[1] = j
                return True
    return False


def alreadyInRow(grid, row, value):
    """checks if value is already in row"""
    for i in range(9):
        if grid[row][i] == value:
            return True
    return False


def alreadyInColumn(grid, column, value):
    """checks if value is already in column"""
    for i in range(9):
        if grid[i][column] == value:
            return True
    return False


def alreadyInBox(grid, row, column, value):
    """checks if value is already in box"""
    for i in range(3):
        for j in range(3):
            if grid[row + i][column + j] == value:
                return True
    return False


def isValidMove(grid, row, column, value):
    """checks if value is valid"""
    return not (alreadyInRow(grid, row, value) or
                alreadyInColumn(grid, column, value) or
                alreadyInBox(grid, row - row % 3, column - column % 3, value))


def solve(grid):
    """solves the grid"""
    location = [0, 0]
    if not findEmpty(grid, location):
        return True
    row = location[0]
    column = location[1]
    for i in range(1, 10):
        if isValidMove(grid, row, column, i):
            grid[row][column] = i
            if solve(grid):
                return True
            grid[row][column] = 0
    return False


if __name__ == '__main__':
    grid = [[1, 0, 0, 0, 0, 0, 5, 6, 9],
            [4, 0, 2, 0, 0, 0, 0, 0, 8],
            [0, 5, 0, 0, 0, 9, 0, 4, 0],
            [0, 0, 0, 6, 4, 0, 8, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [2, 0, 8, 0, 3, 5, 0, 0, 0],
            [0, 4, 0, 5, 0, 0, 0, 1, 0],
            [9, 0, 0, 0, 0, 0, 4, 0, 2],
            [6, 2, 1, 0, 0, 0, 0, 0, 5]]
    printGrid(grid)
    print('Attempting to solve...')
    if solve(grid):
        print('Solution:')
        printGrid(grid)
    else:
        print('No solution found')
