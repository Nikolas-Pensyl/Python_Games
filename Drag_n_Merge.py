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
speed = 10
timeLeft = speed/2
next_time = time()+speed/2
mouseDown = False
coordsClicked = [-1, -1]
game_over = False
movingTile = None
maxTile = 5

alpha = 100
lightness = 50
sat = 100

cyan = 0, 255, 255
green = 0, 255, 0
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
yellow = 0, 255, 255
orange = 255, 128, 0
purple = 153, 0, 153
pink = 255, 0, 127

colors = [cyan, green, white, red, yellow, orange, purple, pink, black, green, green, green, green, green, green, green]
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
        clr = pygame.Color(0)
        clr.hsla = 360-18*self.val, sat, lightness, alpha
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
            tiles[self.y][self.x] = None
            if tiles[tileY][tileX].val>maxTile:
                maxTile = tiles[tileY][tileX].val
            return tiles, True, False, [-1, -1], maxTile
        return tiles, False, True, [self.x, self.y], maxTile       
    def noSharing(self, tiles, clickY, clickX):
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
        
        if tiles[int(self.pos_y/100)][int(self.pos_x/100)] is None and (not self.x == int(self.pos_x/100) or not self.y == int(self.pos_y/100)):
            self.x = int(self.pos_x/100)
            self.y = int(self.pos_y/100)
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

def button(stri, x, y, length, height):
    global screen
    hover = False
    if pygame.mouse.get_pos()[0]>x and pygame.mouse.get_pos()[0]<x+length and pygame.mouse.get_pos()[1]>y and pygame.mouse.get_pos()[1]<y+height:
        hover = True
        pygame.draw.rect(screen, colors[2], [x, y, length, height])
        text = font.render(stri, False, black)
    else:
        pygame.draw.rect(screen, colors[2], [x, y, length, height], 3)
        text = font.render(stri, False, white)
    screen.blit(text, [x+int(length/2-text.get_width()/2), y+int(height/2-text.get_height()/2)])
    if pygame.mouse.get_pressed()[0] and hover:
        return True
    return False

def drawStuff(screen, speed):
    pygame.draw.rect(screen, colors[2], [25, 990-int(timeLeft*800/speed), 50, int(timeLeft*800/speed)])
    pygame.draw.rect(screen, colors[2], [25, 190, 50, 800], 5)
    pygame.draw.rect(screen, colors[2], [0+boardOffSetX, 0+boardOffSetY, 600, 800], 4)
    text = font.render("Round: " + str(level), False, white)
    screen.blit(text, [int((screen_width/8)*7-text.get_width()/2), int(screen_height/8-text.get_height()/2)])
    return screen

def setUp():
    global screen
    instruct = False
    start = False
    while not start:
        dontFreeze()
        if not instruct:
            text = font.render("Welcome to Drag n' Merge", False, white)
            screen.blit(text, [int((screen_width/2)-text.get_width()/2), int(screen_height/8-text.get_height()/2)])
            start = button("Start", int((screen_width/2)-350), int((screen_height/4)*3), 300, 100)
            instruct = button("Instructions", int((screen_width/2)+50), int((screen_height/4)*3), 300, 100)
        else:
            instruct = not button("Go Back", 10, 10, 200, 100)
            fonte = pygame.font.SysFont("comicsansms", 27)
            text = fonte.render("Drags tiles to merge with other tiles of the same value", False, white)
            screen.blit(text, [15, int((screen_height/9)-text.get_height()/2)])
            text = fonte.render("Tiles of the same value on top of each other", False, white)
            screen.blit(text, [15, int((screen_height/9)*3-text.get_height()/2)])
            text = fonte.render("will automactilly become merged", False, white)
            screen.blit(text, [15, int((screen_height/9)*4-text.get_height()/2)])
            text = fonte.render("Your goal is to get to 20 before the tiles hit the top", False, white)
            screen.blit(text, [15, int((screen_height/9)*6-text.get_height()/2)])
            text = fonte.render("Tiles will move up and be added every time the bar is empty", False, white)
            screen.blit(text, [15, int((screen_height/9)*8-text.get_height()/2)])
        pygame.display.flip()
        pygame.draw.rect(screen, black, [0, 0, screen_width, screen_height])

def play():
    global speed, maxTile, screen, tiles, mouseDown, coordsClicked, movingTile, timeLeft, level, next_time, game_over
    while not game_over:
        dontFreeze()
        screen = drawStuff(screen, speed)
        if pygame.mouse.get_pressed()[0] and not mouseDown and mouseInBounds() and not tiles[int(getMouseY()/100)][int(getMouseX()/100)] is None:
            mouseDown = pygame.mouse.get_pressed()[0]
            coordsClicked[0] = int(getMouseX()/100)
            coordsClicked[1] = int(getMouseY()/100)
            movingTile = tiles[coordsClicked[1]][coordsClicked[0]]
        elif not pygame.mouse.get_pressed()[0] and mouseDown:
            movingTile.clicked = False
            mouseDown = False 
            coordsClicked = [-1, -1]
            movingTile = None
        for y in range(len(tiles)):
            for x in range(len(tiles[y])):
                if not tiles[y][x] == None and not tiles[y][x] == movingTile:
                    tiles[y][x].draw(tiles)
                    if timeLeft < 0 and not mouseDown:
                        tiles = tiles[y][x].moveUp(tiles)
                        if game_over:
                            break
                    if timeLeft>0:
                        tiles = tiles[y][x].gravity(tiles)
                        if not tiles[y][x] == None and not y == 7 and not tiles[y+1][x] is None and tiles[y][x].val == tiles[y+1][x].val:
                            tiles[y][x] = None
                            tiles[y+1][x].val = tiles[y+1][x].val + 1
                            if tiles[y+1][x].val>maxTile:
                                maxTile = tiles[y+1][x].val
                else:
                    if not movingTile is None and tiles[y][x] == movingTile:
                        movingTile.clicked = True
                        merger = False
                        tiles, merger, mouseDown, coordsClicked, maxTile = movingTile.merge(tiles, maxTile)
                        if merger:
                            movingTile = None
                        else:
                            if (not movingTile.x == x or not movingTile.y == y) and tiles[movingTile.y][movingTile.x] is None:
                                tiles[movingTile.y][movingTile.x] = movingTile
                                tiles[y][x] = None
                            tiles = movingTile.noSharing(tiles, y, x)
                            movingTile.draw(tiles)

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
        pygame.draw.rect(screen, black, [0, 0, screen_width, screen_height])

setUp()
play()