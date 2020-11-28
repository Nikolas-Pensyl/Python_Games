#Written by: Nikolas Pensyl
#Started on: 7/29/2020
#Last Modified: 7/29/2020

import sys, pygame, math
import pygame.gfxdraw
from random import randint 
from time import time, sleep
pygame.init()

size = screen_width, screen_height = 800, 900 #size of board
screen = pygame.display.set_mode(size)

cyan = 0, 255, 255
green = 0, 255, 0
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
yellow = 0, 255, 255
orange = 255, 128, 0
purple = 153, 0, 153
pink = 255, 0, 127

an_zero = pygame.image.load("Temple_Run/Garruy/Run 0.png")
an_one = pygame.image.load("Temple_Run/Garruy/Run 1.png")
an_two = pygame.image.load("Temple_Run/Garruy/Run 2.png")
an_three = pygame.image.load("Temple_Run/Garruy/Run 3.png")
an_four = pygame.image.load("Temple_Run/Garruy/Run 4.png")
an_five = pygame.image.load("Temple_Run/Garruy/Run 5.png")
an_six = pygame.image.load("Temple_Run/Garruy/Run 6.png")
an_seven = pygame.image.load("Temple_Run/Garruy/Run 7.png")

ans = [an_zero, an_one, an_two, an_three, an_four, an_five, an_six, an_seven]



x_pos = 500
y_pos = 1858
y_size = 10
x_size = 5

floor_tiles = [[None for x in range(x_size)] for y in range(y_size)]

class Player:
    def __init__(self, images):
        self.grounded = True
        self.score = 0
        self.index = 0
        self.ans = images
        self.startspeed = .07
        self.speedup = 0
        self.x_pos = screen_width-15
        self.y_pos = screen_height/2
        self.gravity = 1
        self.y_speed = 0
        self.jump = -30

    def scoring(self):
        self.score +=1
        font = pygame.font.SysFont("comicsansms", 18)
        text = font.render(str(self.score), False, white)
        screen.blit(text, [15, 15])
        self.speedup = self.score/50000

    def animate(self):
        screen.blit(ans[self.index], [int(self.x_pos-15), int(self.y_pos)])
        self.index +=1
        if self.index == 8:
            self.index = 0

    def jumping(self):
        if pygame.key.get_pressed()[pygame.K_w] and self.grounded:
            self.grounded = False
            self.y_pos +=self.jump
        if not self.grounded:
            self.y_speed += self.gravity
            self.y_pos += self.y_speed
            if self.y_pos >= screen_height/2:
                self.grounded = True
                self.y_pos = screen_height/2
                self.y_speed = 0

    def movement(self):
        if pygame.mouse.get_pos()[0] > 50+screen_width/2:
            self.x_pos = 50+screen_width/2
        elif pygame.mouse.get_pos()[0] < screen_width/2-50:
            self.x_pos = screen_width/2-50
        else:
            self.x_pos = pygame.mouse.get_pos()[0]

    def actions(self):
        self.movement()
        self.animate()
        self.scoring()
        self.jumping()

    def getSpeed(self):
        return self.startspeed - self.speedup



def dontFreeze():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

class Tile:
    def __init__(self, clr, x, y, dis):
        self.color = clr
        self.x = x
        self.y = y
        self.width = 1000
        self.height = 2000
        self.x_pos = 2000 - 1000 * self.x
        self.y_pos = self.y * 1500
        self.z_pos = 450
        self.dis = dis
        self.scale = 1
    def drawTile(self):
        self.top_left = flattenPoint([self.x_pos-self.width/2, self.y_pos, self.z_pos], self.dis-9, self.scale)
        self.top_right = flattenPoint([self.x_pos+self.width/2, self.y_pos, self.z_pos], self.dis-9, self.scale)
        self.bottom_left = flattenPoint([self.x_pos-self.width/2, self.y_pos+self.height, self.z_pos], self.dis-8+self.y, self.scale)
        self.bottom_right = flattenPoint([self.x_pos+self.width/2, self.y_pos+self.height, self.z_pos], self.dis-8+self.y, self.scale)
        pygame.gfxdraw.filled_polygon(screen, (self.top_left, self.top_right, self.bottom_right, self.bottom_left), self.color)
    
    def newRow(self):
        self.x = 0 

garruy = Player(ans)


def drawFloor():
    for y in range(y_size):
        for x in range(x_size):
            floor_tiles[y][x].drawTile()

    #Walls
    pygame.draw.aaline(screen, red, flattenPoint([x_pos, y_pos, 450], 15, 15), flattenPoint([x_pos, 0, 450] ,2, 15))
    pygame.draw.aaline(screen, red, flattenPoint([-x_pos, y_pos, 450], 15, 15), flattenPoint([-x_pos, 0, 450], 2, 15))

def flattenPoint(point, distance, scale):
    global screen_height, screen_width
    (x, y, z) = (point[0], point[1], point[2])
    projectedY = int(((y * distance) / (z + distance)) * scale)
    projectedX = int(screen_width/2 + ((x * distance) / (z + distance)) * scale)
    return (projectedX, projectedY)

def play():
    for y in range(y_size):
        for x in range(x_size):
            if y%2 ==  x%2:
                floor_tiles[y][x] = Tile(cyan, x, y, 15+y*2)
            else:
                floor_tiles[y][x] = Tile(green, x, y, 15+y*2)

    timer = time()
    while True:
        dontFreeze()
        if timer < time():
            pygame.draw.rect(screen, black, [0, 0, screen_width, screen_height])
            drawFloor()
            garruy.actions()
            timer = time() + garruy.getSpeed()
            pygame.display.flip()
            if pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[0]:
                print(str(floor_tiles[0][4].top_left))
                print(str(floor_tiles[0][4].bottom_left))

play()