#This file is used for reading and writing from the txt file

import clipboard

#saves the currently displayed board
def saveBoard(b, index):

    code = boardToCode(b)
    FILE = open("text.txt", "r+")
    
    indents = index
    while indents > 0:
        char = FILE.read(1)
        if not char: break
        if char == '\n':
            indents -= 1
    FILE.seek(FILE.tell())
    FILE.write(code)
    FILE.close()


#takes an index and loads that board
def loadBoard(boards, index):

    FILE = open("text.txt", "r")
    lines = FILE.readlines()
    codeToBoard(boards, lines[index][0:-1])
    FILE.close()


#takes the code on the users clipboard and saves it in the slot
def clipToSlot(index):
    
    code = clipboard.paste()
    clipMatch = False

    for n in range(1):

        if not (len(code) == 86):
            break
        
        clipMatch = True

        for i in code:
            try:
                (ord(i))
            except:
                clipMatch = False
                break
            else:
                if not (0 <= (ord(i) -33) < 64):
                    clipMatch = False
                    break

    if clipMatch:
        FILE = open("text.txt", "r+")
    
        indents = index
        n = 0
        while indents > 0:
            if FILE.read(1) == '\n':
                indents -= 1
            n += 1
        
        FILE.seek(FILE.tell())
        FILE.write(code)
        FILE.close()


#copies the board onto their clipboard
def slotToClip(index):

    FILE = open("text.txt", "r")
    lines = FILE.readlines()
    FILE.close()
    
    clipboard.copy(lines[index][0:-1])


#takes the current board and returns a code
def boardToCode(b):

    binList = []
    for i in range(16):
        for j in range(16):
            if b.board[i][j].mine:
                binList += [1]
            else:
                binList += [0]
    
    for i in range(16):
        for j in range(16):
            if b.board[i][j].cover == 'o':
                binList += [1]
            else:
                binList += [0]
    
    code = ""
    n = 1
    digit = 0
    for m in binList:
        digit += m * (2**(n-1))  
        n += 1
        if n > 6:
            n = 1
            code += chr(digit + 33)
            digit = 0
    if (n!=1): code += chr(digit + 33)


    return code


#takes a code and inserts it directly into the board
def codeToBoard(b, code):
    
    binList = []
    for i in range(86):
        n = ord(code[i]) - 33
        for j in range(6):
            binList += [n%2]
            n = n // 2

    b.reset()
    b.blank = False
    
    index = 0
    for i in range(16):
        for j in range(16):
            if binList[index] == 1:
                b.board[i][j].addMine()
            index += 1
    
    for i in range(16):
        for j in range(16):
            if binList[index] == 1:
                b.board[i][j].cover = 'o'
            index += 1
