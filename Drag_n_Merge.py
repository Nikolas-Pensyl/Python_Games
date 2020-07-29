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

cyan = 0, 255, 255
green = 0, 255, 0
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
yellow = 0, 255, 255
orange = 255, 128, 0
purple = 153, 0, 153
pink = 255, 0, 127

colors = [cyan, green, white, red, yellow, orange, purple, pink, black]
background = len(colors)-1

level = 0

class Tile:
    def __init__(self, y_pos, x_pos, value):
        self.width = 100 -4 #the minus four is to give little space between each block
        self.height = 100 -4
        self.x = x_pos
        self.y = y_pos
        self.val = value
        self.clicked = False
    def draw(self, tiles):
        clr = colors[self.val-1]
        text = font.render(str(self.val), False, white)
        if not self.clicked:
           pygame.draw.rect(screen, clr, [int(self.x*100+2), int(self.y*100+2), int(self.width), int(self.height)])
           screen.blit(text, [int(self.x*100+self.width/2-text.get_width()/2), int(self.y*100+self.height/2-text.get_height()/2)])
        else:
            pygame.draw.rect(screen, clr, [int(pygame.mouse.get_pos()[0]-50), int(pygame.mouse.get_pos()[1]-50), int(self.width), int(self.height)])
            screen.blit(text, [int(pygame.mouse.get_pos()[0]-text.get_width()/2), int(pygame.mouse.get_pos()[1]-text.get_height()/2)])
    def moveUp(self, tiles):
        self.y = self.y - 1
        if not self.y == -1:
            return exchange(self, tiles, 0, -1)
        else:
            game_over = True
            return tiles
    def gravity(self, tiles):
        if not self.y == 7:
            if tiles[self.y+1][self.x] is None:
                self.y = self.y + 1
                return exchange(self, tiles, 0, 1)
        return tiles
    def isClicked(self, mouseDown):
        if pygame.mouse.get_pressed()[0]:
            if self.clicked and mouseDown:
                
                return True
            elif not mouseDown and not self.clicked and pygame.mouse.get_pos()[0]>self.x*100 and pygame.mouse.get_pos()[0]<self.x*100+self.width and pygame.mouse.get_pos()[1]>self.y*100 and pygame.mouse.get_pos()[1]<self.y*100+self.height:
                self.clicked = True
                mouseDown = True
                print("test")
            if self.x == 4:
                print(self.clicked)
            return True 
        else:
            mouseDown = False
            self.clicked = False
            return False


def exchange(tile, tiles, changeX, changeY):
    tiles[tile.y][tile.x] = tile
    pygame.draw.rect(screen, colors[background], [int(tile.x-changeX*100+2), int(tile.y-changeY*100+2), int(tile.width), int(tile.height)])
    tiles[tile.y-changeY][tile.x-changeX] = None
    return tiles


def dontFreeze():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

def play():
    global tiles, mouseDown
    while not game_over:
        dontFreeze()
        for y in range(len(tiles)):
            for x in range(len(tiles[y])):
                if not tiles[y][x] == None:
                    tiles[y][x].draw(tiles)
                    mouseDown = tiles[y][x].isClicked(mouseDown)
                    if time_left == 0 and not mouseDown and not tiles[y+1][x] is None:
                        tiles = tiles[y][x].moveUp(tiles)
                        if game_over:
                            break
                    if not mouseDown:
                        tiles = tiles[y][x].gravity(tiles)
                        if not tiles[y][x] == None and not y == 7 and not tiles[y+1][x] is None and tiles[y][x].val == tiles[y+1][x].val:
                            tiles[y][x] = None
                            tiles[y+1][x].val = tiles[y+1][x].val + 1
            if game_over:
                break
        pygame.display.flip()
        pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])

#tiles[3][2] = Tile(3, 2, 5)
tiles[2][2] = Tile(2, 2, 5)
tiles[4][4] = Tile(4, 4, 5)
play()
print(tiles)
