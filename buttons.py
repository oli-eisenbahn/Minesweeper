#this file handles the buttons at the top of the screen

#class to store all button classes
class Button:

    def __init__(this, plus, editor, counter, saves):
        this.plus = Plus(plus)
        this.editor = Editor(editor)
        this.counter = Counter(counter)
        this.saves = Saves(saves)


#new game button
class Plus:

    def __init__(this, pos):
        #update attributes to include x and y
        this.__dict__.update(pos.__dict__)


#editor tab
class Editor:

    def __init__(this, pos):
        #update attributes to include x and y
        this.__dict__.update(pos.__dict__)
        this.editing = False    #is the board being edited?

    #toggle editing mode
    def toggle(this):
        if this.editing:    this.editing = False
        else:               this.editing = True


#saves tab
class Saves:

    def __init__(this, pos):
        #update attributes to include x and y
        this.__dict__.update(pos.__dict__)
        this.saveMenu = False
        this.occupied = [False for _ in range(16)]

        this.saveSlotCheck()

    #toggle menu
    def toggle(this):
        if this.saveMenu:   this.saveMenu = False
        else:               this.saveMenu = True
    
    #check which save slots are occupied
    def saveSlotCheck(this):
        FILE = open("text.txt", "r")

        lines = FILE.readlines()
        for i in range(16):

            for j in lines[i]:
                if j != '!' and j != '\n':
                    this.occupied[i] = True
                    break
                elif j == '\n':
                    this.occupied[i] = False
            
        FILE.close()


#mine counter
class Counter:

    def __init__(this, pos):
        #update attributes to include x and y
        this.__dict__.update(pos.__dict__)