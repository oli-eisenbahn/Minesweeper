#this file handles the board and tiles within the board

import random

#class to represent the board
class Board:
    
    def __init__(this, pos, size, mines, button):
        #use a 3d array to represent board
        this.board = [[Tile(i, j, this) for i in range(size.xr)] for j in range(size.yr)]
        #initialize board sizes
        this.pos = pos      #position of board
        this.size = size    #dimensions of board
        this.minesLeft = mines     #amount of mines - flagged mines
        this.mines = mines      #amount of mines on the board
        this.blank = True       #is the board blank? (not generated yet)
        this.won = False        #is the board solved?
        this.lost = False       #has a mine been clicked?
        this.button = button    #buttons


    #update the board
    def update(this):
        #reset mine counter
        this.minesLeft = this.mines
        win = True
        lose = False
        #loop through mines
        for i in this.board:
            for j in i:
                #update mine counter
                if j.cover == 'f':
                    this.minesLeft -= 1
                #check for win
                if win and (j.cover == 'c' or (j.cover == 'f' and not j.mine) or (j.cover == 'o' and j.mine)):
                    win = False
                #check for loss
                if not lose and j.cover == 'o' and j.mine:
                    lose = True
        if not this.button.editor.editing:
            if lose: this.lost = True
            if win: this.won = True
        


    #left click on board
    def leftClick(this, x, y):
        #generate board if board is blank
        if this.blank and not this.button.editor.editing:
            this.newBoard((x, y))
        this.board[y][x].lClick()
    #right click on board
    def rightClick(this, x, y, state):
        this.board[y][x].rClick(state)


    #reset the board
    def reset(this):
        this.board = [[Tile(i, j, this) for i in range(this.size.xr)] for j in range(this.size.yr)]
        this.blank = True
        this.won = False
        this.lost = False


    #randomly generate new board
    def newBoard(this, firstClick):
        #generate 2d array to keep track of available spaces
        available = [[i for i in range(this.size.xr)] for _ in range(this.size.yr)]
        #number of entries in "available"
        entries = this.size.xr * this.size.yr
        #create a 3x3 safe zone around click
        for i in range(3):
            i += firstClick[0] - 1
            for j in range(3):
                j += firstClick[1] - 1
                #make sure tile is in range
                if i >= 0 and i < this.size.xr and j >= 0 and j < this.size.yr:
                    #remove the tiles from array of available tiles
                    available[j].remove(this.board[j][i].x)
                    entries -= 1
        this.blank = False
        
        #loop over mines that need to be placed
        for _ in range(this.mines):
            rand = random.randint(1, entries)
            #loop until the right row is found
            for i in range(this.size.yr):
                length = len(available[i])
                if rand <= length:
                    #convert selected square to mine
                    this.board[i][available[i][rand - 1]].addMine()
                    available[i].remove(available[i][rand - 1])
                    entries -= 1
                    break
                rand -= length



#class to represent each tile on the board
class Tile:

    def __init__(this, x, y, board):
        this.x, this.y = x, y
        this.num = 0    #attribute to represent the number of the tile
        this.cover = 'c'    #is mine covered? c = covered, o = open, f = flagged
        this.mine = False   #is the tile a mine?
        this.b = board


    #increment/decrement number
    def increment(this):
        this.num += 1
    def decrement(this):
        this.num -= 1


    #convert to mine
    def addMine(this):
        if this.mine == False:
            this.mine = True
            #cycle adjacent tiles
            for i in range(3):
                i += this.x - 1
                for j in range(3):
                    j += this.y - 1
                    #make sure tile is in range
                    if i >= 0 and i < this.b.size.xr and j >= 0 and j < this.b.size.yr:
                        this.b.board[j][i].increment()

    #remove mine
    def remMine(this):
        if this.mine == True:
            this.mine = False
            #cycle adjacent tiles
            for i in range(3):
                i += this.x - 1
                for j in range(3):
                    j += this.y - 1
                    #make sure tile is in range
                    if i >= 0 and i < this.b.size.xr and j >= 0 and j < this.b.size.yr:
                        this.b.board[j][i].decrement()


    #revert to default state
    def revert(this):
        this.cover = 'c'
        this.mine = False


    #open surrounding mines
    def spread(this):
        #cycle adjacent tiles
        for i in range(3):
            i += this.x - 1
            for j in range(3):
                j += this.y - 1
                #make sure tile is in range
                if i >= 0 and i < this.b.size.xr and j >= 0 and j < this.b.size.yr:
                    this.b.board[j][i].lClick()


    #when tile is left clicked
    def lClick(this):
        if not this.b.button.editor.editing:
            #zero spreading
            if this.num == 0 and this.cover == 'c':
                this.cover = 'o'
                this.spread()
            elif this.cover == 'c':
                this.cover = 'o'
        
        #editing
        else:
            if this.mine:
                this.remMine()
            else:
                this.addMine()
    
    #when tile is right clicked
    def rClick(this, state):
        if not this.b.button.editor.editing:
            #flag
            if this.cover == 'c' and state == 'c':
                this.cover = 'f'
            elif this.cover == 'f' and state == 'f':
                this.cover = 'c'
            
            #reveal neighboring tiles if tile is satisfied
            if this.cover == 'o':
                mines = 0 #neighboring mines
                #cycle adjacent tiles
                for i in range(3):
                    i += this.x - 1
                    for j in range(3):
                        j += this.y - 1
                        #make sure tile is in range
                        if i >= 0 and i < this.b.size.xr and j >= 0 and j < this.b.size.yr:
                            #increment mine counter
                            if this.b.board[j][i].cover == 'f':
                                mines += 1
                #if the tile is fulfilled, open surrounding mines
                if mines == this.num:
                    this.spread()
        
        #editing
        else:
            if this.cover != 'o': this.cover = 'o'
            else: this.cover = 'c'