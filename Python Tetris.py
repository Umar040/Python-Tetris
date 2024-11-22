import pygame
import time
import random

#---------------------------------------Square Class----------------------------------------------------------
class Square:
    #class variables
    #eg. size = 30
    #constructor
    def __init__(self,size,x=600,y=72,colour="white"):
        self.x = x
        self.y = y
        self.size = size
        self.square = pygame.Rect(self.x,self.y,self.size,self.size)
        self.colour = colour

    #Updates class xy and then moves square rect (can use rect.x/rect.y)
    def move(self,x,y):
        self.x+=x
        self.y+=y
        self.square = self.square.move(x,y)

    def ghost(self):
        return pygame.Rect(self.x,self.y,self.size,self.size)

    #Rect method lets class act like a rect for colliderect
    def rect(self):
        return self.square

#------------------------------------------Tetris Pieces----------------------------------------------------------
class TPiece:
    def __init__(self,size):
        self.size = size
        self.name = "T"
        self.squares = [Square(self.size,colour=(138,43,226)),Square(self.size,colour=(138,43,226)),Square(self.size,colour=(138,43,226)),Square(self.size,colour=(138,43,226))]
        self.squares[1].move(-self.size-1,0)#Left
        self.squares[2].move(self.size+1,0)#Right
        self.squares[3].move(0,self.size+1)#Down
        self.rotateNum = 1

    def move(self,x,y):
        for square in self.squares:
            square.move(x,y)

    def rotate(self):
        if self.rotateNum == 1:
            self.squares[2].move(-self.size-1,-self.size-1)
            self.rotateNum+=1
        elif self.rotateNum == 2:
            self.squares[3].move(self.size+1,-self.size-1)
            self.rotateNum+=1
        elif self.rotateNum == 3:
            self.squares[1].move(self.size+1,self.size+1)
            self.rotateNum+=1
        else:
            self.squares[2].move(-self.size-1,+self.size+1)
            self.rotateNum=1
            self.squares[1],self.squares[2],self.squares[3] = self.squares[2],self.squares[3],self.squares[1]

    def unrotate(self):
        if self.rotateNum == 1:
            self.squares[1],self.squares[2],self.squares[3] = self.squares[3],self.squares[1],self.squares[2]
            self.rotateNum=4
            self.squares[2].move(self.size+1,-self.size-1)
        elif self.rotateNum == 2:
            self.rotateNum-=1
            self.squares[2].move(self.size+1,self.size+1)
        elif self.rotateNum == 3:
            self.rotateNum-=1
            self.squares[3].move(-self.size-1,self.size+1)
        else:
            self.rotateNum-=1
            self.squares[1].move(-self.size-1,-self.size-1)

class OPiece:
    def __init__(self,size):
        self.size = size
        self.name = "O"
        self.squares = [Square(self.size,colour=(255,255,0)),Square(self.size,colour=(255,255,0)),Square(self.size,colour=(255,255,0)),Square(self.size,colour=(255,255,0))]
        self.squares[1].move(self.size+1,0)#Right
        self.squares[2].move(0,self.size+1)#Down
        self.squares[3].move(self.size+1,self.size+1)#Bottom Right

    def move(self,x,y):
        for square in self.squares:
            square.move(x,y)

    def rotate(self):
        pass

    def unrotate(self):
        pass

class SPiece:
    def __init__(self,size):
        self.size = size
        self.name = "S"
        self.squares = [Square(self.size,colour=(0,255,0)),Square(self.size,colour=(0,255,0)),Square(self.size,colour=(0,255,0)),Square(self.size,colour=(0,255,0))]
        self.squares[1].move(self.size+1,0)#Right
        self.squares[2].move(0,self.size+1)#Down
        self.squares[3].move(-self.size-1,self.size+1)#Bottom Left
        self.rotateNum = 1

    def move(self,x,y):
        for square in self.squares:
            square.move(x,y)

    def rotate(self):
        if self.rotateNum == 1:
            self.squares[2].move(self.size+1,0)
            self.squares[3].move(self.size+1,2*(-self.size-1))
            self.rotateNum+=1
        else:
            self.squares[2].move(-self.size-1,0)
            self.squares[3].move(-self.size-1,2*(self.size+1))
            self.rotateNum=1

    def unrotate(self):
        if self.rotateNum == 1:
            self.squares[2].move(self.size+1,0)
            self.squares[3].move(self.size+1,2*(-self.size-1))
            self.rotateNum+=1
        else:
            self.squares[2].move(-self.size-1,0)
            self.squares[3].move(-self.size-1,2*(self.size+1))
            self.rotateNum=1

class ZPiece:
    def __init__(self,size):
        self.size = size
        self.name = "Z"
        self.squares = [Square(self.size,colour=(255,0,0)),Square(self.size,colour=(255,0,0)),Square(self.size,colour=(255,0,0)),Square(self.size,colour=(255,0,0))]
        self.squares[1].move(-self.size-1,0)#Left
        self.squares[2].move(0,self.size+1)#Down
        self.squares[3].move(self.size+1,self.size+1)#Bottom Right
        self.rotateNum = 1

    def move(self,x,y):
        for square in self.squares:
            square.move(x,y)

    def rotate(self):
        if self.rotateNum == 1:
            self.squares[1].move(2*(self.size+1),-self.size-1)
            self.squares[3].move(0,-self.size-1)
            self.rotateNum+=1
        else:
            self.squares[1].move(2*(-self.size-1),self.size+1)
            self.squares[3].move(0,self.size+1)
            self.rotateNum=1

    def unrotate(self):
        if self.rotateNum == 1:
            self.squares[1].move(2*(self.size+1),-self.size-1)
            self.squares[3].move(0,-self.size-1)
            self.rotateNum+=1
        else:
            self.squares[1].move(2*(-self.size-1),self.size+1)
            self.squares[3].move(0,self.size+1)
            self.rotateNum=1

class IPiece:
    def __init__(self,size):
        self.size = size
        self.name = "I"
        self.squares = [Square(self.size,colour=(0,255,255)),Square(self.size,colour=(0,255,255)),Square(self.size,colour=(0,255,255)),Square(self.size,colour=(0,255,255))]
        self.squares[1].move(-self.size-1,0)#Left
        self.squares[2].move(self.size+1,0)#Right
        self.squares[3].move(2*(self.size+1),0)#Double Right
        self.rotateNum = 1

    def move(self,x,y):
        for square in self.squares:
            square.move(x,y)

    def rotate(self):
        if self.rotateNum == 1:
            self.squares[1].move(self.size+1,-self.size-1)
            self.squares[2].move(-self.size-1,self.size+1)
            self.squares[3].move(2*(-self.size-1),2*(self.size+1))
            self.rotateNum+=1
        else:
            self.squares[1].move(-self.size-1,self.size+1)
            self.squares[2].move(self.size+1,-self.size-1)
            self.squares[3].move(2*(self.size+1),2*(-self.size-1))
            self.rotateNum=1

    def unrotate(self):
        if self.rotateNum == 1:
            self.squares[1].move(self.size+1,-self.size-1)
            self.squares[2].move(-self.size-1,self.size+1)
            self.squares[3].move(2*(-self.size-1),2*(self.size+1))
            self.rotateNum+=1
        else:
            self.squares[1].move(-self.size-1,self.size+1)
            self.squares[2].move(self.size+1,-self.size-1)
            self.squares[3].move(2*(self.size+1),2*(-self.size-1))
            self.rotateNum=1

class LPiece:
    def __init__(self,size):
        self.size = size
        self.name = "L"
        self.squares = [Square(self.size,colour=(255,127,0)),Square(self.size,colour=(255,127,0)),Square(self.size,colour=(255,127,0)),Square(self.size,colour=(255,127,0))]
        self.squares[1].move(-self.size-1,0)#Left
        self.squares[2].move(self.size+1,0)#Right
        self.squares[3].move(-self.size-1,self.size+1)#Bottom Left
        self.rotateNum = 1

    def move(self,x,y):
        for square in self.squares:
            square.move(x,y)

    def rotate(self):
        if self.rotateNum == 1:
            self.squares[1].move(0,-self.size-1)
            self.squares[2].move(-self.size-1,-self.size-1)
            self.squares[3].move(self.size+1,0)
            self.rotateNum+=1
        elif self.rotateNum == 2:
            self.squares[1].move(0,self.size+1)
            self.squares[2].move(self.size+1,0)
            self.squares[3].move(self.size+1,-self.size-1)
            self.rotateNum+=1
        elif self.rotateNum == 3:
            self.squares[1].move(self.size+1,-self.size-1)
            self.squares[2].move(0,2*(self.size+1))
            self.squares[3].move(-self.size-1,self.size+1)
            self.rotateNum+=1
        else:
            self.squares[1].move(-self.size-1,self.size+1)
            self.squares[2].move(0,-self.size-1)
            self.squares[3].move(-self.size-1,0)
            self.rotateNum=1

    def unrotate(self):
        if self.rotateNum==1:
            self.squares[1].move(self.size+1,-self.size-1)
            self.squares[2].move(0,self.size+1)
            self.squares[3].move(self.size+1,0)
            self.rotateNum=4
        elif self.rotateNum==2:
            self.squares[1].move(0,self.size+1)
            self.squares[2].move(self.size+1,self.size+1)
            self.squares[3].move(-self.size-1,0)
            self.rotateNum-=1
        elif self.rotateNum==3:
            self.squares[1].move(0,-self.size-1)
            self.squares[2].move(-self.size-1,0)
            self.squares[3].move(-self.size-1,self.size+1)
            self.rotateNum-=1
        else:
            self.squares[1].move(-self.size-1,self.size+1)
            self.squares[2].move(0,2*(-self.size-1))
            self.squares[3].move(self.size+1,-self.size-1)

class JPiece:
    def __init__(self,size):
        self.size = size
        self.name = "J"
        self.squares = [Square(self.size,colour=(0,0,255)),Square(self.size,colour=(0,0,255)),Square(self.size,colour=(0,0,255)),Square(self.size,colour=(0,0,255))]
        self.squares[1].move(-self.size-1,0)#Left
        self.squares[2].move(self.size+1,0)#Right
        self.squares[3].move(self.size+1,self.size+1)#Bottom Right
        self.rotateNum = 1

    def move(self,x,y):
        for square in self.squares:
            square.move(x,y)

    def rotate(self):
        if self.rotateNum == 1:
            self.squares[1].move(0,self.size+1)
            self.squares[2].move(-self.size-1,-self.size-1)
            self.squares[3].move(-self.size-1,0)
            self.rotateNum+=1
        elif self.rotateNum == 2:
            self.squares[1].move(0,-self.size-1)
            self.squares[2].move(-self.size-1,0)
            self.squares[3].move(self.size+1,-self.size-1)
            self.rotateNum+=1
        elif self.rotateNum == 3:
            self.squares[1].move(self.size+1,-self.size-1)
            self.squares[2].move(2*(self.size+1),0)
            self.squares[3].move(-self.size-1,self.size+1)
            self.rotateNum+=1
        else:
            self.squares[1].move(-self.size-1,self.size+1)
            self.squares[2].move(0,self.size+1)
            self.squares[3].move(self.size+1,0)
            self.rotateNum=1

    def unrotate(self):
        if self.rotateNum == 1:
            self.squares[1].move(self.size+1,-self.size-1)
            self.squares[2].move(0,-self.size-1)
            self.squares[3].move(-self.size-1,0)
            self.rotateNum=4
        elif self.rotateNum == 2:
            self.squares[1].move(0,-self.size-1)
            self.squares[2].move(self.size+1,self.size+1)
            self.squares[3].move(self.size+1,0)
            self.rotateNum-=1
        elif self.rotateNum == 3:
            self.squares[1].move(0,self.size+1)
            self.squares[2].move(self.size+1,0)
            self.squares[3].move(-self.size-1,self.size+1)
            self.rotateNum-=1
        else:
            self.squares[1].move(-self.size-1,self.size+1)
            self.squares[2].move(2*(-self.size-1),0)
            self.squares[3].move(self.size+1,-self.size-1)
            self.rotateNum-=1

#------------------------------------------------Game Code---------------------------------------------------------------------
class Game:
    def __init__(self,screen,size):
        self.screen = screen
        self.squares = []
        self.dropped = False
        #Board select y then x [y][x]
        self.board = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
        self.size=size
        self.font = pygame.font.SysFont('Calibri',40)
        self.controlsFont = pygame.font.SysFont('Calibri',30)
        self.piecesLeft = ["T","O","S","Z","I","L","J"]
        self.held = None
        self.heldPiece = None
        self.next = None
        self.makePiece()
        self.frameCount = 0
        self.running = True

    def makePiece(self):
        if self.next == None:
            piece = random.choice(self.piecesLeft)
            self.piecesLeft.remove(piece)
            self.next = random.choice(self.piecesLeft)
            self.piecesLeft.remove(self.next)
        else:
            piece = self.next
            self.next = random.choice(self.piecesLeft)
            self.piecesLeft.remove(self.next)
        if len(self.piecesLeft) == 0:
            self.piecesLeft = ["T","O","S","Z","I","L","J"]
        self.currentPiece = self.getPiece(piece)
        self.nextPiece = self.getPiece(self.next)
        self.nextPiece.move(275,50)
        self.makeGhost()
        
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

    def holdPiece(self):
        if self.held == None:
            self.held = self.currentPiece.name
            self.makePiece()
        else:
            self.held, self.currentPiece = self.currentPiece.name, self.getPiece(self.held)
            self.makeGhost()
        self.heldPiece = self.getPiece(self.held)
        self.heldPiece.move(-275,50)

    def killCheck(self):
        if self.board[0][5] == 1 or self.board[0][4] == 1 or self.board[0][6] == 1:
            self.screen.fill("red")
            gameOverText = self.font.render("Game Over",True, (0,0,0))
            self.screen.blit(gameOverText,(520,350))
            pygame.display.flip()
            time.sleep(2)
            self.running = False

    def pieceEventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                collision = False
                if event.key == pygame.K_RIGHT:
                    for square in self.currentPiece.squares: #Instead of piece move then running another loop for collision both together is more efficient
                        square.move(self.size+1,0)
                        if square.x > 600 + (self.size+1)*5 + self.size or square.rect().collidelistall(self.squares):
                            collision = True
                    if collision:
                        self.currentPiece.move(-self.size-1,0)
                    self.makeGhost()
                elif event.key == pygame.K_LEFT:
                    for square in self.currentPiece.squares:
                        square.move(-self.size-1,0)
                        if square.x < 600 - (self.size+1)*4 or square.rect().collidelistall(self.squares):
                            collision = True
                    if collision:
                        self.currentPiece.move(+self.size+1,0)
                    self.makeGhost()
                elif event.key == pygame.K_UP:
                    self.currentPiece.rotate()
                    undo = False
                    for square in self.currentPiece.squares:
                        if square.rect().collidelistall(self.squares) or square.y<72 or square.x<476 or square.x>756:
                            undo = True
                    if undo:
                        self.currentPiece.unrotate()
                    self.makeGhost()
                elif event.key == pygame.K_DOWN:
                    finished = False
                    collide = False
                    while not finished:
                        for square in self.currentPiece.squares:
                            square.move(0,self.size+1)
                            if square.rect().collidelistall(self.squares) or square.y > 661:
                                finished = True
                                collide = True
                            elif square.y > 660:
                                finished = True
                    if collide:
                        self.currentPiece.move(0,-self.size-1)
                    self.dropped = True
                elif event.key == pygame.K_c:
                    self.holdPiece()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def pieceDraw(self):
        self.screen.fill("black")
        borderRect = pygame.Rect(474,70,313,623)
        pygame.draw.rect(self.screen,(255,255,255),borderRect,1)
        nextText = self.font.render("Next:",True,(255,255,255))
        self.font.size
        controlText = [self.controlsFont.render("Controls:",True,(255,255,255)), self.controlsFont.render("Left Arrow = Move Piece Left",True,(255,255,255)), self.controlsFont.render("Right Arrow = Move Piece Right",True,(255,255,255)), self.controlsFont.render("Down Arrow = Drop Piece",True,(255,255,255)), self.controlsFont.render("Up Arrow = Rotate Piece",True,(255,255,255)), self.controlsFont.render("C Key = Hold Piece",True,(255,255,255))]
        for line in range(len(controlText)):
            self.screen.blit(controlText[line],(50,250+(30*line)))
        self.screen.blit(nextText,(850,70))
        heldText = self.font.render("Held:",True,(255,255,255))
        self.screen.blit(heldText,(300,70))
        for square in self.nextPiece.squares:
            pygame.draw.rect(self.screen,square.colour, square.rect())
        if self.heldPiece != None:
            for square in self.heldPiece.squares:
                pygame.draw.rect(self.screen,square.colour, square.rect())
        for rect in self.ghost:
            pygame.draw.rect(self.screen,self.currentPiece.squares[0].colour,rect,1)
        for square in self.squares:
            pygame.draw.rect(self.screen, square.colour, square.rect())
        for square in self.currentPiece.squares:
            pygame.draw.rect(self.screen, square.colour, square.rect())
        pygame.display.flip()

    def multiClearLine(self):
        rowToDelete = []
        squaresToRemove = []
        for square in self.currentPiece.squares:
            self.board[int((square.y - 72)/31)][int((square.x-476)/31)]=1
        for row in range(len(self.board)):
            if all(column==1 for column in self.board[row]):
                rowToDelete.append(row)
        for row in rowToDelete:
            for square in self.squares:
                if square.y == (row*31)+72:
                    squaresToRemove.append(square)
        for square in squaresToRemove:
            self.squares.remove(square)
        for row in rowToDelete:
            tempRow = [0,0,0,0,0,0,0,0,0,0]
            for row2 in range(row+1):
                self.board[row2],tempRow = tempRow,self.board[row2]
            for square in self.squares:
                if square.y < (row*31)+72:
                    square.move(0,31)

    def makeGhost(self):
        self.ghost=[]
        for square in self.currentPiece.squares:
            self.ghost.append(square.ghost())
        finished = False
        collide = False
        while not finished:
            for rectNum in range(len(self.ghost)):
                self.ghost[rectNum] = self.ghost[rectNum].move(0,self.size+1)
                if self.ghost[rectNum].collidelistall(self.squares) or self.ghost[rectNum].y > 661:
                    finished = True
                    collide = True
                elif self.ghost[rectNum].y > 660:
                    finished = True
        if collide:
            for rectNum in range(len(self.ghost)):
                self.ghost[rectNum] = self.ghost[rectNum].move(0,-self.size-1)
        
    def pieceLoop(self):
        self.pieceEventHandler()
        self.pieceDraw()
        self.frameCount+=1
        if self.frameCount == 30 or self.dropped:
            add = False
            collision = False
            for square in self.currentPiece.squares:
                if square.y > 660:
                    add = True
            if add:
                self.squares.extend(self.currentPiece.squares)
                self.multiClearLine()
                self.makePiece()
            else:
                for square in self.currentPiece.squares:
                    square.move(0,self.size+1)
                    if square.rect().collidelistall(self.squares):
                        collision=True
            if collision:
                self.currentPiece.move(0,-self.size-1)
                self.squares.extend(self.currentPiece.squares)
                self.multiClearLine()
                self.makePiece()
            self.killCheck()
            self.frameCount=0
            self.dropped = False


#------------------------------------------------------------------Game Loop------------------------------------------------------
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game = Game(screen,30)
while game.running:
    game.pieceLoop()
    clock.tick(60)
print("Game Over")
    
pygame.quit()
