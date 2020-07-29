#Written by: Nikolas Pensyl
#Started on: 7/29/2020
#Last Modified: 7/29/2020
import sys, pygame, math
from random import randint 
from time import time, sleep
pygame.init()

size = screen_width, screen_height = 800, 1000 #size of board

screen = pygame.display.est_mode(size)

font = pygame.font.SysFont("comicsansms", 45)

prev_time = 0
mouseDown = False

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
    def draw(self):
        pygame.draw.rect(screen, red, [int(self.x), int(self.y), int(self.width), int(self.height)])
    def moveUp(self):
        self.y = y_pos - 100
    def isClicked(self):
        if pygame.mouse.get_pressed()[0] and not mouseDown and pygame.mouse.get_pos()[0]>self.x and pygame.mouse.get_pos()[0]<self.x+self.width and pygame.mouse.get_pos()[1]>self.y and pygame.mouse.get_pos()[1]<self.y+self.height:
            mouseDown = True
            changes = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0] and mouseDown
