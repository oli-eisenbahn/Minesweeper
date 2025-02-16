#this file renders every part of the application

import pygame
import math
pygame.init()


#all colors and fonts
class Colors:
    def __init__(this):
        this.tileFace = (160, 160, 160)     #main face of the tile
        this.tileLight = (250, 250, 250)    #up and left sides of the tile, in light
        this.tileDark = (120, 120, 120)     #down and right sides of tile, in shadow

        #list of colors, used for coloring the numbers under tiles
        this.numCol = [(0,0,0),          #null
                       (157,192,246),    #1
                       (143,178,134),    #2
                       (246,154,186),    #3
                       (185,153,246),    #4
                       (246,137,103),    #5
                       (140,246,221),    #6
                       (200,200,200),    #7
                       (120,120,120) ]   #8    
        
        this.FONT = pygame.font.SysFont("", 50)
        this.FONT2 = pygame.font.SysFont("", 60)



#used render different shapes easily
class Draw:

    def __init__(this, WIN, color, tileSize):
        #variables the class will have to use
        this.tileSize = tileSize
        this.color = color
        this.WIN = WIN
    
    def rect(this, rp, rc, rr = None): #rp = (top left x, top left y, bottom right offset x, bottom right offset y), rc = (red, green, blue), rr = rounding
        if rr == None:
            pygame.draw.rect(this.WIN, rc, rp)
        else:
            pygame.draw.rect(this.WIN, rc, rp, 0, rr)
    
    def circ(this, cp, cr, cc): #cp = centerpoint position, cr = radius, cc = (red, green, blue)
        pygame.draw.circle(this.WIN, cc, cp, cr)
    
    def poly(this, pp, pc): #pp = [list of tuples of vertices], pc = (red, green, blue)
        pygame.draw.polygon(this.WIN, pc, pp)
    
    def text(this, tp, tc, tf, tx): #tp = (position), tc = color, tf = font {string}, tx = text {string}
        this.WIN.blit((tf).render(tx, 1, tc), tp)
    
    #since so many of the same basic tile shape are used, this method produces them, taking inputs of the colors of each face (default grey)
    def tile(this, x, y, colLight = None, colMed = None, colDark = None):
        
        #retrieve the tile size
        t = this.tileSize

        #scale the x and y values appropriately
        x *= t
        y *= t

        #set default color values
        if colLight == None: colLight = this.color.tileLight
        if colMed == None: colMed = this.color.tileFace
        if colDark == None: colDark = this.color.tileDark
        
        #add each shape that makes up the tile to the masterlist
        pygame.draw.polygon(this.WIN, colLight, [(x,y), (x+t,y), (x,y+t)])
        pygame.draw.polygon(this.WIN, colDark, [(x+t,y+t), (x+t,y), (x,y+t)])
        pygame.draw.rect(this.WIN, colMed, (x+3,y+3,t-6,t-6))
    
    #selectbox
    def select(this, x, y):
        pygame.draw.rect(this.WIN, (80, 80, 80), (x*40,y*40,41,41), 3)
            


#adds all needed shapes to the Draw class so they can be rendered
def drawShapes(WIN, b, button, mouse, tileSize, winSize):
    
    #initialize draw & colors class
    color = Colors()
    draw = Draw(WIN, color, tileSize)
    

    """BACKGROUND"""

    #checkerboard colors
    backgroundCol1 = (50,50,50)
    backgroundCol2 = (40,40,40)

    #loop through size of the window
    for i in range(winSize.xr//2):
        for j in range(winSize.yr):
            
            #add each square to the draw class, doubling each value and adding offset to create a checkerboard
            draw.rect(((i * 2 + (j % 2)) * tileSize, j * tileSize, tileSize, tileSize), backgroundCol1)
            draw.rect(((i * 2 + ((j + 1) % 2)) * tileSize, j * tileSize, tileSize, tileSize), backgroundCol2)



    """BUTTONS"""

    #new game
    draw.tile(button.plus.xr, button.plus.yr, (180, 215, 180), (50, 200, 50), (1, 150, 32))
    draw.rect((button.plus.x + 3, button.plus.y + 15, tileSize - 6, tileSize - 30), (1, 140, 32))
    draw.rect((button.plus.x + 15, button.plus.y + 3, tileSize - 30, tileSize - 6), (1, 140, 32))

    #edit board
    if not button.editor.editing:   #variant 1 (not editing)
        draw.tile(button.editor.xr, button.editor.yr, (255,207,173), (246,137,83), (186,77,43))
        draw.poly([(button.editor.x+40,button.editor.y+15),(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+30,button.editor.y+25)],(186,77,43))
        draw.poly([(button.editor.x+25,button.editor.y),(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+15,button.editor.y+10)],(186,77,43))
    else:               #variant 2 (editing)
        draw.tile(button.editor.xr, button.editor.yr, (186,77,43), (246,137,83), (255,207,173))
        draw.poly([(button.editor.x+40,button.editor.y+15),(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+30,button.editor.y+25)],(186,77,43))
        draw.poly([(button.editor.x+25,button.editor.y),(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+15,button.editor.y+10)],(186,77,43))

    #saved boards menu
    draw.tile(button.saves.xr, button.saves.yr, (200,200,250), (120,120,250), (80,80,120))
    if button.saves.saveMenu:
        draw.tile(button.saves.xr, button.saves.yr, (80,80,120), (120,120,250), (200,200,250))
    draw.rect((button.saves.x+6,button.saves.y+7,28,6), (80,80,120))
    draw.rect((button.saves.x+6,button.saves.y+17,28,6), (80,80,120))
    draw.rect((button.saves.x+6,button.saves.y+27,28,6), (80,80,120))



    """BOARD"""

    #regular play screen
    if not button.saves.saveMenu:
        #loop through all tiles
        for i in b.board:
            for j in i:
                
                #position of the tile
                tileX = j.x + b.pos.xr
                tileY = j.y + b.pos.yr

                #draw all mines if a mine was clicked
                if (b.lost and j.mine) or (j.mine and j.cover == 'o'):
                    WIN.blit((pygame.transform.scale(pygame.image.load("assets\cherry3.png"), (40,40))), (tileX * tileSize, tileY * tileSize))

                #draw closed tiles
                elif j.cover == 'c':
                    draw.tile(tileX, tileY)

                #draw red flag if the game isn't won; green flag if the game is won
                elif j.cover == 'f':
                    if not b.won:
                        draw.tile(tileX, tileY, (240, 180, 180), (200, 80, 80), (140, 40, 40)) 
                        #(255, 220, 220), (255, 140, 140), (255, 80, 80) red mine
                        #(120, 120, 120), (160, 160, 160), (250, 250, 250) alt grey mine
                        #(80, 80, 80), (110, 110, 110), (140, 140, 140) grey mine
                    else:
                        draw.tile(tileX, tileY, (180, 215, 180), (100, 200, 100), (1, 150, 32))

                #draw numbers for open tiles
                elif j.cover == 'o' and j.num > 0:
                    draw.text((tileX * tileSize + 11, tileY * tileSize + 4), color.numCol[j.num], color.FONT, f"{j.num}")
                
                #draw numbers on tiles in the editor
                if button.editor.editing and j.cover != 'o':
                    #mine
                    if j.mine:
                        WIN.blit((pygame.transform.scale(pygame.image.load("assets\cherry3.png"), (40,40))), (tileX * tileSize, tileY * tileSize))
                    #numbers
                    elif j.num > 0:
                        draw.text((tileX * tileSize + 11, tileY * tileSize + 4), (20,20,20), color.FONT, f"{j.num}")
    
    #saved boards menu
    else:
        drawSaves(draw, b, button, tileSize)
                


    """MINE COUNTER"""

    numFont = pygame.font.Font("assets\clock.ttf", 30)
    numOffset = 0
    if b.minesLeft > 99 or b.minesLeft < -9:
        numOffset = 10
    elif b.minesLeft < 10 and b.minesLeft >= 0:
        numOffset = -10

    pygame.draw.polygon(WIN, (250, 250, 250), [(button.counter.x,button.counter.y),(button.counter.x,button.counter.y+40),(button.counter.x+20,button.counter.y+20),(button.counter.x+60,button.counter.y+20),(button.counter.x+80,button.counter.y)])
    pygame.draw.polygon(WIN, (120, 120, 120), [(button.counter.x+80,button.counter.y+40),(button.counter.x,button.counter.y+40),(button.counter.x+20,button.counter.y+20),(button.counter.x+60,button.counter.y+20),(button.counter.x+80,button.counter.y)])
    pygame.draw.rect(WIN, (160, 160, 160), (button.counter.x+3,button.counter.y+3,74,34))
    pygame.draw.rect(WIN, (20,20,20), (button.counter.x+6,button.counter.y+6,68,28))
    draw.text((button.counter.x+25-numOffset,button.counter.y+4), (255,0,0), numFont, f"{b.minesLeft}")



    """SELECT BOX"""
    
    x = math.floor(mouse[0] / 40) #relative x position
    y = math.floor(mouse[1] / 40) #relative y position

    #board & saves menu
    if (x >= b.pos.xr and y >= b.pos.yr and    #board lower limit
        x < (b.pos.xr + b.size.xr) and y < (b.pos.yr + b.size.yr)):   #board upper limit

        #board
        if not button.saves.saveMenu:
            if (b.board[y - b.pos.yr][x - b.pos.xr].cover != 'o'):    #tile is closed
                draw.select(x, y)
        
        #saves menu
        else:
            x2 = x - b.pos.xr
            if x2 == 0 or x2 == 1 or x2 == 5 or x2 == 6:
                draw.select(x, y)
    
    #buttons
    if ((x == button.plus.xr and y == button.plus.yr) or    #new game
        (x == button.saves.xr and y == button.saves.yr) or  #saved boards menu
        (x == button.editor.xr and y == button.editor.yr)):  #editor
        draw.select(x, y)



    
"""

    #editor
    pygame.draw.polygon(WIN, (255,207,173), [(button.editor.x,button.editor.y),(button.editor.x+40,button.editor.y),(button.editor.x,button.editor.y+40)])
    pygame.draw.polygon(WIN, (186,77,43), [(button.editor.x+40,button.editor.y+40),(button.editor.x+40,button.editor.y),(button.editor.x,button.editor.y+40)])
    pygame.draw.rect(WIN, (246,137,103), (button.editor.x+3,button.editor.y+3,34,34))
    #pygame.draw.circle(WIN, (186,77,43), (button.editor.x+15,button.editor.y+15), 10)
    #pygame.draw.circle(WIN, (246,137,103), (button.editor.x+10,button.editor.y+10), 6)
    #pygame.draw.polygon(WIN, (246,137,103), [(button.editor.x+3,button.editor.y+9),(button.editor.x+9,button.editor.y+3),(button.editor.x+18,button.editor.y+13),(button.editor.x+13,button.editor.y+18)])
    #pygame.draw.polygon(WIN, (186,77,43), [(button.editor.x+28,button.editor.y+33),(button.editor.x+33,button.editor.y+28),(button.editor.x+18,button.editor.y+13),(button.editor.x+13,button.editor.y+18)])
    pygame.draw.polygon(WIN, (186,77,43), [(button.editor.x+40,button.editor.y+15),(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+30,button.editor.y+25)])
    pygame.draw.polygon(WIN, (186,77,43), [(button.editor.x+25,button.editor.y),(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+15,button.editor.y+10)])
    #pygame.draw.lines(WIN, (255,207,173), False, [(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+15,button.editor.y+10),(button.editor.x+23,button.editor.y+17),(button.editor.x+15,button.editor.y+10),(button.editor.x+25,button.editor.y)], 4)
    if globs[2]:
        pygame.draw.polygon(WIN, (186,77,43), [(button.editor.x,button.editor.y),(button.editor.x+40,button.editor.y),(button.editor.x,button.editor.y+40)])
        pygame.draw.polygon(WIN, (255,207,173), [(button.editor.x+40,button.editor.y+40),(button.editor.x+40,button.editor.y),(button.editor.x,button.editor.y+40)])
        pygame.draw.rect(WIN, (246,137,103), (button.editor.x+3,button.editor.y+3,34,34))
        pygame.draw.polygon(WIN, (186,77,43), [(button.editor.x+40,button.editor.y+15),(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+30,button.editor.y+25)])
        pygame.draw.polygon(WIN, (186,77,43), [(button.editor.x+25,button.editor.y),(button.editor.x+40,button.editor.y),(button.editor.x+10,button.editor.y+30),(button.editor.x+15,button.editor.y+10)])

        #cover button
        pygame.draw.polygon(WIN, (210, 230, 250), [(coverX*40,coverY*40),(coverX*40+40,coverY*40),(coverX*40,coverY*40+40)])
        pygame.draw.polygon(WIN, (100, 120, 160), [(coverX*40+40,coverY*40+40),(coverX*40+40,coverY*40),(coverX*40,coverY*40+40)])
        pygame.draw.rect(WIN, (140, 160, 200), (coverX*40+3,coverY*40+3,34,34))

    numFont = pygame.font.Font("clock.ttf", 30)
    numOffset = 0
    if minesLeft > 99:
        numOffset = 10
    elif minesLeft < 10:
        numOffset = -10

    #mine counter
    pygame.draw.polygon(WIN, (250, 250, 250), [(button.counter.x,button.counter.y),(button.counter.x,button.counter.y+40),(button.counter.x+20,button.counter.y+20),(button.counter.x+60,button.counter.y+20),(button.counter.x+80,button.counter.y)])
    pygame.draw.polygon(WIN, (120, 120, 120), [(button.counter.x+80,button.counter.y+40),(button.counter.x,button.counter.y+40),(button.counter.x+20,button.counter.y+20),(button.counter.x+60,button.counter.y+20),(button.counter.x+80,button.counter.y)])
    pygame.draw.rect(WIN, (160, 160, 160), (button.counter.x+3,button.counter.y+3,74,34))
    pygame.draw.rect(WIN, (20,20,20), (button.counter.x+6,button.counter.y+6,68,28))
    WIN.blit(numFont.render(f"{minesLeft}", 1, (255,0,0)), (minesX*40+25-numOffset,minesY*40+4))


    #saves
    pygame.draw.polygon(WIN, (200,200,250), [(button.saves.x,button.saves.y),(button.saves.x+40,button.saves.y),(button.saves.x,button.saves.y+40)])
    pygame.draw.polygon(WIN, (80,80,120), [(button.saves.x+40,button.saves.y+40),(button.saves.x+40,button.saves.y),(button.saves.x,button.saves.y+40)])
    pygame.draw.rect(WIN, (140,140,250), (button.saves.x+3,button.saves.y+3,34,34))
    #pygame.draw.circle(WIN, (80,80,120), (button.saves.x+20,button.saves.y+20), 15)
    #pygame.draw.rect(WIN, (80,80,120), (button.saves.x+15,button.saves.y+3,10,34))
    #pygame.draw.rect(WIN, (80,80,120), (button.saves.x+3,button.saves.y+15,34,10))
    #pygame.draw.polygon(WIN, (80,80,120), [(button.saves.x+10,button.saves.y+4),(button.saves.x+4,button.saves.y+10),(button.saves.x+29,button.saves.y+35),(button.saves.x+35,button.saves.y+29)])
    #pygame.draw.polygon(WIN, (80,80,120), [(button.saves.x+11,button.saves.y+35),(button.saves.x+5,button.saves.y+29),(button.saves.x+30,button.saves.y+4),(button.saves.x+36,button.saves.y+10)])
    pygame.draw.rect(WIN, (80,80,120), (button.saves.x+6,button.saves.y+7,28,6))
    pygame.draw.rect(WIN, (80,80,120), (button.saves.x+6,button.saves.y+17,28,6))
    pygame.draw.rect(WIN, (80,80,120), (button.saves.x+6,button.saves.y+27,28,6))
    if globs[4]:
        pygame.draw.polygon(WIN, (80,80,120), [(button.saves.x,button.saves.y),(button.saves.x+40,button.saves.y),(button.saves.x,button.saves.y+40)])
        pygame.draw.polygon(WIN, (200,200,250), [(button.saves.x+40,button.saves.y+40),(button.saves.x+40,button.saves.y),(button.saves.x,button.saves.y+40)])
        pygame.draw.rect(WIN, (140,140,250), (button.saves.x+3,button.saves.y+3,34,34))
        pygame.draw.rect(WIN, (80,80,120), (button.saves.x+6,button.saves.y+7,28,6))
        pygame.draw.rect(WIN, (80,80,120), (button.saves.x+6,button.saves.y+17,28,6))
        pygame.draw.rect(WIN, (80,80,120), (button.saves.x+6,button.saves.y+27,28,6))
"""


def drawSaves(draw, b, button, tileSize):

    for j in range(16):
        jr = j  #relative offset
        j = jr * tileSize    #actual offset
        
        #colors for slot labels
        color1 = [(250, 250, 250),(120, 120, 120),(160, 160, 160),(100, 100, 100)]
        if not button.saves.occupied[jr]: color1 = [(100, 100, 100),(100, 100, 100),(100, 100, 100),(160, 160, 160)]

        #tiles behind slot buttons
        for i in [0,1,5,6]:
            draw.tile(b.pos.xr + i, b.pos.yr + jr, (250, 250, 250), (160, 160, 160), (120, 120, 120))


        #copy
        i = 0   #x alignment of button
        x,y = 15,6
        draw.rect((b.pos.x+i+x,b.pos.y+j+y,20,25), (100, 100, 100))
        x,y = 6,10
        draw.rect((b.pos.x+i+x-2,b.pos.y+j+y-2,24,29),(160, 160, 160))
        draw.rect((b.pos.x+i+x,b.pos.y+j+y,20,25),(100, 100, 100))
        draw.rect((b.pos.x+i+x-2,b.pos.y+j+y-2,7+4,7+4),(160, 160, 160))
        draw.poly([(b.pos.x+i+x+7,b.pos.y+j+y+7),(b.pos.x+i+x+7,b.pos.y+j+y),(b.pos.x+i+x,b.pos.y+j+y+7)],(100, 100, 100))

        #paste
        i = 40
        x,y = 8,9
        draw.rect((b.pos.x+i+x,b.pos.y+j+y,24,26),(100, 100, 100),2)
        draw.rect((b.pos.x+i+x+4,b.pos.y+j+y+4,24-8,26-8),(160, 160, 160))
        draw.rect((b.pos.x+i+x+4,b.pos.y+j+y-4,16,10),(160, 160, 160))
        draw.rect((b.pos.x+i+x+6,b.pos.y+j+y-2,12,6),(100, 100, 100))
        draw.circ((b.pos.x+i+x+12,b.pos.y+j+y-2),3,(100, 100, 100))
        draw.rect((b.pos.x+i+x+6,b.pos.y+j+y+7,24-12,2),(100, 100, 100))
        draw.rect((b.pos.x+i+x+6,b.pos.y+j+y+12,24-12,2),(100, 100, 100))
        draw.rect((b.pos.x+i+x+6,b.pos.y+j+y+17,24-12,2),(100, 100, 100))

        #slots
        i = 80
        draw.poly([(b.pos.x+i,b.pos.y+j),(b.pos.x+120+i,b.pos.y+j),(b.pos.x+100+i,b.pos.y+20+j),(b.pos.x+20+i,b.pos.y+20+j),(b.pos.x+i,b.pos.y+40+j)],color1[0])
        draw.poly([(b.pos.x+120+i,b.pos.y+40+j),(b.pos.x+120+i,b.pos.y+j),(b.pos.x+100+i,b.pos.y+20+j),(b.pos.x+20+i,b.pos.y+20+j),(b.pos.x+i,b.pos.y+40+j)],color1[1])
        draw.rect((b.pos.x+3+i,b.pos.y+3+j,114,34),color1[2])

        FONT = pygame.font.SysFont("", 40)
        if jr > 8:
            FONT = pygame.font.SysFont("", 35)
        draw.text((b.pos.x+i+12,b.pos.y+8+j), color1[3], FONT, f"SLOT {jr + 1}")


        #play board
        i = 200
        draw.poly([(b.pos.x+10+i,b.pos.y+8+j),(b.pos.x+10+i,b.pos.y+32+j),(b.pos.x+30+i,b.pos.y+20+j)],(100, 100, 100))

        #save board
        i = 240
        draw.rect((b.pos.x+3+i,b.pos.y+32+j,34,5),(100, 100, 100))
        draw.rect((b.pos.x+17+i,b.pos.y+13+j,7,17),(100, 100, 100))
        draw.poly([(b.pos.x+20+i,b.pos.y+5+j),(b.pos.x+12+i,b.pos.y+13+j),(b.pos.x+28+i,b.pos.y+13+j)],(100, 100, 100))
        
        



#alt squares
#pygame.draw.polygon(WIN, (250, 250, 250), [(jOffset,iOffset),(jOffset+40,iOffset),(jOffset,iOffset+40)])
#pygame.draw.polygon(WIN, (120, 120, 120), [(jOffset+40,iOffset+40),(jOffset+40,iOffset),(jOffset,iOffset+40)])
#pygame.draw.rect(WIN, (160, 160, 160), (jOffset+3,iOffset+3,34,34),5)
