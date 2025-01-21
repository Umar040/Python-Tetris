import random
import time


#------------------------------------------Tetris Pieces----------------------------------------------------------
class TPiece:
    def __init__(self,size):
        self.size = size
        self.name = "T"

class OPiece:
    def __init__(self,size):
        self.size = size
        self.name = "O"

class SPiece:
    def __init__(self,size):
        self.size = size
        self.name = "S"

class ZPiece:
    def __init__(self,size):
        self.size = size
        self.name = "Z"

class IPiece:
    def __init__(self,size):
        self.size = size
        self.name = "I"

class LPiece:
    def __init__(self,size):
        self.size = size
        self.name = "L"

class JPiece:
    def __init__(self,size):
        self.size = size
        self.name = "J"

################################################################################################################################
#------------------------------------------------Game Code---------------------------------------------------------------------#
################################################################################################################################
class Game:
    def __init__(self,heightW,holesW,blockHolesW,wellsW,clearsW,size=30):
        #Initalising variables
        self.squares = []
        #Board select y then x [y][x]
        self.board = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
        self.size=size
        self.piecesLeft = ["T","O","S","Z","I","L","J"]
        self.held = None #True/False
        self.heldPiece = None #String representation of piece
        self.next = None #String representation of piece
        self.makePiece()
        self.bestBoard = []
        self.currentPieceSquares = []
        self.blankHeld = False
        self.cleared = False
        self.linesCleared = 0
        self.failed=False
        self.heightW = heightW
        self.holesW = holesW
        self.blockHolesW = blockHolesW
        self.wellsW = wellsW
        self.clearsW = clearsW
        self.startTime = time.time()

    #Makes the next piece the current piece and generates a new next piece
    def makePiece(self):
        if self.next == None:
            piece = random.choice(self.piecesLeft)
            self.piecesLeft.remove(piece)
            self.next = random.choice(self.piecesLeft)
            self.piecesLeft.remove(self.next)
        else:
            #If there is no current held and you try to hold a piece the current piece becomes held the next piece becomes the current piece and the next piece is generated
            if self.blankHeld:
                piece = random.choice(self.piecesLeft)
                self.piecesLeft.remove(piece)
                if len(self.piecesLeft) == 0:
                    self.piecesLeft = ["T","O","S","Z","I","L","J"]
                else:
                    self.next = random.choice(self.piecesLeft)
                    self.piecesLeft.remove(self.next)
                self.blankHeld = False
            else:
                piece = self.next
                self.next = random.choice(self.piecesLeft)
                self.piecesLeft.remove(self.next)
        if len(self.piecesLeft) == 0:
            self.piecesLeft = ["T","O","S","Z","I","L","J"] #Refreshes list when empty
        self.currentPiece = self.getPiece(piece)
        self.nextPiece = self.getPiece(self.next)

    #Creates a piece object from the string representation of the pieces
    def getPiece(self,p):
        if p == "T":
            return TPiece(self.size)
        elif p == "O":
            return OPiece(self.size)
        elif p == "S":
            return SPiece(self.size)
        elif p == "Z":
            return ZPiece(self.size)
        elif p == "I":
            return IPiece(self.size)
        elif p == "L":
            return LPiece(self.size)
        elif p == "J":
            return JPiece(self.size)

    #Check for clearlines and gameover
    def AICheck(self):
        if time.time()-self.startTime >=5: #Set timer for how many seconds before stopping the AI
            self.failed=True
            #Debug code but can enable to see how many lines are cleared for each member of the population
##            print("Complete with",self.linesCleared,"lines cleared")
        rowToDelete = []
        squaresToRemove = []
        redSquaresToRemove = []
        if self.alt:
            for row in range(len(self.altBestBoard)):
                if all(self.altBestBoard[row]): #check if all items in row are 1(True)
                    self.cleared = True
                    self.linesCleared+=1
                    rowToDelete.append(row)
            for row in rowToDelete:
                tempRow = [0,0,0,0,0,0,0,0,0,0]
                for row2 in range(row+1):
                    self.altBestBoard[row2],tempRow = tempRow,self.altBestBoard[row2]
            if 1 in self.altBestBoard[0]:
                self.failed=True
##                print("Complete with",self.linesCleared,"lines cleared")
        else:
            for row in range(len(self.bestBoard)):
                if all(self.bestBoard[row]): #check if all items in row are 1(True)
                    self.cleared = True
                    self.linesCleared+=1
                    rowToDelete.append(row)
            for row in rowToDelete:
                tempRow = [0,0,0,0,0,0,0,0,0,0]
                for row2 in range(row+1):
                    self.bestBoard[row2],tempRow = tempRow,self.bestBoard[row2]
            if 1 in self.bestBoard[0]:
                self.failed=True
##                print("Complete with",self.linesCleared,"lines cleared")

    #Automatic Loop
    def AILoop(self):
        self.alt = False
        self.altBestBoard = None
        self.AI(self.currentPiece.name)
        if self.held: #If a piece is held then do a held piece check to see if it is better than the current piece
            self.AI(self.heldPiece, self.currentMaxScore)
            if not self.altBestBoard == None:
                self.alt = True
                self.heldPiece,self.currentPiece = self.currentPiece.name,self.getPiece(self.heldPiece)
        else: #Otherwise check if the next piece is better so you can hold the current piece to get the next piece
            self.AI(self.next, self.currentMaxScore)
            if not self.altBestBoard == None:
                self.alt = True
                self.held = True
                self.heldPiece,self.currentPiece = self.currentPiece.name,self.nextPiece
                self.blankHeld = True
        self.AICheck()#Checks if any line clears or if the AI has game overed
        if self.cleared:#If a line has been cleared
            self.currentPieceSquares = []
            self.cleared = False
        self.makePiece()#Make a new piece
        if self.alt:
            self.board = self.altBestBoard
        else:
            self.board = self.bestBoard
        self.cleared = False
        

################################################################################################################################
#------------------------------------------------AI Logic----------------------------------------------------------------------#
################################################################################################################################

    #Board is [y][x]
    #First generates all possible board states that can be generated by the piece given
    def AI(self,pieceName,maxScore = None):
        #Generates all O boards fine
        currentMove = []
        if pieceName == "O":
            y = 0
            x = 0
            possibleBoards = []
            allBoards = False
            while allBoards == False:
                copyBoard = [row[:] for row in self.board] #List comprehension needed for copying a list of lists as [:] does shallow copy therefore effecting original
                if x>8:
                    allBoards = True
                else:
                    finished = False
                    while not finished:
                        if copyBoard[y+2][x] == 1 or copyBoard[y+2][x+1] == 1:
                            finished = True
                        elif y>16:
                            y+=1
                            finished = True
                        else:
                            y+=1
                    copyBoard[y][x],copyBoard[y][x+1],copyBoard[y+1][x],copyBoard[y+1][x+1] = 1,1,1,1
                    currentMove.append([[y,x],[y,x+1],[y+1,x],[y+1,x+1]])
                    possibleBoards.append(copyBoard)
                    y=0
                    x+=1
        #Generates all I boards fine
        elif pieceName == "I":
            yv = 1
            xv = 0
            yh = 0
            xh = 1
            possibleBoards = []
            copyBoard = [row[:] for row in self.board]
            allBoards = False
            while allBoards == False:
                if xv>9 and xh>7:
                    allBoards = True
                #Condition 1 (Vertical)
                if xv<=9: #If Y is not past point where vertical block can be placed
                    finished = False
                    while not finished: #While still dropping
                        if copyBoard[yv+3][xv] == 1: #Check if block below
                            finished = True
                        elif yv>15: #If 1 away from bottom
                            yv+=1 #Since already checked if block is there just add 1 and finish
                            finished = True
                        else:
                            yv+=1 #Otherwise keep dropping
                    copyBoard[yv][xv],copyBoard[yv-1][xv],copyBoard[yv+1][xv],copyBoard[yv+2][xv] = 1,1,1,1 #Make shape in 1's
                    currentMove.append([[yv,xv],[yv-1,xv],[yv+1,xv],[yv+2,xv]])
                    possibleBoards.append(copyBoard)#Add to boards
                    copyBoard = [row[:] for row in self.board] #Make fresh new board using self.board
                    yv=1#Reset Y
                    xv+=1#Increment X
                #Condition 2 (Horizontal)
                if xh<=7:
                    finished = False
                    while not finished:
                        if copyBoard[yh+1][xh] == 1 or copyBoard[yh+1][xh+1] == 1 or copyBoard[yh+1][xh-1] == 1 or copyBoard[yh+1][xh+2] == 1:
                            finished = True
                        elif yh>17:
                            yh+=1
                            finished = True
                        else:
                            yh+=1
                    copyBoard[yh][xh],copyBoard[yh][xh-1],copyBoard[yh][xh+1],copyBoard[yh][xh+2] = 1,1,1,1
                    currentMove.append([[yh,xh],[yh,xh-1],[yh,xh+1],[yh,xh+2]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    yh=0
                    xh+=1
        #Generates all T boards fine
        elif pieceName == "T":
            lx = 1
            ly = 1
            ux = 1
            uy = 1
            rx = 0
            ry = 1
            dx = 1
            dy = 0
            possibleBoards = []
            copyBoard = [row[:] for row in self.board]
            allBoards = False
            while allBoards == False:
                if lx>9 and ux>8 and rx>8 and dx>8:
                    allBoards = True
                if lx<=9:
                    finished = False
                    while not finished:
                        if copyBoard[ly+2][lx] == 1 or copyBoard[ly+1][lx-1] == 1:
                            finished = True
                        elif ly>16:
                            ly+=1
                            finished = True
                        else:
                            ly+=1
                    copyBoard[ly][lx],copyBoard[ly][lx-1],copyBoard[ly+1][lx],copyBoard[ly-1][lx] = 1,1,1,1
                    currentMove.append([[ly,lx],[ly,lx-1],[ly+1,lx],[ly-1,lx]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    ly=1
                    lx+=1
                if ux<=8:
                    finished = False
                    while not finished:
                        if copyBoard[uy+1][ux] == 1 or copyBoard[uy+1][ux-1] == 1 or copyBoard[uy+1][ux+1] == 1:
                            finished = True
                        elif uy>17:
                            uy+=1
                            finished = True
                        else:
                            uy+=1
                    copyBoard[uy][ux],copyBoard[uy][ux-1],copyBoard[uy][ux+1],copyBoard[uy-1][ux] = 1,1,1,1
                    currentMove.append([[uy,ux],[uy,ux-1],[uy,ux+1],[uy-1,ux]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    uy=1
                    ux+=1
                if rx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[ry+2][rx] == 1 or copyBoard[ry+1][rx+1] == 1:
                            finished = True
                        elif ry>16:
                            ry+=1
                            finished = True
                        else:
                            ry+=1
                    copyBoard[ry][rx],copyBoard[ry-1][rx],copyBoard[ry+1][rx],copyBoard[ry][rx+1] = 1,1,1,1
                    currentMove.append([[ry,rx],[ry-1,rx],[ry+1,rx],[ry,rx+1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    ry=1
                    rx+=1
                if dx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[dy+1][dx-1] == 1 or copyBoard[dy+1][dx+1] == 1 or copyBoard[dy+2][dx] == 1:
                            finished = True
                        elif dy>16:
                            dy+=1
                            finished = True
                        else:
                            dy+=1
                    copyBoard[dy][dx],copyBoard[dy][dx-1],copyBoard[dy][dx+1],copyBoard[dy+1][dx] = 1,1,1,1
                    currentMove.append([[dy,dx],[dy,dx-1],[dy,dx+1],[dy+1,dx]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    dy=1
                    dx+=1
        #Generates all L boards fine
        elif pieceName == "L":
            rx=0
            ry=1
            dx=1
            dy=0
            lx=1
            ly=1
            ux=1
            uy=1
            possibleBoards = []
            copyBoard = [row[:] for row in self.board]
            allBoards = False
            while allBoards == False:
                if lx>9 and dx>8 and rx>8 and ux>8:
                    allBoards = True
                if lx<=9:
                    finished = False
                    while not finished:
                        if copyBoard[ly][lx-1] == 1 or copyBoard[ly+2][lx] == 1:
                            finished = True
                        elif ly>16:
                            ly+=1
                            finished = True
                        else:
                            ly+=1
                    copyBoard[ly][lx],copyBoard[ly+1][lx],copyBoard[ly-1][lx],copyBoard[ly-1][lx-1] = 1,1,1,1
                    currentMove.append([[ly,lx],[ly+1,lx],[ly-1,lx],[ly-1,lx-1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    ly=1
                    lx+=1
                if dx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[dy+1][dx] == 1 or copyBoard[dy+1][dx+1] == 1 or copyBoard[dy+2][dx-1] == 1:
                            finished = True
                        elif dy>16:
                            dy+=1
                            finished = True
                        else:
                            dy+=1
                    copyBoard[dy][dx],copyBoard[dy][dx+1],copyBoard[dy][dx-1],copyBoard[dy+1][dx-1] = 1,1,1,1
                    currentMove.append([[dy,dx],[dy,dx+1],[dy,dx-1],[dy+1,dx-1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    dy=0
                    dx+=1
                if ux<=8:
                    finished = False
                    while not finished:
                        if copyBoard[uy+1][ux] == 1 or copyBoard[uy+1][ux+1] == 1 or copyBoard[uy+1][ux-1] == 1:
                            finished = True
                        elif uy>17:
                            uy+=1
                            finished = True
                        else:
                            uy+=1
                    copyBoard[uy][ux],copyBoard[uy][ux-1],copyBoard[uy][ux+1],copyBoard[uy-1][ux+1] = 1,1,1,1
                    currentMove.append([[uy,ux],[uy,ux-1],[uy,ux+1],[uy-1,ux+1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    uy=1
                    ux+=1
                if rx<=8:#8 is 1 block away from right and 9 is touchig right side
                    finished = False
                    while not finished:
                        if copyBoard[ry+2][rx] == 1 or copyBoard[ry+2][rx+1] == 1: #For x + is right - is left | for y + is down - is up
                            finished = True
                        elif ry>16: #16 means 1 before end 17 means touch bottom
                            ry+=1
                            finished = True
                        else:
                            ry+=1
                    copyBoard[ry][rx],copyBoard[ry-1][rx],copyBoard[ry+1][rx],copyBoard[ry+1][rx+1] = 1,1,1,1
                    currentMove.append([[ry,rx],[ry-1,rx],[ry+1,rx],[ry+1,rx+1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    ry=1
                    rx+=1
        #Generates all J boards fine
        elif pieceName == "J":
            rx=0
            ry=1
            lx=1
            ly=1
            dx=1
            dy=0
            ux=1
            uy=1
            possibleBoards = []
            copyBoard = [row[:] for row in self.board]
            allBoards = False
            while allBoards == False:
                if lx>9 and dx>8 and rx>8 and ux>8:
                    allBoards = True
                if lx<=9:
                    finished = False
                    while not finished:
                        if copyBoard[ly+2][lx-1] == 1 or copyBoard[ly+2][lx] == 1:
                            finished = True
                        elif ly>16:
                            ly+=1
                            finished = True
                        else:
                            ly+=1
                    copyBoard[ly][lx],copyBoard[ly+1][lx],copyBoard[ly-1][lx],copyBoard[ly+1][lx-1] = 1,1,1,1
                    currentMove.append([[ly,lx],[ly+1,lx],[ly-1,lx],[ly+1,lx-1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    ly=1
                    lx+=1
                if dx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[dy+1][dx] == 1 or copyBoard[dy+1][dx-1] == 1 or copyBoard[dy+2][dx+1] == 1:
                            finished = True
                        elif dy>16:
                            dy+=1
                            finished = True
                        else:
                            dy+=1
                    copyBoard[dy][dx],copyBoard[dy][dx+1],copyBoard[dy][dx-1],copyBoard[dy+1][dx+1] = 1,1,1,1
                    currentMove.append([[dy,dx],[dy,dx+1],[dy,dx-1],[dy+1,dx+1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    dy=0
                    dx+=1
                if ux<=8:
                    finished = False
                    while not finished:
                        if copyBoard[uy+1][ux] == 1 or copyBoard[uy+1][ux+1] == 1 or copyBoard[uy+1][ux-1] == 1:
                            finished = True
                        elif uy>17:
                            uy+=1
                            finished = True
                        else:
                            uy+=1
                    copyBoard[uy][ux],copyBoard[uy][ux-1],copyBoard[uy][ux+1],copyBoard[uy-1][ux-1] = 1,1,1,1
                    currentMove.append([[uy,ux],[uy,ux-1],[uy,ux+1],[uy-1,ux-1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    uy=1
                    ux+=1
                if rx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[ry+2][rx] == 1 or copyBoard[ry][rx+1] == 1:
                            finished = True
                        elif ry>16: 
                            ry+=1
                            finished = True
                        else:
                            ry+=1
                    copyBoard[ry][rx],copyBoard[ry-1][rx],copyBoard[ry+1][rx],copyBoard[ry-1][rx+1] = 1,1,1,1
                    currentMove.append([[ry,rx],[ry-1,rx],[ry+1,rx],[ry-1,rx+1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    ry=1
                    rx+=1
        #Generates all Z boards fine
        elif pieceName == "Z":
            hx=1
            hy=0
            vx=0
            vy=1
            possibleBoards = []
            copyBoard = [row[:] for row in self.board]
            allBoards = False
            while allBoards == False:
                if hx>8 and vx>8:
                    allBoards = True
                if hx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[hy+1][hx-1] == 1 or copyBoard[hy+2][hx] == 1 or copyBoard[hy+2][hx+1] == 1:
                            finished = True
                        elif hy>16:
                            hy+=1
                            finished = True
                        else:
                            hy+=1
                    copyBoard[hy][hx],copyBoard[hy][hx-1],copyBoard[hy+1][hx],copyBoard[hy+1][hx+1] = 1,1,1,1
                    currentMove.append([[hy,hx],[hy,hx-1],[hy+1,hx],[hy+1,hx+1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    hy=1
                    hx+=1
                if vx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[vy+2][vx] == 1 or copyBoard[vy+1][vx+1] == 1:
                            finished = True
                        elif vy>16:
                            vy+=1
                            finished = True
                        else:
                            vy+=1
                    copyBoard[vy][vx],copyBoard[vy][vx+1],copyBoard[vy+1][vx],copyBoard[vy-1][vx+1] = 1,1,1,1
                    currentMove.append([[vy,vx],[vy,vx+1],[vy+1,vx],[vy-1,vx+1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    vy=1
                    vx+=1
        #Generates all S boards fine
        elif pieceName == "S":
            hx=1
            hy=0
            vx=0
            vy=1
            possibleBoards = []
            copyBoard = [row[:] for row in self.board]
            allBoards = False
            while allBoards == False:
                if hx>8 and vx>8:
                    allBoards = True
                if hx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[hy+1][hx+1] == 1 or copyBoard[hy+2][hx] == 1 or copyBoard[hy+2][hx-1] == 1:
                            finished = True
                        elif hy>16:
                            hy+=1
                            finished = True
                        else:
                            hy+=1
                    copyBoard[hy][hx],copyBoard[hy][hx+1],copyBoard[hy+1][hx],copyBoard[hy+1][hx-1] = 1,1,1,1
                    currentMove.append([[hy,hx],[hy,hx+1],[hy+1,hx],[hy+1,hx-1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    hy=1
                    hx+=1
                if vx<=8:
                    finished = False
                    while not finished:
                        if copyBoard[vy+2][vx+1] == 1 or copyBoard[vy+1][vx] == 1:
                            finished = True
                        elif vy>16:
                            vy+=1
                            finished = True
                        else:
                            vy+=1
                    copyBoard[vy][vx],copyBoard[vy][vx+1],copyBoard[vy-1][vx],copyBoard[vy+1][vx+1] = 1,1,1,1
                    currentMove.append([[vy,vx],[vy,vx+1],[vy-1,vx],[vy+1,vx+1]])
                    possibleBoards.append(copyBoard)
                    copyBoard = [row[:] for row in self.board]
                    vy=1
                    vx+=1
        #Next evaluate all board states that are given to see which one is the best
        if maxScore == None:
            maxScore = float('-inf')
            altAI = False
        else:
            altAI = True#Alternate check is for Held or Next piece evaluation
        for boardNum in range(len(possibleBoards)):
            board = possibleBoards[boardNum]
            score = 0
            maxHeight = 100
            holes = 0
            blocksAboveHoles=0
            wells=0
            clears = 0
            for y in range(len(board)):
                #Line Clear Check
                if all(board[y]):
                    clears+=1
                for x in range(len(board[y])):
                    #Max Height Check
                    if maxHeight>99:
                        if board[y][x]==1:
                            maxHeight=20-y #larger y is lower down

                    #Holes Check
                    if board[y][x]==0 and board[y-1][x]==1 and y>0:
                        holes+=1
                        #Blocks above holes check
                        tempY = y-2
                        finished = False
                        while tempY>0 and not finished:
                            if board[tempY][x]==1:
                                blocksAboveHoles+=1
                            else:
                                finished = True
                            tempY-=1
                    #Wells/Pits Check
                    if board[y][x]==1:
                        if x-1>=0:
                            if board[y][x-1]==0:
                                tmpY = y+1
                                finished = False
                                rWell=0
                                while tmpY<20 and not finished:
                                    if board[tmpY][x-1]==0:
                                        rWell+=1
                                    else:
                                        finished = True
                                    tmpY+=1
                                wells+=rWell**2
                        if x+1<10:
                            if board[y][x+1]==0:
                                tmpY = y+1
                                finished = False
                                lWell=0
                                while tmpY<20 and not finished:
                                    if board[tmpY][x-1]==0:
                                        lWell+=1
                                    else:
                                        finished = True
                                    tmpY+=1
                                wells+=lWell**2
            score-=self.heightW*maxHeight
            score-=self.holesW*holes
            score-=self.blockHolesW*blocksAboveHoles
            score-=self.wellsW*wells
            score+=self.clearsW*clears
            if score > maxScore:
                maxScore = score
                if altAI:
                    self.altBestBoard = board
                    self.altBestBoardCurrentMove = currentMove[boardNum]
                else:
                    self.bestBoard = board
                    self.bestBoardCurrentMove = currentMove[boardNum]
                    self.currentMaxScore = maxScore

#------------------------------------------------------------Genetic Algorithm-------------------------------------------------------
#Genes is maxHeightWeight,holesWeight, blocksAboveHolesWeight, wellsWeight, clearsWeight
def randomF(lower,upper):
    return random.random()*(upper-lower)+lower #Generate random number including floats between 2 numbers

def initialPopulation(popSize): #Generate the inital population
    population = []
    for x in range(popSize):
        chromosome = []
        chromosome.append(randomF(0,10))
        chromosome.append(randomF(0,10))
        chromosome.append(randomF(0,10))
        chromosome.append(randomF(0,10))
        chromosome.append(randomF(0,10))
        population.append(chromosome)
    return population

def fitnessEvaluation(selectedChromosome):#Run the game with the given chromosome values until losing or timing out
    game = Game(selectedChromosome[0],selectedChromosome[1],selectedChromosome[2],selectedChromosome[3],selectedChromosome[4])
    while not game.failed:
        game.AILoop()
    return game.linesCleared

def mutate(child,mutationRate):#Mutation before creating a new population
    mutatedChild = []
    for x in child:
        if random.random()>1-mutationRate:
            mutatedChild.append(random.choice([-1*randomF(0,2),randomF(0,2)])+x)
        else:
            mutatedChild.append(x)
    return mutatedChild

def crossover(p1,p2): #Create a child with attributes from both parents
    child = []
    p1M = 3
    p2M = 2
    p1C=0
    p2C=0
    for x in range(len(p1)):
        if p1C==p1M:
            child.append(p2[x])
            p2C+=1
        elif p2C==p2M:
            child.append(p1[x])
            p1C+=1
        else:
            choice = random.choice(['p1','p2'])
            if choice == 'p1':
                child.append(p1[x])
                p1C+=1
            else:
                child.append(p2[x])
                p2C+=1
    return child

def geneticAlgorithm(popSize,runTime): #Genetic loop until reaching the generation end (runTime)
    population = initialPopulation(popSize)
    iteration=0
    while iteration < runTime:
        iteration+=1
        population = sorted(population, key=lambda x:fitnessEvaluation(x),reverse=True) #Sort by fitness values
        population = population[:popSize//2]
        children = []
        for x in range(len(population)): #Creates the children 2 for each parent and if uneven then create 1 more from the best in the population
            children.append(crossover(population[x],random.choice(population[0:x]+population[x+1:])))
            children.append(crossover(population[x],random.choice(population[0:x]+population[x+1:])))
        if len(children) != popSize:
            children.append(crossover(population[0],random.choice(population[1:])))
        print('Generation:'+str(iteration))
        print('Best of current population:')
        print(population[0])
        print("--------------------------------------------------------")
        if iteration == runTime:
            endPop = population
        population = []
        for x in children:
            population.append(mutate(x,0.05))
    print("Best of all population was")
    print(endPop[0])
    print("Fitness Score:",fitnessEvaluation(population[0]))

#Run algorithm
geneticAlgorithm(50,20)
        
#Best in the end [4.95,7.4,1,1,7.5] (Rounded)

