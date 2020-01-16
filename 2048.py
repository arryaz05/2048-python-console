import random
import os
import keyboard

# Colors
class bcolors:
    Red          = "\033[31m"
    Green        = "\033[32m"
    Yellow       = "\033[33m"
    Blue         = "\033[34m"
    Magenta      = "\033[35m"
    Cyan         = "\033[36m"
    LightGray    = "\033[37m"
    DarkGray     = "\033[90m"
    LightRed     = "\033[91m"
    LightGreen   = "\033[92m"
    LightYellow  = "\033[93m"
    LightBlue    = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan    = "\033[96m"
    White        = "\033[97m"

def coloured(val):
    colouring = {
        0: bcolors.LightGray + str(val) + bcolors.White,
        2: bcolors.LightGreen + str(val) + bcolors.White,
        4: bcolors.LightBlue + str(val) + bcolors.White,
        8: bcolors.LightRed + str(val) + bcolors.White,
        16: bcolors.LightMagenta + str(val) + bcolors.White,  
        32: bcolors.LightYellow + str(val) + bcolors.White,    
        64: bcolors.LightRed + str(val) + bcolors.White,    
        128: bcolors.Green + str(val) + bcolors.White,
        256: bcolors.Cyan + str(val) + bcolors.White,
        512: bcolors.Magenta + str(val) + bcolors.White,    
        1024: bcolors.Red + str(val) + bcolors.White,  
        2048: bcolors.Blue + str(val) + bcolors.White,          
    }
    return colouring[val]

# Key Listener
def keyListener():
    while True:
        keystroke = keyboard.read_key()
        if keystroke == "a":
            board.__swipeLeft__()
            board.__print__()
        elif keystroke == "d":
            board.__swipeRight__()
            board.__print__()
        elif keystroke == "w":
            board.__swipeUp__()
            board.__print__()
        elif keystroke == "s":
            board.__swipeDown__()
            board.__print__()

def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def mergeLeft(row):
    for idx, value in enumerate(row):
        if idx == len(row) - 1:
            pass
        else:
            if value == row[idx + 1]:
                row[idx] = value * 2
                row[idx + 1] = 0
                board.__addScore__(value * 2)

def collapseLeft(row):
    zeros = 0
    while 0 in row:
        row.remove(0)
        zeros += 1
    for i in range(zeros):
        row.append(0)

def moveLeft(row):
    collapseLeft(row)
    mergeLeft(row)
    collapseLeft(row)

def moveRight(row):
    row.reverse()
    collapseLeft(row)
    mergeLeft(row)
    collapseLeft(row)
    row.reverse()

def spawnTwo(mat):
    aux = []
    for i, col in enumerate(mat):
        for j, col in enumerate(mat[i]):
            if mat[i][j] == 0:
                aux.append((i,j))
    if not aux:
        return False
    else:
        new = random.choice(aux)
        mat[new[0]][new[1]] = 2
        return True

def printUpperBorder(size):
    upper_border = bcolors.DarkGray + '╔'
    for i in range(size):
        if i != size-1:
            upper_border += '═════╦'
        else:
            upper_border += '═════╗'
    print(upper_border) 

def printLowerBorder(size):
    lower_border = bcolors.DarkGray + '╚'
    for i in range(size):
        if i != size-1:
            lower_border += '═════╩'
        else:
            lower_border += '═════╝'
    print(lower_border + '\n') 

def printInnerBorder(size):
    inner_border = bcolors.DarkGray + '╠'
    for i in range(size):
        if i != size-1:
            inner_border += '═════╬'
        else:
            inner_border += '═════╣'
    print(inner_border) 

def printBody(mat, size):
    for idx, row in enumerate(mat):
        str_row = bcolors.DarkGray + '║'
        for i, val in enumerate(row):
            digits = len(str(row[i]))
            spaces = 5
            for j in range(digits):
                spaces -= 1
            for j in range(spaces):
                str_row = str_row + ' '
            str_row = str_row + coloured(val) + bcolors.DarkGray + '║'
        print(str_row)
        if idx != size-1:
            printInnerBorder(size)



class Board:
    # Initialize Board with two 2's randomly placed
    def __init__(self, size):
        self.rows = [[0 for x in range(size)] for y in range(size)] 
        firstTwo = (random.randint(0,size-1), random.randint(0,size-1))
        while True:
            secondTwo = (random.randint(0,size-1), random.randint(0,size-1))
            if secondTwo != firstTwo:
                break
        self.rows[ firstTwo[0] ] [firstTwo[1]] = 2
        self.rows[ secondTwo[0] ] [secondTwo[1]] = 2
        self.score = 0
        self.size = size
    
    # Print Board
    def __print__(self):
        os.system('cls')
        printUpperBorder(self.size)
        printBody(self.rows, self.size)
        printLowerBorder(self.size)
        print(f'Score: {self.score}' + '\n')

    # Swipe LEFT
    def __swipeLeft__(self):
        moved = False
        for row in self.rows:
            aux = row.copy()
            moveLeft(row)
            if aux != row:
                moved = True
        if moved == True:
            if spawnTwo(self.rows) == False:
                print('Game Over')

    # Swipe RIGHT
    def __swipeRight__(self):
        moved = False
        for row in self.rows:
            aux = row.copy()
            moveRight(row)
            if aux != row:
                moved = True
        if moved == True:
            if spawnTwo(self.rows) == False:
                print('Game Over')

    # Swipe UP
    def __swipeUp__(self):
        moved = False
        self.rows = transpose(self.rows)
        for row in self.rows:
            aux = row.copy()
            moveLeft(row)
            if aux != row:
                moved = True
        self.rows = transpose(self.rows)
        if moved == True:
            if spawnTwo(self.rows) == False:
                print('Game Over')

    # Swipe UP
    def __swipeDown__(self):
        moved = False
        self.rows = transpose(self.rows)
        for row in self.rows:
            aux = row.copy()
            moveRight(row)
            if aux != row:
                moved = True
        self.rows = transpose(self.rows)
        if moved == True:
            if spawnTwo(self.rows) == False:
                print('Game Over')
    
    # Set Score
    def __addScore__(self, score):
        self.score += score


os.system('cls')
size = input('Insert board size: ')
board = Board(int(size))
board.__print__()
keyListener()