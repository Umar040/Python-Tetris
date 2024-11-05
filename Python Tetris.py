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

    def move(self,x,y):
        self.x+=x
        self.y+=y
        self.square = self.square.move(x,y)

    def rect(self):
        return self.square

class Game:
    def __init__(self,screen,size):
        self.screen = screen
        self.squares = []
        self.yDict = {}
        self.size=size
        self.currentSquare = Square(size)
        self.frameCount = 0
        self.running = True

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.currentSquare.x + self.size*2+1 > 600 + (self.size+1)*5 + self.size:
                        pass
                    else:
                        self.currentSquare.move(self.size+1,0)
                        if self.currentSquare.rect().collidelistall(self.squares):
                            self.currentSquare.move(-self.size-1,0)
                        print(self.currentSquare.x)
                elif event.key == pygame.K_LEFT:
                    if self.currentSquare.x - self.size-1 < 600 - (self.size+1)*4:
                        pass
                    else:
                        self.currentSquare.move(-self.size-1,0)
                        if self.currentSquare.rect().collidelistall(self.squares):
                            self.currentSquare.move(self.size+1,0)
                elif event.key == pygame.K_DOWN:
                    while not self.currentSquare.rect().collidelistall(self.squares) and not self.currentSquare.y > 660:
                        self.currentSquare.move(0,self.size+1)
                    self.currentSquare.move(0,-self.size-1)
            
    def draw(self):
        self.screen.fill("black")
        for x in self.squares:
            pygame.draw.rect(self.screen, x.colour, x.rect())
        pygame.draw.rect(self.screen,"white",self.currentSquare.rect()) 
        pygame.display.flip()

    def clearLine(self):
        self.yDict
        

    def loop(self):
        self.eventHandler()
        self.draw()
        self.frameCount += 1
        if self.frameCount == 30:
            if self.currentSquare.y > 660:
                print(self.currentSquare.y)
                self.squares.append(self.currentSquare)
                self.currentSquare = Square(self.size)
            else:
                self.currentSquare.move(0,self.size+1)
                if self.currentSquare.rect().collidelistall(self.squares):
                    self.currentSquare.move(0,-self.size-1)
                    self.squares.append(self.currentSquare)
                    self.clearLine()
                    self.currentSquare = Square(self.size)
            self.frameCount = 0
        
        

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game = Game(screen,30)
while game.running:
    game.loop()
    clock.tick(60)
    
pygame.quit()
