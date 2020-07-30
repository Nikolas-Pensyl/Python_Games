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
coordsClicked = [-1, -1]
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
offset = 4

class Tile:
    def __init__(self, y_pos, x_pos, value):
        self.width = 100 -offset #the minus four is to give little space between each block
        self.height = 100 -offset
        self.x = x_pos
        self.y = y_pos
        self.pos_x = self.x*100+offset/2
        self.pos_y = self.y*100+offset/2
        self.val = value
        self.clicked = False
    def draw(self, tiles):
        clr = colors[self.val-1]
        text = font.render(str(self.val), False, white)
        if not self.clicked:
           pygame.draw.rect(screen, clr, [int(self.x*100+2), int(self.y*100+2), int(self.width), int(self.height)])
           screen.blit(text, [int(self.x*100+self.width/2-text.get_width()/2), int(self.y*100+self.height/2-text.get_height()/2)])
        else:
            pygame.draw.rect(screen, clr, [int(self.pos_x), int(self.pos_y), int(self.width), int(self.height)])
            screen.blit(text, [int(self.pos_x+self.width/2-text.get_width()/2), int(self.pos_y+self.height/2-text.get_height()/2)])
    def moveUp(self, tiles):
        self.y = self.y - 1
        self.pos_x = self.x*100-self.width/2
        self.pos_y = self.y*100-self.height/2
        if not self.y == -1:
            return exchange(self, tiles, 0, -1)
        else:
            game_over = True
            return tiles
    def gravity(self, tiles):
        if not self.y == 7:
            if tiles[self.y+1][self.x] is None:
                self.y = self.y + 1
                self.pos_x = self.x*100
                self.pos_y = self.y*100
                return exchange(self, tiles, 0, 1)
        return tiles
    def merge(self, tiles):
        tileY = int((self.pos_y+self.height/2)/100)
        tileX = int((self.pos_x+self.width/2)/100)
        if self.clicked and not tiles[tileY][tileX] is None and tiles[tileY][tileX].val == self.val and (not tileY == self.y or not tileX == self.x):
            tiles[tileY][tileX].val = tiles[tileY][tileX].val + 1
            return tiles, True, False, [-1, -1]
        return tiles, False, True, [self.x, self.y]
    def updatePos(self):
        if self.clicked:
            self.pos_x = getMouseX()-self.width/2
            self.pos_y = getMouseY()-self.height/2
            print((self.pos_x+self.width/2)/100, (self.pos_y+self.height/2)/100, sep=' ')
            if self.pos_x>500:
                self.pos_x = 502
            if self.pos_y>700:
                self.pos_y = 702
            if self.pos_x<0:
                self.pos_x = 0
            if self.pos_y<0:
                self.pos_y = 0
    def setNewCoords(self, tiles, coordsClicked):
        tiles[int((self.pos_y+self.height/2)/100)][int((self.pos_x+self.width/2)/100)] = self
        self.x = int((self.pos_x+self.width/2)/100)
        self.y = int((self.pos_y+self.height/2)/100)
        if not coordsClicked[0] == self.x or not coordsClicked[1] == self.y:
            tiles[coordsClicked[1]][coordsClicked[0]] = None
        return tiles
    def noSharing(self, tiles, coordsClicked):
        return tiles

def getMouseX():
    return pygame.mouse.get_pos()[0]

def getMouseY():
    return pygame.mouse.get_pos()[1]

def mouseInBounds():
    return getMouseY()<800 and getMouseX()<600

def coordInBounds(x_pos, y_pos):
    return y_pos/100<800 and x_pos/100<600

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
    global tiles, mouseDown, coordsClicked
    while not game_over:
        dontFreeze()
        
        if pygame.mouse.get_pressed()[0] and not mouseDown and mouseInBounds() and not tiles[int(getMouseY()/100)][int(getMouseX()/100)] is None:
            mouseDown = pygame.mouse.get_pressed()[0]
            coordsClicked[0] = int(getMouseX()/100)
            coordsClicked[1] = int(getMouseY()/100)
        elif not pygame.mouse.get_pressed()[0] and mouseDown:
            tiles[coordsClicked[1]][coordsClicked[0]].clicked = False
            tiles = tiles[coordsClicked[1]][coordsClicked[0]].setNewCoords(tiles, coordsClicked)
            mouseDown = False 
            coordsClicked = [-1, -1]
        for y in range(len(tiles)):
            for x in range(len(tiles[y])-1, -1, -1):
                if not tiles[y][x] == None:
                    if y == coordsClicked[1] and x == coordsClicked[0]:
                        tiles[y][x].clicked = True
                        tiles[y][x].updatePos()
                    tiles[y][x].draw(tiles)
                    if time_left == 0 and not mouseDown and not tiles[y+1][x] is None:
                        tiles = tiles[y][x].moveUp(tiles)
                        if game_over:
                            break
                    if not mouseDown:
                        tiles = tiles[y][x].gravity(tiles)
                        if not tiles[y][x] == None and not y == 7 and not tiles[y+1][x] is None and tiles[y][x].val == tiles[y+1][x].val:
                            tiles[y][x] = None
                            tiles[y+1][x].val = tiles[y+1][x].val + 1
                    else: 
                        
                        if y == coordsClicked[1] and x == coordsClicked[0]:
                            merger = False
                            #tiles, merger, mouseDown, coordsClicked = tiles[y][x].merge(tiles)
                            if merger:
                                tiles[y][x] = None
            if game_over:
                break
        pygame.display.flip()
        pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
        pygame.draw.line(screen, colors[3], [0, 800], [600, 800])
        pygame.draw.line(screen, colors[3], [600, 0], [600, 800])
        pygame.draw.line(screen, colors[3], [0, 0], [600, 0])

tiles[3][3] = Tile(3, 3, 5)
tiles[2][2] = Tile(2, 2, 5)
tiles[4][4] = Tile(4, 4, 5)
tiles[5][5] = Tile(5, 5, 5)
tiles[6][1] = Tile(6, 1, 5)
tiles[7][5] = Tile(7, 5, 5)
play()
print(tiles)
