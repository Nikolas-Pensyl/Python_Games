#Written by: Nikolas Pensyl
#Started on: 7/29/2020
#Last Modified: 7/29/2020
import sys, pygame, math
from random import randint 
from time import time, sleep
pygame.init()

size = screen_width, screen_height = 800, 1000 #size of board

screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("comicsansms", 45)
tiles = [[None for x in range(6)] for y in range(8)]

prev_time = 0
time_left = 1
mouseDown = False
game_over = False

cyan = 0, 50, 255
green = 0, 255, 0
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
yellow = 0, 255, 255
orange = 255, 165, 0
purple = 130, 0, 255
pink = 255, 0, 255

colors = [cyan, green, white, red, yellow, orange, purple, pink, black]
background = len(colors)-1

level = 0

class Tile:
    def __init__(self, x_pos, y_pos, value):
        self.width = 100 -4 #the minus four is to give little space between each block
        self.height = 100 -4
        self.x = x_pos
        self.y = y_pos
        self.val = value
        self.clicked = False
    def draw(self, tiles):
        if not self.clicked:
          pygame.draw.rect(screen, red, [int(self.x*100+2), int(self.y*100+2), int(self.width), int(self.height)])
        else:
            pygame.draw.rect(screen, red, [int(pygame.mouse.get_pos()[0]-50), int(pygame.mouse.get_pos()[1]-50), int(self.width), int(self.height)])
    def moveUp(self, tiles):
        self.y = self.y - 1
        if not self.y == -1:
            return self.exchange(tiles)
        else:
            game_over = True
            return tiles
    def gravity(self, tiles):
        print(str(self.y))
        if not self.y == 7:
            if tiles[self.x][self.y] is None:
                self.y = self.y + 1
    def isClicked(self, mouseDown):
        if pygame.mouse.get_pressed()[0] and not mouseDown and pygame.mouse.get_pos()[0]>self.x*100 and pygame.mouse.get_pos()[0]<self.x*100+self.width and pygame.mouse.get_pos()[1]>self.y*100 and pygame.mouse.get_pos()[1]<self.y*100+self.height:
            self.clicked = True
            mouseDown = True
            return True
        if pygame.mouse.get_pressed()[0] and mouseDown:
            return True
        if self.clicked and not pygame.mouse.get_pressed()[0]:
            mouseDown = False
            self.clicked = False
        return False
    def exchange(self, tiles):
        
        return tiles


def dontFreeze():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

def play():
    global tiles
    while not game_over:
        dontFreeze()
        for x in range(len(tiles)):
            for y in range(len(tiles[x])):
                if not tiles[x][y] is None:
                    if tiles[x][y].isClicked(mouseDown):
                        print("test")
                    elif not mouseDown and tiles[x][y].isClicked(mouseDown):
                        print("test")
                    else: 
                        tiles[x][y].gravity(tiles)
                    if time_left == 0 and not mouseDown:
                        tiles = moveUp(tiles)
                        if game_over:
                            break
                    tiles[x][y].draw(tiles)
            if game_over:
                break
        pygame.display.flip()
        pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])

tiles[1][1] = Tile(1, 1, 5)
tiles[0][2] = Tile(0, 2, 5)
play()
