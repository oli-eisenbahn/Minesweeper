#this file handles left and right clicks on the application

import pygame
import board
import math
import draw
import text

#handles clicks
class Click:

    def __init__(this, b, type, loc, button):
        this.b = b          #board
        this.type = type    #type of click
        this.loc = loc      #location of click
        this.button = button    #button classes
        this.relX = math.floor(loc[0] / 40) #relative x position
        this.relY = math.floor(loc[1] / 40) #relative y position
        #if the board is clicked on establish the state of the tile being clicked on
        this.tileState = None
        if this.onBoard(this.relX, this.relY):
            this.tileState = b.board[this.relY - b.pos.yr][this.relX - b.pos.xr].cover

        #trigger clicks (only on init)
        if type == "left":
            this.leftClick()
        elif type == "right":
            this.rightClick()
        


    #update mouse position, render box
    def update(this, loc):
        newRelX = math.floor(loc[0] / 40) #new relative x position
        newRelY = math.floor(loc[1] / 40) #new relative y position
        
        if not this.b.button.editor.editing:
            #retrigger click if on a different tile if:
            if ((newRelX != this.relX or newRelY != this.relY) and  #the position has changed
                this.onBoard(newRelX, newRelY) and                  #the click was on the board
                this.tileState != 'o' and                           #the first click was not on an open tile
                #the tile has the same state as the first clicked tile
                this.tileState == this.b.board[newRelY - this.b.pos.yr][newRelX - this.b.pos.xr].cover):

                this.relX, this.relY = newRelX, newRelY
                #retrigger
                if this.type == "left":
                    this.leftClick()
                elif this.type == "right":
                    this.rightClick()
            else:
                this.relX, this.relY = newRelX, newRelY
            this.loc = loc

        #editing
        else:
            if this.tileState == 'f': this.tileState = 'c'
            if ((newRelX != this.relX or newRelY != this.relY) and  #the position has changed
                this.onBoard(newRelX, newRelY) and                  #the click was on the board
                #the tile has the same state as the first clicked tile
                (this.tileState == this.b.board[newRelY - this.b.pos.yr][newRelX - this.b.pos.xr].cover or this.type == "left")):

                this.relX, this.relY = newRelX, newRelY
                #retrigger
                if this.type == "left":
                    this.leftClick()
                elif this.type == "right":
                    this.rightClick()
            else:
                this.relX, this.relY = newRelX, newRelY
            this.loc = loc


    def leftClick(this):
        #check if clicked on board
        if not this.button.saves.saveMenu:
            if this.onBoard(this.relX, this.relY):
                this.b.leftClick(this.relX - this.b.pos.xr, this.relY - this.b.pos.yr)
        else:
            this.leftMenuClick()
        
        #individual buttons

        #new game
        if this.relX == this.button.plus.xr and this.relY == this.button.plus.yr:
            this.b.reset()
            this.button.saves.saveMenu = False

        #editor
        elif this.relX == this.button.editor.xr and this.relY == this.button.editor.yr:
            this.button.editor.toggle()

        #saved boards menu
        elif this.relX == this.button.saves.xr and this.relY == this.button.saves.yr:
            this.button.saves.toggle()

    def rightClick(this):
        #check if clicked on board
        if this.onBoard(this.relX, this.relY):
            this.b.rightClick(this.relX - this.b.pos.xr, this.relY - this.b.pos.yr, this.tileState)
    

    def leftMenuClick(this):
        #check if clicked on board
        if this.onBoard(this.relX, this.relY):
            row = this.relY - this.b.pos.yr
            column = this.relX - this.b.pos.xr

            #copy
            if column == 0:
                text.slotToClip(row)

            #paste
            elif column == 1:
                text.clipToSlot(row)

            #save board
            elif column == 6:
                text.saveBoard(this.b, row)

            #play board
            elif column == 5:
                text.loadBoard(this.b, row)
                this.button.saves.saveMenu = False
            
            else: return
            this.button.saves.saveSlotCheck()



    #check if the mouse is over board
    def onBoard(this, x, y):
        if (x >= this.b.pos.xr and 
            y >= this.b.pos.yr and 
            x < (this.b.pos.xr + this.b.size.xr) and 
            y < (this.b.pos.yr + this.b.size.yr)):
            return True
        return False