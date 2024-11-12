import pygame
import os

#Ghost squares that return squares that exact position then make equal to ghost list then drop then udpate every click

class Square:
    #class variables
    #eg. size = 30
    #constructor
    def __init__(self,size,x=600,y=72):
        self.x = x
        self.y = y
        self.size = size
        self.square = pygame.Rect(self.x,self.y,self.size,self.size)
        self.colour = "white"

    #Updates class xy and then moves square rect (can use rect.x/rect.y)
    def move(self,x,y):
        self.x+=x
        self.y+=y
        self.square = self.square.move(x,y)

    #Rect method lets class act like a rect for colliderect
    def rect(self):
        return self.square

class TPiece:
    def __init__(self,size):
        self.size = size
        self.squares = [Square(self.size),Square(self.size),Square(self.size),Square(self.size)]
        self.squares[1].move(-self.size-1,0)#left
        self.squares[2].move(self.size+1,0)#right
        self.squares[3].move(0,self.size+1)#down
        self.rotateNum = 1
        for square in self.squares:
            square.colour = (255, 255, 0)

    def move(self,x,y):
        for square in self.squares:
            square.move(x,y)
            
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

class Game:
    def __init__(self,screen,size):
        self.screen = screen
        self.squares = []
        #Board select y then x [y][x]
        self.board = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
        self.size=size
        self.currentSquare = Square(size)
        self.currentPiece = TPiece(size)
        self.makePiece("T")
        self.ghost=[]
        self.frameCount = 0
        self.running = True

    def makePiece(self, piece):
        if piece == "T":
            self.currentPiece = TPiece(self.size)
            

    def multiEventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                collision = False
                if event.key == pygame.K_RIGHT:
                    for square in self.currentSquares:
                        square.move(self.size+1,0)
                        if square.x > 600 + (self.size+1)*5 + self.size or square.rect().collidelistall(self.squares):
                            collision = True
                    if collision:
                        for square in self.currentSquares:
                            square.move(-self.size-1,0)
                elif event.key == pygame.K_LEFT:
                    for square in self.currentSquares:
                        square.move(-self.size-1,0)
                        if square.x < 600 - (self.size+1)*4 or square.rect().collidelistall(self.squares):
                            collision = True
                    if collision:
                        for square in self.currentSquares:
                            square.move(+self.size+1,0)

    def pieceEventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                collision = False
                if event.key == pygame.K_RIGHT:
                    for square in self.currentPiece.squares: #Instead of piece move then running another loop for collision both together is more efficient
                        square.move(self.size+1,0)
                        if square.x > 600 + (self.size+1)*5 + self.size or square.rect().collidelistall(self.squares):
                            collision = True
                    if collision:
                        self.currentPiece.move(-self.size-1,0)
                elif event.key == pygame.K_LEFT:
                    for square in self.currentPiece.squares:
                        square.move(-self.size-1,0)
                        if square.x < 600 - (self.size+1)*4 or square.rect().collidelistall(self.squares):
                            collision = True
                    if collision:
                        self.currentPiece.move(+self.size+1,0)
                elif event.key == pygame.K_UP:
                    self.currentPiece.rotate()
                    undo = False
                    for square in self.currentPiece.squares:
                        if square.rect().collidelistall(self.squares) or square.y<72 or square.x<476 or square.x>756:
                            undo = True
                    if undo:
                        self.currentPiece.unrotate()
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
                        
                    
    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    #If out of bound for game then pass
                    if self.currentSquare.x + self.size*2+1 > 600 + (self.size+1)*5 + self.size:
                        pass
                    else:
                        #Move square and check if it collides and if it does move it back else carry on
                        self.currentSquare.move(self.size+1,0)
                        if self.currentSquare.rect().collidelistall(self.squares):
                            self.currentSquare.move(-self.size-1,0)
                elif event.key == pygame.K_LEFT:
                    if self.currentSquare.x - self.size-1 < 600 - (self.size+1)*4:
                        pass
                    else:
                        self.currentSquare.move(-self.size-1,0)
                        if self.currentSquare.rect().collidelistall(self.squares):
                            self.currentSquare.move(self.size+1,0)
                elif event.key == pygame.K_DOWN:
                    #While the square has not hit another square or not gone out of the game bounds keep going down
                    while not self.currentSquare.rect().collidelistall(self.squares) and not self.currentSquare.y > 691:
                        self.currentSquare.move(0,self.size+1)
                    self.currentSquare.move(0,-self.size-1)
            
    def draw(self):
        self.screen.fill("black")
        for x in self.squares:
            pygame.draw.rect(self.screen, x.colour, x.rect())
        pygame.draw.rect(self.screen,"white",self.currentSquare.rect()) 
        pygame.display.flip()

    def multiDraw(self):
        self.screen.fill("black")
        for square in self.squares:
            pygame.draw.rect(self.screen, square.colour, square.rect())
        for square in self.currentSquares:
            pygame.draw.rect(self.screen, square.colour, square.rect())
        pygame.display.flip()

    def pieceDraw(self):
        self.screen.fill("black")
        borderRect = pygame.Rect(474,70,313,623)
        pygame.draw.rect(self.screen,(255,255,255),borderRect,1)
        for square in self.squares:
            pygame.draw.rect(self.screen, square.colour, square.rect())
        for square in self.currentPiece.squares:
            pygame.draw.rect(self.screen, square.colour, square.rect())
        pygame.display.flip()
        
    #Original plan was to add all square y to a dictionary and and any duplicate add them up then when reaching 10 remove all y in that row then move rest down but now going to use an
    #array to track the game board
    def clearLine(self):
        rowToDelete = []
        squaresToRemove = []
        self.board[int((self.currentSquare.y - 72)/31)][int((self.currentSquare.x-476)/31)]=1
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
            tempRow2 = []
            for row2 in range(row+1):
                tempRow2 = self.board[row2]
                self.board[row2] = tempRow
                tempRow = tempRow2
            for square in self.squares:
                if square.y < (row*31)+72:
                    square.move(0,31)

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
        
             
    def loop(self):
        self.eventHandler()
        self.draw()
        self.frameCount += 1
        if self.frameCount == 30:
            if self.currentSquare.y > 660:
                self.squares.append(self.currentSquare)
                self.clearLine()
                self.currentSquare = Square(self.size)
            else:
                self.currentSquare.move(0,self.size+1)
                if self.currentSquare.rect().collidelistall(self.squares):
                    self.currentSquare.move(0,-self.size-1)
                    self.squares.append(self.currentSquare)
                    self.clearLine()
                    self.currentSquare = Square(self.size)
            self.frameCount = 0
            
    def multiLoop(self):
        self.multiEventHandler()
        self.multiDraw()
        self.frameCount+=1
        if self.frameCount == 30:
            add = False
            collision = False
            for square in self.currentSquares:
                if square.y > 660:
                    add = True
            if add:
                self.squares.extend(self.currentSquares)
                self.multiClearLine()
                self.makePiece("T")
            else:
                for square in self.currentSquares:
                    square.move(0,self.size+1)
                    if square.rect().collidelistall(self.squares):
                        collision=True
            if collision:
                for square in self.currentSquares:
                    square.move(0,-self.size-1)
                self.squares.extend(self.currentSquares)
                self.multiClearLine()
                self.makePiece("T")
            self.frameCount=0

    def pieceLoop(self):
        self.pieceEventHandler()
        self.pieceDraw()
        self.frameCount+=1
        if self.frameCount == 30:
            add = False
            collision = False
            for square in self.currentPiece.squares:
                if square.y > 660:
                    add = True
            if add:
                self.squares.extend(self.currentPiece.squares)
                self.multiClearLine()
                self.makePiece("T")
            else:
                for square in self.currentPiece.squares:
                    square.move(0,self.size+1)
                    if square.rect().collidelistall(self.squares):
                        collision=True
            if collision:
                self.currentPiece.move(0,-self.size-1)
                self.squares.extend(self.currentPiece.squares)
                self.multiClearLine()
                self.makePiece("T")
            self.frameCount=0
        
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game = Game(screen,30)
while game.running:
    game.pieceLoop()
    clock.tick(60)
    
pygame.quit()

#Bug when down at start block builds up but fixed with kill when top block filled
