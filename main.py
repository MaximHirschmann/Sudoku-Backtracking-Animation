import pygame
import sys
from copy import deepcopy
from random import randrange
import time

class Game():
    def __init__(self):
        pygame.init()
        self.methods = [
            "Backtracking",
            "Dynamic"
        ]
        self.texts = [
            """   Backtracking with Brute Force
            
            Starting with the first free square, 
            you try systematically, starting with the number one, 
            whether you come to a solution. At the first 
            contradiction you backtrack. This solution can be 
            formulated very elegantly recursively and you can be sure 
            that all possible combinations are searched. 
            Since there can be thousands of ways, 
            this algorithm is only suitable for computer programs. 
            However, the solution algorithm is not the fastest, 
            since it does not use any analytical preliminary information and 
            only proceeds by trial and error. 
            It therefore uses numbers with brute force and then checks them. 
            Nevertheless, even for difficult 9×9 Sudokus on ordinary PCs, 
            the solution is usually obtained quickly. 
            The program runtime depends on the number of digits. 
            The order in which the fields are filled also influences the program runtime. 
            For larger Sudokus, however, 
            this method quickly reaches its limits.
            """
            ,
            """
            Backtracking with dynamic order

            You can modify the backtracking method to 
            dynamically generate the processing order of the fields. 
            Instead of filling the first free field, 
            you determine the one with the least number of candidates 
            and start there with the experimental insertion. 
            This reduces the effort to approximately linear runtime, 
            because in practice (even with difficult Sudokus) 
            there is almost always a field for which only one number is possible. 
            Since the order in which the fields are filled is not fixed, 
            the current state must be saved at each step 
            to be able to reproduce it later. 
            The animation is deliberately slowed down.
            """
        ]
        self.methodIndex = 1
        self.method = self.methods[self.methodIndex]
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.loadSudokus()
        self.indexSudokus = randrange(len(self.sudokus))
        self.initial = deepcopy(self.sudokus[self.indexSudokus])
        screenInfo = pygame.display.Info()
        self.width = screenInfo.current_w
        self.height = screenInfo.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Sudoku Backtracking")
        self.currentlySelected = ()
        smallest = min(self.width, self.height)
        self.padding1 = smallest//30
        self.padding2 = smallest//30
        self.boardSize = self.height-2*self.padding1
        self.third = self.boardSize//3
        self.cellLength = (self.boardSize-6*self.padding2)//9
        self.lineThicknessFactor = 80
        self.lineThickness = max((self.boardSize - 6*self.padding2)//(3*self.lineThicknessFactor), 1)
        self.fact1 = self.padding1 + self.padding2 + self.lineThickness
        buttonAreaWidth = self.width - self.height
        self.buttSolve = pygame.Rect(
            0,
            0,
            buttonAreaWidth//4,
            self.height//12
        )
        self.buttNext = pygame.Rect(
            0,
            0,
            buttonAreaWidth//4,
            self.height//12
        )
        self.button1 = pygame.Rect(0, 0, self.height//12, self.height//12)
        self.button2 = pygame.Rect(0, 0, self.height//12, self.height//12)
        self.font = pygame.font.SysFont("Helvetica", self.height//18)
        self.fontSmall = pygame.font.SysFont("Helvetica", self.height//40)
        self.colorBackground = 33, 33, 33
        self.colorLines = 191, 191, 191
        self.colorSelected = 77, 77, 77
        self.colorFont = 191, 191, 191
        self.colorFontDark = self.colorBackground
        self.colorInitial = 59, 59, 59
        self.colorButton = 232, 135, 245
        self.numsRendered = {i: self.font.render(str(i), True, self.colorFont) for i in range(1, 10)}
        self.loadSudokus()

    def onResize(self, size):
        a, b = size
        # proportion of 12:9 or wider
        if a*9 >= b*12:
            pygame.display.set_mode(size, pygame.RESIZABLE)
            self.width, self.height = size
            self.padding1 = self.height//30
            self.padding2 = self.height//40
            self.font = pygame.font.SysFont("Helvetica", self.height//18)
            self.fontSmall = pygame.font.SysFont("Helvetica", self.height//40)
            self.numsRendered = {i: self.font.render(str(i), True, self.colorFont) for i in range(1, 10)}
            buttonAreaWidth = self.width - self.height
            self.buttSolve = pygame.Rect(
                0,
                0,
                buttonAreaWidth//4,
                self.height//12
            )
            self.buttNext = pygame.Rect(
                0,
                0,
                buttonAreaWidth//4,
                self.height//12
            )
            self.button1 = pygame.Rect(0, 0, self.height//12, self.height//12)
            self.button2 = pygame.Rect(0, 0, self.height//12, self.height//12)
            self.boardSize = self.height-2*self.padding1
            self.third = self.boardSize//3
            self.cellLength = (self.boardSize-6*self.padding2)//9
            self.lineThickness = max((self.boardSize - 6*self.padding2)//(3*self.lineThicknessFactor), 1)
            self.fact1 = self.padding1 + self.padding2 + self.lineThickness
            self.setup()

    """ Draws grid from point p1 left-top to p2 bottom-right on screen """
    def drawGrid(self, p1, p2):
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]
        for i in range(2):
            pygame.draw.line(
                self.screen,
                self.colorLines,
                (width*(i+1)/3 + p1[0], p1[1]),
                (width*(i+1)/3 + p1[0], p2[1]),
                max(width//self.lineThicknessFactor, 1) # linesize
            )
            pygame.draw.line(
                self.screen,
                self.colorLines,
                (p1[0], height*(i+1)/3 + p1[1]),
                (p2[0], height*(i+1)/3 + p1[1]),
                max(width//self.lineThicknessFactor, 1) # linesize
            )

    def setup(self):
        pygame.init()
        self.screen.fill(self.colorBackground)
        padding1 = self.padding1
        padding2 = self.padding2
        cellLength = self.cellLength

        self.lineThickness = max((self.boardSize - 6*padding2)//(3*self.lineThicknessFactor), 1)
        # draw currently selected
        if self.currentlySelected:
            bigPos = self.currentlySelected[0]//3, self.currentlySelected[1]//3
            smallPos = self.currentlySelected[0]%3, self.currentlySelected[1]%3
            
            self.currentRect = pygame.Rect(
                padding1 + bigPos[0]*self.boardSize//3 + smallPos[0]*cellLength + padding2 + self.lineThickness,
                padding1 + bigPos[1]*self.boardSize//3 + smallPos[1]*cellLength + padding2 + self.lineThickness,
                cellLength - self.lineThickness,
                cellLength - self.lineThickness
            )
            pygame.draw.rect(
                self.screen,
                self.colorSelected, 
                self.currentRect
            )
        # draw thick lines
        topLeft = (padding1, padding1)
        bottomright = (padding1+self.boardSize, padding1+self.boardSize)
        self.drawGrid(
            topLeft,
            bottomright
        )
        # draw thin lines
        for i in range(3):
            for j in range(3):
                topLeft2 = (padding1 + self.boardSize*i//3 + padding2, padding1 + self.boardSize*j//3 + padding2)
                bottomright2 = (padding1 + self.boardSize*(i+1)//3 - padding2, padding1 + self.boardSize*(j+1)//3 - padding2)
                self.drawGrid(
                    topLeft2,
                    bottomright2
                )
        # draw nums
        for i in range(3):
            for j in range(3):
                topLeft = (
                    padding1 + j * self.boardSize//3,
                    padding1 + i * self.boardSize//3
                )
                for k in range(3):
                    for l in range(3):
                        if self.board[i*3+k][j*3+l]:
                            topLeft2 = (
                                topLeft[0] + l * cellLength + padding2,
                                topLeft[1] + k * cellLength + padding2
                            )
                            txt = self.numsRendered[self.board[i*3+k][j*3+l]]
                            txtRect = txt.get_rect(center = (topLeft2[0] + cellLength//2, topLeft2[1] + cellLength//2))
                        elif self.initial[i*3+k][j*3+l]:
                            topLeft2 = (
                                topLeft[0] + l * cellLength + padding2 + self.lineThickness,
                                topLeft[1] + k * cellLength + padding2 + self.lineThickness
                            )
                            pygame.draw.rect(
                                self.screen,
                                self.colorInitial,
                                (
                                    topLeft2[0],
                                    topLeft2[1],
                                    cellLength - self.lineThickness,
                                    cellLength - self.lineThickness
                                )
                            )
                            txt = self.numsRendered[self.initial[i*3+k][j*3+l]]
                            txtRect = txt.get_rect(center = (topLeft2[0] + cellLength//2, topLeft2[1] + cellLength//2))
                        else:
                            continue
                        self.screen.blit(txt, txtRect)

        buttonAreaWidth = self.width - self.height
        for i, line in enumerate(self.texts[self.methodIndex].split("\n")):
            movesurface = self.fontSmall.render(line, True, self.colorFont)
            textRect = movesurface.get_rect(center = (self.height + buttonAreaWidth//2, self.height*(i+1)//30))
            self.screen.blit(movesurface, textRect)

        self.buttSolve.center = (self.boardSize + 2*padding1 + buttonAreaWidth*2//3, self.height*9//12)
        pygame.draw.rect(self.screen, self.colorButton, self.buttSolve)
        movesurface = self.font.render("Solve", True, self.colorFontDark)
        textRect = movesurface.get_rect(center = self.buttSolve.center)
        self.screen.blit(movesurface, textRect)

        self.buttNext.center = (self.boardSize + 2*padding1 + buttonAreaWidth//3, self.height*9//12)
        pygame.draw.rect(self.screen, self.colorButton, self.buttNext)
        movesurface = self.font.render("Next", True, self.colorFontDark)
        textRect = movesurface.get_rect(center = self.buttNext.center)
        self.screen.blit(movesurface, textRect)

        movesurface = self.font.render("Method:", True, self.colorFont)
        textRect = movesurface.get_rect(center = (self.boardSize + 2*padding1 + buttonAreaWidth//3, self.height*11//12))
        self.screen.blit(movesurface, textRect)

        #self.button1.center = (self.boardSize + 2*padding1 + buttonAreaWidth*2//3, self.height*11//12)
        self.button1.right = self.boardSize + 2*padding1 + buttonAreaWidth*2//3 - padding2
        self.button1.centery = self.height*11//12
        color = self.colorButton if self.methodIndex == 0 else self.colorInitial
        pygame.draw.rect(self.screen, color, self.button1)
        movesurface = self.font.render("1", True, self.colorFontDark)
        textRect = movesurface.get_rect(center = self.button1.center)
        self.screen.blit(movesurface, textRect)
        #self.button2.center = (self.boardSize + 2*padding1 + buttonAreaWidth*5//6, self.height*11//12)
        self.button2.left = self.boardSize + 2*padding1 + buttonAreaWidth*2//3 + padding2
        self.button2.centery = self.height*11//12
        color = self.colorButton if self.methodIndex == 1 else self.colorInitial
        pygame.draw.rect(self.screen, color, self.button2)
        movesurface = self.font.render("2", True, self.colorFontDark)
        textRect = movesurface.get_rect(center = self.button2.center)
        self.screen.blit(movesurface, textRect)
        pygame.display.update()

    def getCoordinates(self, pos):
        padding1 = self.padding1
        padding2 = self.padding2
        third = self.boardSize//3
        cellLength = (third - 2*padding2)//3
        if padding1 <= pos[0] <= self.boardSize+padding1 and padding1 <= pos[1] <= self.boardSize+padding1:
            x, y = pos[0]-padding1, pos[1]-padding1
            divX = x // third
            divY = y // third
            modX = x % third
            modY = y % third
            if padding2 <= modX <= 3*cellLength + padding2 and padding2 <= modY <= 3*cellLength + padding2:
                modX -= padding2
                modY -= padding2
                return (divX*3 + modX//cellLength, divY*3 + modY//cellLength)
        return None

    def setMethod(self, to):
        self.methodIndex = to
        self.method = self.methods[self.methodIndex]
        self.setup() 

    def click(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                        pygame.quit
                        sys.exit()
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        if self.currentlySelected:
                            i, j = self.currentlySelected
                            self.board[j][i] = int(event.unicode)
                            self.updateCell(int(event.unicode), j, i)
                    elif pygame.K_BACKSPACE == event.key:
                        if self.currentlySelected:
                            i, j = self.currentlySelected
                            self.board[j][i] = 0
                            self.updateCell(0, j, i)
                elif event.type == pygame.VIDEORESIZE:
                    size = event.size
                    self.onResize(size)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.buttSolve.collidepoint(pos):
                        self.solve(method=self.method)
                    elif self.buttNext.collidepoint(pos):
                        self.loadNext()
                    elif self.button1.collidepoint(pos):
                        self.setMethod(0)
                    elif self.button2.collidepoint(pos):
                        self.setMethod(1)
                    else:
                        coordinates = self.getCoordinates(pos)
                        if coordinates:
                            if not self.initial[coordinates[1]][coordinates[0]]:
                                self.currentlySelected = coordinates
                            else:
                                self.currentlySelected = None
                            self.setup()

    def updateCell(self, num, y, x):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    pygame.quit
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
        x1, x2 = divmod(x, 3)
        y1, y2 = divmod(y, 3)
        topLeft = (
            x1*self.third + x2*self.cellLength + self.fact1,
            y1*self.third + y2*self.cellLength + self.fact1,
        )
        if self.currentlySelected == (x, y):
            color = self.colorSelected
        else:
            color = self.colorBackground
        pygame.draw.rect(
            self.screen,
            color,
            (
                topLeft[0],
                topLeft[1],
                self.cellLength - self.lineThickness,
                self.cellLength - self.lineThickness,
            )
        )
        if num:
            txt = self.numsRendered[num]
            txtRect = txt.get_rect(center = (topLeft[0] + self.cellLength//2, topLeft[1] + self.cellLength//2))
            self.screen.blit(txt, txtRect)
        pygame.display.update()

    def solve(self, method = "Backtracking"):
        start = time.time()
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.currentlySelected = None
        self.setup()
        board = deepcopy(self.initial)
        if method == "Backtracking":
            res = self.solveBacktracking(board, 0, 0)
        else:
            candidates = [[[k for k in range(1, 10) if self.isValid(board, k, i, j)] if board[i][j] == 0 else None for j in range(len(board[i])) ] for i in range(len(board))]
            res = self.solveDynamic(board, candidates)
        if res:
            for i in range(9):
                for j in range(9):
                    if not self.initial[i][j]:
                        self.board[i][j] = board[i][j]
            self.setup()
        print(time.time()-start)

    def solveDynamic(self, board, candidates):
        time.sleep(0.1)
        countFilled = 0
        smallest = float("inf")
        smallestInd = 0
        for i in range(9):
            for j in range(9):
                if candidates[i][j] == None:
                    countFilled += 1
                elif len(candidates[i][j]) == 0:
                    return False
                elif len(candidates[i][j]) < smallest:
                    smallest = len(candidates[i][j])
                    smallestInd = (i, j)
        if countFilled == 81:
            return board
        i, j = smallestInd
        for candidate in candidates[i][j]:
            newCand = self.newCandidates(deepcopy(candidates), candidate, i, j)
            newCand[i][j] = None
            board[i][j] = candidate
            self.updateCell(candidate, i, j)
            res = self.solveDynamic(board, newCand)
            if res:
                return res
            board[i][j] = 0
            self.updateCell(0, i, j)

    def newCandidates(self, candidates, candidate, i, j):
        for k in range(9):
            try:
                candidates[i][k].remove(candidate)
            except:
                pass
            try:
                candidates[k][j].remove(candidate)
            except:
                pass
        # 3x3 field
        i = i//3
        j = j//3
        for k in range(3):
            for l in range(3):
                try:
                    candidates[3*i+k][3*j+l].remove(candidate)
                except:
                    pass
        return candidates

    def solveBacktracking(self, board, y, x):
        if y == 9:
            return board
        if board[y][x]:
            x += 1
            y += x//9
            x = x%9
            return self.solveBacktracking(board, y, x)

        for num in range(10):
            if self.isValid(board, num, y, x):
                self.updateCell(num, y, x)
                board[y][x] = num
                newX = x + 1
                newY = y + newX//9
                newX = newX%9
                res = self.solveBacktracking(board, newY, newX)
                if res:
                    return res
                board[y][x] = 0
                self.updateCell(0, y, x)
        return False

    def isValid(self, board, num, y, x):
        for i in range(9):
            if board[y][i] == num or board[i][x] == num:
                return False
        y = 3*(y//3)
        x = 3*(x//3)
        for i in range(3):
            for j in range(3):
                if board[y+i][x+j] == num:
                    return False
        return True

    def loadSudokus(self):
        sudokus = []
        with open("sudokus.txt", "r") as f:
            sudoku = []
            lines = f.readlines()
            count = 0
            for line in lines:
                for char in line:
                    if char == ".":
                        num = 0
                    elif "0" < char <= "9":
                        num = int(char)
                    else:
                        continue
                    if count % 9 == 0:
                        if count == 81:
                            sudokus.append(sudoku)
                            sudoku = []
                            count = 0
                        sudoku.append([])
                    sudoku[-1].append(num)
                    count += 1
        self.sudokus = sudokus

    def loadNext(self):
        newIndex = self.indexSudokus
        while newIndex == self.indexSudokus:
            newIndex = randrange(len(self.sudokus))
        self.indexSudokus = newIndex
        self.initial = self.sudokus[newIndex]
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.setup()

    def play(self):
        self.setup()
        while True:
            self.click()
            self.setup()


if __name__ == "__main__":
    Game().play()