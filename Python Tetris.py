import pygame
import os

class Square:
    #class variables
    #eg. size = 30
    #constructor
    def __init__(self,size):
        self.x = 600
        self.y = 72
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
        self.makePiece("T")
        self.frameCount = 0
        self.running = True

    def makePiece(self, piece):
        if piece == "T":
            self.currentSquares = [Square(self.size),Square(self.size),Square(self.size),Square(self.size)]
            self.currentSquares[1].move(-self.size-1,0)
            self.currentSquares[2].move(self.size+1,0)
            self.currentSquares[3].move(0,self.size+1)
            

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
            for square in self.currentSquares:
                if square.y > 660:
                    add = True
            if add:
                self.squares.extend(self.currentSquares)
                self.makePiece("T")
            else:
                for square in self.currentSquares:
                    square.move(0,self.size+1)
            self.frameCount=0
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game = Game(screen,30)
while game.running:
    game.multiLoop()
    clock.tick(60)
    
pygame.quit()

#Bug when down at start block builds up but fixed with kill when top block filled
