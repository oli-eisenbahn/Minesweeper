"""
This project is a take on the classic game minesweeper, with a built-in editor that allows
the user to create challenging boards. It also has 
"""

#imports
import pygame
import click
import draw
import board
import buttons
pygame.init()


"""THIS SECTION USES CLASSES AS DICTIONARIES TO STORE GLOBAL VARIABLES"""

tileSize = 40           #size of each tile on the board


#alternative to a tuple for storing x,y coordinates for better syntax
class XY:
    def __init__(this, x, y):
        this.xr = x             #r = relative position in relation to the grid of the window
        this.yr = y
        this.x = x * tileSize   #actual pixel position
        this.y = y * tileSize


#sizes & counts
totalMines = 40         #total mines
boardSize = XY(16, 16)    #number of tiles on the board
winSize = XY(18, 19)      #window size (in tiles)


#positions
boardPos = XY(1,2)        #board
minesPos = XY(15,1)       #mine counter
plusPos = XY(1,1)         #new game button
editorPos = XY(2,1)       #edit board button
settingsPos = XY(3,1)     #saved boards menu button
textPos = XY(4,1)         #labels
coverPos = XY(14,1)       #cover button (editor only)


#which click is being held down, used for toggles that only toggle at the start of a click
class Clicks:
    def __init__(this):
        this.left = False
        this.right = False

clicks = Clicks()

button = buttons.Button(plusPos, editorPos, minesPos, settingsPos)

b = board.Board(boardPos, boardSize, totalMines, button)





"""OTHER VARIOUS INITIALIZTIONS"""

#initialize fonts


#create the window
WIN = pygame.display.set_mode((winSize.x, winSize.y))
pygame.display.set_caption("Minesweeper")

#if there is a saved board in each slot
saveSlots = [False for i in range(16)]
#click.saveSlotCheck(saveSlots)




clock = pygame.time.Clock()
#keep track of clicks in progress
clicks = [None, None]

def main():
    run = True

    while run:

        for event in pygame.event.get():
            
            #quit
            if event.type == pygame.QUIT:
                run = False
                break

            #clicks down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #left and right click
                if pygame.mouse.get_pressed()[0]:
                    clicks[0] = click.Click(b, "left", pygame.mouse.get_pos(), button)
                if pygame.mouse.get_pressed()[2]:
                    clicks[1] = click.Click(b, "right", pygame.mouse.get_pos(), button)
            
            #clicks up
            elif event.type == pygame.MOUSEBUTTONUP:
                #left and right click
                if not pygame.mouse.get_pressed()[0]:
                    clicks[0] = None
                if not pygame.mouse.get_pressed()[1]:
                    clicks[1] = None
            

            #update mouse position
            for i in clicks:
                if i != None:
                    i.update(pygame.mouse.get_pos())
                
                
        b.update()
        draw.drawShapes(WIN, b, button, pygame.mouse.get_pos(), tileSize, winSize)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()