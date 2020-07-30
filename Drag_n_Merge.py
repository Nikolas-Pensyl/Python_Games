#Written by: Nikolas Pensyl
#Started on: 7/29/2020
#Last Modified: 7/29/2020
import sys, pygame, math
from random import randint 
from time import time, sleep
pygame.init()

size = screen_width, screen_height = 800, 1000 #size of board
boardOffSetX = 100
boardOffSetY = 190

screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("comicsansms", 45)
tiles = [[None for x in range(6)] for y in range(8)]

prev_time = 0
timeLeft = 10
next_time = time()+10
mouseDown = False
coordsClicked = [-1, -1]
game_over = False
movingTile = None
maxTile = 5

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
           pygame.draw.rect(screen, clr, [int(self.x*100+(offset/2)+boardOffSetX), int(self.y*100+(offset/2)+boardOffSetY), int(self.width), int(self.height)])
           screen.blit(text, [int(self.x*100+self.width/2-text.get_width()/2+boardOffSetX), int(self.y*100+self.height/2-text.get_height()/2+boardOffSetY)])
        else:
            pygame.draw.rect(screen, clr, [int(self.pos_x-self.width/2+boardOffSetX+(offset/2)), int(self.pos_y-self.height/2+boardOffSetY+(offset/2)), int(self.width), int(self.height)])
            screen.blit(text, [int(self.pos_x-text.get_width()/2+boardOffSetX), int(self.pos_y-text.get_height()/2+boardOffSetY)])
    def moveUp(self, tiles):
        global game_over
        self.y = self.y - 1
        self.pos_x = self.x*100+self.width/2
        self.pos_y = self.y*100+self.height/2
        if not self.y == -1:
            return exchange(self, tiles, 0, -1)
        else:
            game_over = True
            return tiles
    def gravity(self, tiles):
        if not self.y == 7:
            if tiles[self.y+1][self.x] is None:
                self.y = self.y + 1
                self.pos_x = self.x*100+self.width/2
                self.pos_y = self.y*100+self.width/2
                return exchange(self, tiles, 0, 1)
        return tiles
    def merge(self, tiles, maxTile):
        tileY = int(self.pos_y/100)
        tileX = int(self.pos_x/100)
        if self.clicked and not tiles[tileY][tileX] is None and tiles[tileY][tileX].val == self.val and (not tileY == self.y or not tileX == self.x):
            tiles[tileY][tileX].val = tiles[tileY][tileX].val + 1
            if tiles[tileY][tileX].val>maxTile:
                maxTile = tiles[tileY][tileX].val
            return tiles, True, False, [-1, -1], maxTile
        return tiles, False, True, [self.x, self.y], maxTile       
    def setNewCoords(self, tiles, coordsClicked):
        tiles[int(self.pos_y/100)][int(self.pos_x/100)] = self
        self.x = int(self.pos_x/100)
        self.y = int(self.pos_y/100)
        if not coordsClicked[0] == self.x or not coordsClicked[1] == self.y:
            tiles[coordsClicked[1]][coordsClicked[0]] = None
        return tiles
    def noSharing(self, tiles):
        minY = getMinY(tiles, self.pos_x, self.pos_y, self)
        maxY = getMaxY(tiles, self.pos_x, self.pos_y, self)
        minX = getMinX(tiles, self.pos_x, self.pos_y, self)
        maxX = getMaxX(tiles, self.pos_x, self.pos_y, self)

        if getMouseX()>maxX:
            self.pos_x = maxX
        elif getMouseX()<minX:
            self.pos_x = minX
        else:
            self.pos_x = getMouseX()
        if getMouseY()>maxY:
            self.pos_y = maxY
        elif getMouseY()<minY:
            self.pos_y = minY
        else:
            self.pos_y = getMouseY()
        self.x = int(self.pos_x/100)
        self.y = int(self.pos_x/100)
        return tiles

def getMaxX(tiles, currentX, currentY, tile):
    maxX = currentX//100
    top = False
    bottom = False
    if currentY%100<48 and currentY>100:
        top = True
    elif currentY%100>52 and currentY<700:
        bottom = True
    if not currentX//100 == 5:
        for i in range(int(currentX/100)+1, len(tiles[int(currentY/100)])):
            if not tiles[int(currentY/100)][i] is None and not tiles[int(currentY/100)][i].val == tile.val:
                break
            if top and not tiles[int(currentY/100)-1][i] is None and not tiles[int(currentY/100)-1][i].val == tile.val:
                break
            if bottom and not tiles[int(currentY/100)+1][i] is None and not tiles[int(currentY/100)+1][i].val == tile.val:
                break
            maxX = i
        return maxX*100+tile.width/2
    else:
        return 600-tile.width/2

def getMinX(tiles, currentX, currentY, tile):
    minX = currentX//100
    top = False
    bottom = False
    if currentY%100<48 and currentY>100:
        top = True
    elif currentY%100>52 and currentY<700:
        bottom = True
    if not currentX//100 == 0:
        for i in range(int(currentX/100)-1, -1, -1):
            if not tiles[int(currentY/100)][i] is None and not tiles[int(currentY/100)][i].val == tile.val:
                break
            if top and not tiles[int(currentY/100)-1][i] is None and not tiles[int(currentY/100)-1][i].val == tile.val:
                break
            if bottom and not tiles[int(currentY/100)+1][i] is None and not tiles[int(currentY/100)+1][i].val == tile.val:
                break
            minX = i
        return minX*100+tile.width/2
    else:
        return tile.width/2

def getMaxY(tiles, currentX, currentY, tile):
    maxY = currentY//100
    left = False
    right = False
    if currentX%100<48 and currentX>100:
        left = True
    elif currentX%100>52 and currentX<500:
        right = True
    if not currentY//100 == 7:
        for i in range(int(currentY/100)+1, len(tiles)):
            if not tiles[i][int(currentX/100)] is None and not tiles[i][int(currentX/100)].val == tile.val:
                break
            if left and not tiles[i][int(currentX/100)-1] is None and not tiles[i][int(currentX/100)-1].val == tile.val:
                break
            if right and not tiles[i][int(currentX/100)+1] is None and not tiles[i][int(currentX/100)+1].val == tile.val:
                break
            maxY = i
        return maxY*100+tile.height/2
    else:
        return 800-tile.height/2

def getMinY(tiles, currentX, currentY, tile):
    minY = currentY//100
    left = False
    right = False
    if currentX%100<48 and currentX>100:
        left = True
    elif currentX%100>52 and currentX<500:
        right = True
    if not currentY//100 == 0:
        for i in range(int(currentY/100)-1, -1, -1):
            if not tiles[i][int(currentX/100)] is None and not tiles[i][int(currentX/100)].val == tile.val:
                break
            if left and not tiles[i][int(currentX/100)-1] is None and not tiles[i][int(currentX/100)-1].val == tile.val:
                break
            if right and not tiles[i][int(currentX/100)+1] is None and not tiles[i][int(currentX/100)+1].val == tile.val:
                break
            minY = i
        return minY*100+tile.height/2
    else:
        return tile.height/2
        

def getMouseX():
    return pygame.mouse.get_pos()[0]- boardOffSetX

def getMouseY():
    return pygame.mouse.get_pos()[1]-boardOffSetY

def getMouseRelX():
    return pygame.mouse.get_rel()[0]

def getMouseRelY():
    return pygame.mouse.get_rel()[1]

def mouseInBounds():
    return getMouseY()<800 and getMouseX()<600

def coordInBounds(x_pos, y_pos):
    return y_pos/100<800 and x_pos/100<600

def exchange(tile, tiles, changeX, changeY):
    tiles[tile.y][tile.x] = tile
    tiles[tile.y-changeY][tile.x-changeX] = None
    return tiles

def dontFreeze():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

def drawStuff(screen):
    pygame.draw.rect(screen, colors[2], [25, 990-int(timeLeft*80), 50, int(timeLeft*80)])
    pygame.draw.rect(screen, colors[2], [25, 190, 50, 800], 5)
    pygame.draw.rect(screen, colors[2], [0+boardOffSetX, 0+boardOffSetY, 600, 800], 4)
    text = font.render("Round: " + str(level), False, white)
    screen.blit(text, [int((screen_width/8)*7-text.get_width()/2), int(screen_height/8-text.get_height()/2)])
    return screen


def play():
    global maxTile, screen, tiles, mouseDown, coordsClicked, movingTile, timeLeft, level, next_time, game_over
    while not game_over:
        dontFreeze()
        screen = drawStuff(screen)
        if pygame.mouse.get_pressed()[0] and not mouseDown and mouseInBounds() and not tiles[int(getMouseY()/100)][int(getMouseX()/100)] is None:
            mouseDown = pygame.mouse.get_pressed()[0]
            coordsClicked[0] = int(getMouseX()/100)
            coordsClicked[1] = int(getMouseY()/100)
            getMouseRelX()
            getMouseRelY()
            movingTile = tiles[coordsClicked[1]][coordsClicked[0]]
            tiles[coordsClicked[1]][coordsClicked[0]] = None
        elif not pygame.mouse.get_pressed()[0] and mouseDown:
            movingTile.clicked = False
            tiles = movingTile.setNewCoords(tiles, coordsClicked)
            mouseDown = False 
            coordsClicked = [-1, -1]
            movingTile = None
        for y in range(len(tiles)):
            for x in range(len(tiles[y])):
                if not tiles[y][x] == None:
                    tiles[y][x].draw(tiles)
                    if timeLeft < 0 and not mouseDown:
                        tiles = tiles[y][x].moveUp(tiles)
                        if game_over:
                            break
                    if not mouseDown and timeLeft>0:
                        tiles = tiles[y][x].gravity(tiles)
                        if not tiles[y][x] == None and not y == 7 and not tiles[y+1][x] is None and tiles[y][x].val == tiles[y+1][x].val:
                            tiles[y][x] = None
                            tiles[y+1][x].val = tiles[y+1][x].val + 1
                            if tiles[y+1][x].val>maxTile:
                                maxTile = tiles[y+1][x].val
                else:
                    if y == coordsClicked[1] and x == coordsClicked[0]:
                        movingTile.clicked = True
                        tiles = movingTile.noSharing(tiles)
                        movingTile.draw(tiles)
                        merger = False
                        tiles, merger, mouseDown, coordsClicked, maxTile = movingTile.merge(tiles, maxTile)
                        if merger:
                            movingTile = None
            if game_over:
                break
        if timeLeft <0 and not mouseDown:
            for i in range(len(tiles[7])):
                tiles[7][i] = Tile(7, i, randint(1, maxTile))
            speed = 10-level/5
            if speed<3:
                speed = 3
            next_time = time()+speed
            timeLeft = next_time
            level +=1
        if timeLeft > 0:
            timeLeft = next_time-time()
        pygame.display.flip()
        pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])


tiles[3][3] = Tile(3, 3, 5)
tiles[2][2] = Tile(2, 2, 5)
tiles[4][4] = Tile(4, 4, 4)
tiles[5][5] = Tile(5, 5, 5)
tiles[6][1] = Tile(6, 1, 5)
tiles[7][5] = Tile(7, 5, 5)
play()