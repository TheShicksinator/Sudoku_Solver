import pygame
import time
pygame.font.init()


class Board:
    grid = [[1, 0, 0, 0, 0, 0, 5, 6, 9],
            [4, 0, 2, 0, 0, 0, 0, 0, 8],
            [0, 5, 0, 0, 0, 9, 0, 4, 0],
            [0, 0, 0, 6, 4, 0, 8, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [2, 0, 8, 0, 3, 5, 0, 0, 0],
            [0, 4, 0, 5, 0, 0, 0, 1, 0],
            [9, 0, 0, 0, 0, 0, 4, 0, 2],
            [6, 2, 1, 0, 0, 0, 0, 0, 5]]

    def __init__(self, rows, columns, width, height, win):
        self.rows = rows
        self.columns = columns
        self.boxes = [[Box(self.grid[i][j], i, j, width, height)
                       for j in range(columns)] for i in range(rows)]
        self.width = width
        self.height = height
        self.current = None
        self.update()
        self.selected = None
        self.win = win

    def update(self):
        self.current = [[self.boxes[i][j].value for j in range(
            self.columns)] for i in range(self.rows)]

    def permSet(self, value):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set(value)
            self.update()

            if isValidMove(self.current, value, (row, col)) and self.solve():
                return True
            else:
                self.boxes[row][col].set(0)
                self.boxes[row][col].setTemp(0)
                self.update()
                return False

    def sketch(self, value):
        row, col = self.selected
        self.boxes[row][col].setTemp(value)

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap),
                             (self.width, i * gap), thickness)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0),
                             (i * gap, self.height), thickness)

        for i in range(self.rows):
            for j in range(self.columns):
                self.boxes[i][j].draw(self.win)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.columns):
                self.boxes[i][j].selected = False
        self.boxes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].setTemp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def isFinished(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.boxes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        empty = findEmpty(self.current)
        if not empty:
            return True
        else:
            row, col = empty

        for i in range(1, 10):
            if isValidMove(self.current, i, (row, col)):
                self.current[row][col] = i
                if self.solve():
                    return True
                self.current[row][col] = 0
        return False

    def solveGUI(self):
        self.update()
        empty = findEmpty(self.current)
        if not empty:
            return True
        else:
            row, col = empty

        for i in range(1, 10):
            if isValidMove(self.current, i, (row, col)):
                self.current[row][col] = i
                self.boxes[row][col].set(i)
                self.boxes[row][col].drawChange(self.win, True)
                self.update()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solveGUI():
                    return True
                self.current[row][col] = 0
                self.boxes[row][col].set(0)
                self.update()
                self.boxes[row][col].drawChange(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)
        return False


class Box:
    def __init__(self, value, row, column, width, height):
        self.value = value
        self.tempVal = 0
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont('comicsans', 40)
        boxDispSize = self.width // 9
        x = self.column * boxDispSize
        y = self.row * boxDispSize
        if self.value == 0 and self.tempVal != 0:
            text = font.render(str(self.tempVal), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (boxDispSize/2 - text.get_width()/2),
                     y + (boxDispSize/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0),
                             (x, y, boxDispSize, boxDispSize), 3)

    def drawChange(self, win, g=True):
        font = pygame.font.SysFont('comicsans', 40)
        boxDispSize = self.width // 9
        x = self.column * boxDispSize
        y = self.row * boxDispSize

        pygame.draw.rect(win, (255, 255, 255),
                         (x, y, boxDispSize, boxDispSize), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))

        win.blit(text, (x + (boxDispSize/2 - text.get_width()/2),
                 y + (boxDispSize/2 - text.get_height()/2)))

        if g:
            pygame.draw.rect(win, (0, 255, 0),
                             (x, y, boxDispSize, boxDispSize), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0),
                             (x, y, boxDispSize, boxDispSize), 3)

    def set(self, val):
        self.value = val

    def setTemp(self, val):
        self.tempVal = val


def findEmpty(grid):
    """finds the first empty location in grid"""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)
    return False


def isValidMove(grid, value, pos):
    """checks if value is valid"""
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == value and pos[1] != i:
            return False
    for i in range(len(grid)):
        if grid[i][pos[1]] == value and pos[0] != i:
            return False

    boxX = pos[1] // 3
    boxY = pos[0] // 3

    for i in range(boxY * 3, boxY * 3 + 3):
        for j in range(boxX * 3, boxX * 3 + 3):
            if grid[i][j] == value and (i, j) != pos:
                return False
    return True


def redraw(win, board, time, strikes):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont('comicsans', 40)
    text = font.render('Time: ' + timeFormat(time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    text = font.render('Strikes: ' + str(strikes), 1, (0, 0, 0))
    win.blit(text, (20, 560))
    board.draw()


def timeFormat(timeInSecs):
    m = timeInSecs // 60
    s = timeInSecs % 60
    h = m // 60
    formatted = " " + str(m) + ":" + str(s)
    return formatted


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption('Sudoku')
    board = Board(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        playTime = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.solveGUI()
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.boxes[i][j].tempVal != 0:
                        if board.permSet(board.boxes[i][j].tempVal):
                            print("Successful placement")
                        else:
                            print("Invalid placement")
                            strikes += 1
                        key = None
                        if board.isFinished():
                            print("Successful completion")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw(win, board, playTime, strikes)
        pygame.display.update()


main()
pygame.quit()
