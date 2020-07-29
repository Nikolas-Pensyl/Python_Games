#Written by: Nikolas Pensyl
#Started on: 4/19/2020
#Last Modified: 4/22/2020
import sys, pygame, math
from random import randint 
from time import time, sleep
pygame.init()

size = screen_width, screen_height = 1200, 1000 #size of board

screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("comicsansms", 45)

score_limit = -1

random_colors = False

prev_time = 0

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

class Player:
    def __init__(self, x_pos, up, down):
        self.width = 10
        self.speed = 10
        self.height = screen_height/20
        self.score = 0
        self.y = screen_height/2-self.height/2
        self.win = False
        self.color = white
        self.bot = False
        self.x = x_pos
        self.up = up
        self.down = down
        self.bot_level = -1
        self.hurt = -1
        self.offset = -1
        if x_pos>screen_width/2:
            self.x = x_pos-self.width
    def draw(self):
        pygame.draw.rect(screen, self.color, [int(self.x), int(self.y), int(self.width), int(self.height)])
    def getHurt(self):
        self.hurt = randint((self.bot_level*10)-40, 40-(self.bot_level*10))
        self.offset = randint(-10, 11)
    def move(self):
        if not self.bot:
            if pygame.key.get_pressed()[self.up]:
                self.y -= self.speed
            elif pygame.key.get_pressed()[self.down]:
                self.y += self.speed
        else:
            closest = 0
            closest_x = abs(balls[0].x-self.x)
            for i in range(len(balls)):
                if closest_x>abs(balls[i].x-self.x):
                    closest = i
                    closest_x = abs(balls[i].x-self.x)
            if self.y+self.height/2+self.offset+self.hurt>balls[closest].y:
                self.y -= self.speed
            elif self.y+self.height/2+self.offset+self.hurt<balls[closest].y:
                self.y += self.speed
        if self.y<0:
            self.y = 0
        elif self.y+self.height>screen_height:
            self.y = screen_height-self.height



class Ball:
    def __init__(self):
        self.direction = 0
        self.speed = 5
        self.get_newDirection(0, 360)
        self.radius = 5
        self.x = screen_width/2
        self.y = screen_height/2
        self.color = white
    def reset(self):
        self.get_newDirection(0, 359)
        self.x = screen_width/2
        self.y = screen_height/2
    def get_newDirection(self, low, high):
        self.direction = randint(low, high)
        while self.direction>82 and self.direction<98 or self.direction>262 and self.direction<278:
            self.direction = randint(low, high)
    def draw(self):
        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)
    def move(self):
        self.y -= int(math.sin(math.radians(self.direction))*self.speed)
        self.x -= int(math.cos(math.radians(self.direction))*self.speed)
        self.bounce()
    def bounce(self):
        if self.y-self.radius<=0 or self.y+self.radius>=screen_height:
            lower = abs(360-self.direction)-5
            upper = abs(360-self.direction)+5
            if lower<0:
                lower = 0
            if upper>359:
                upper = 359
            self.get_newDirection(lower, upper)
        bouncer = False
        for i in range(len(players)):
            if self.y+self.radius>=players[i].y and self.y-self.radius<=players[i].y+players[i].height:
                if self.x-self.radius<=players[i].x+players[i].width and self.x+self.radius>players[i].x+players[i].width:
                    bouncer = True
                elif self.x+self.radius>=players[i].x and self.x-self.radius<players[i].x:
                    bouncer = True
        if bouncer:
            if self.direction<=180:
                if players[i].bot:
                    players[i].getHurt()
                lower = abs(180-self.direction)-5
                upper = abs(180-self.direction)+5
                if lower<0:
                    lower = 0
                if upper>359:
                    upper = 359
                self.get_newDirection(lower, upper)
            else:
                if players[i].bot:
                    players[i].getHurt()
                lower = abs(270-self.direction)-5
                upper = abs(270-self.direction)+5
                if lower<0:
                    lower = 0
                if upper>359:
                    upper = 359
                self.get_newDirection(lower, upper)
    def scoring(self):
        if self.x-self.radius<0:
            self.reset()
            players[0].score +=1
        elif self.x+self.radius>screen_width:
            self.reset()
            players[1].score +=1


players = [Player(10, pygame.K_w, pygame.K_s), Player(screen_width-10, pygame.K_UP, pygame.K_DOWN)]
balls = [Ball()]

def updateTime():
    global prev_time
    prev_time = time()

def setup():
    choosePlayers()
    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    ballAmount()
    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    chooseScoreLimit()
    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    #chooseColors()
    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    #ballSize()
    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    #playerHeight()
    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    ballSpeed()
    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    instructions()

def clicked(left, right, top, bottom): 
    global prev_time
    return pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0]>left and pygame.mouse.get_pos()[0]<right and pygame.mouse.get_pos()[1]>top and pygame.mouse.get_pos()[1]<bottom and time() - prev_time>1

def choosePlayers():
    amt_players = -1
    while amt_players == -1:
        dontFreeze()
        text = font.render("Choose amount of human players", False, white)
        screen.blit(text, [int(screen_width/2-text.get_width()/2), int(screen_height/8-text.get_height()/2)])
        for i in range(3):
            pygame.draw.rect(screen, white, [300*i+200, 550, 200, 100], 5)
            text = font.render(str(i), False, white)
            screen.blit(text, [int(300*i+300-text.get_width()/2), int(600-text.get_height()/2)])
            if clicked(300*i+200, 300*i+400, 550, 650):
                updateTime()
                amt_players = i
                if amt_players<1:
                    players[0].bot = True
                    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
                    chooseBotDifficulty(0)
                if amt_players<2:
                    players[1].bot = True
                    pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
                    chooseBotDifficulty(1)
        pygame.display.flip()

def chooseBotDifficulty(num):
    text = font.render("Choose bot diffculty for player " + str(num+1), False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2), 5])
    while players[num].bot_level == -1:
        dontFreeze()
        for i in range(4):
            pygame.draw.rect(screen, white, [280*i+40, 550, 200, 100], 5)
            text = font.render(str(i+1), False, white)
            screen.blit(text, [int(280*i+140-text.get_width()/2), int(600-text.get_height()/2)])
            if clicked(280*i+40, 280*i+240, 550, 650):
                updateTime()
                players[num].bot_level = i
        pygame.display.flip()

def ballAmount():
    text = font.render("How many balls do you want", False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2), 5])
    amount_b = 0
    while amount_b==0:
        dontFreeze()
        for i in range(5):
            pygame.draw.rect(screen, white, [240*i+20, 550, 200, 100], 5)
            text = font.render(str(i+1), False, white)
            screen.blit(text, [int(240*i+120-text.get_width()/2), int(600-text.get_height()/2)])
            if clicked(240*i+20, 240*i+260, 550, 650):
                updateTime()
                amount_b = i+1
        pygame.display.flip()
        for i in range(1, amount_b):
            balls.append(Ball())

def ballSpeed():
    speed = -1
    while not clicked(screen_width/2-100, screen_width/2+100, 700, 800) or speed==-1:
        dontFreeze()
        text = font.render("How many pixels do you want the ball", False, white)
        screen.blit(text, [int(screen_width/2-text.get_width()/2), 5])
        text = font.render("to move per iteration", False, white)
        screen.blit(text, [int(screen_width/2-text.get_width()/2), 5+int(text.get_height())+5])
        text = font.render("(the higher the number the faster the ball moves)", False, white)
        screen.blit(text, [int(screen_width/2-text.get_width()/2), 5+int(text.get_height())*2+5])
        if not speed==-1:
            text = font.render("Submit", False, white)
            screen.blit(text, [int(screen_width/2-text.get_width()/2), 750-int(text.get_height()/2)])
            pygame.draw.rect(screen, white, [int(screen_width/2)-100, 700, 200, 100], 5)
            text = font.render("Chosen speed: " + str(speed) + " pixels per iterattion", False, white)
            screen.blit(text, [int(screen_width/2-text.get_width()/2), 300])
        pygame.draw.line(screen, white, [50, 500], [850, 500], 5)
        for i in range(17):
            if (i+3)%2==1:
                text = font.render(str(i+3), False, white)
                pygame.draw.line(screen, white, [50+i*50, 500], [50+i*50, 480], 2)
                screen.blit(text, [50+i*50-int(text.get_width()/2), 430])
                if clicked(30+i*50, 70+i*50, 400, 497):
                    speed = i+3
            else:
                text = font.render(str(i+3), False, white)
                pygame.draw.line(screen, white, [50+i*50, 500], [50+i*50, 520], 2)
                screen.blit(text, [50+i*50-int(text.get_width()/2), 510])
                if clicked(30+i*50, 70+i*50, 503, 575):
                    speed = i+3
        text = font.render("Random", False, white)
        screen.blit(text, [int(1025-text.get_width()/2), int(500-text.get_height()/2)])
        pygame.draw.rect(screen, white, [925, 450, 200, 100], 5)
        if clicked(925, 1125, 450, 550):
            speed = -1
            break
        pygame.display.flip()
        pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    for i in range(len(balls)):
        balls[i].speed = speed
        if speed ==-1:
            balls[i].speed = randint(3, 20)
    updateTime()

def chooseScoreLimit():
    global score_limit
    while not clicked(screen_width/2-100, screen_width/2+100, 700, 800):
        dontFreeze()
        text = font.render("At what score should a player win", False, white)
        screen.blit(text, [int(screen_width/2-text.get_width()/2), 5])
        if not score_limit==-1:
            text = font.render("Submit", False, white)
            screen.blit(text, [int(screen_width/2-text.get_width()/2), 750-int(text.get_height()/2)])
            pygame.draw.rect(screen, white, [int(screen_width/2)-100, 700, 200, 100], 5)
            text = font.render("Chosen score for a victory: " + str(score_limit), False, white)
            screen.blit(text, [int(screen_width/2-text.get_width()/2), 300])
        pygame.draw.line(screen, white, [200, 500], [500, 500], 5)
        for i in range(7):
            if (i)%2==1:
                text = font.render(str(i+1), False, white)
                screen.blit(text, [200+i*50-int(text.get_width()/2), 430])
                pygame.draw.line(screen, white, [200+i*50, 500], [200+i*50, 480], 2)
                if clicked(180+i*50, 220+i*50, 400, 497):
                    score_limit = i+1
            else:
                text = font.render(str(i+1), False, white)
                pygame.draw.line(screen, white, [200+i*50, 500], [200+i*50, 520], 2)
                screen.blit(text, [200+i*50-int(text.get_width()/2), 510])
                if clicked(180+i*50, 220+i*50, 503, 575):
                    score_limit = i+1
        text = font.render("Random", False, white)
        screen.blit(text, [int(900-text.get_width()/2), int(500-text.get_height()/2)])
        pygame.draw.rect(screen, white, [800, 450, 200, 100], 5)
        if clicked(800, 1000, 450, 550):
            score_limit = randint(1, 8)
            break
        pygame.display.flip()
        pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    updateTime()

def displayScore():
    text = font.render("Player 1: " + str(players[0].score) + "                                         Player 2: " + str(players[1].score), False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2), 5])
    
def checkWin():
    for i in range(len(players)):
        if players[i].score>=score_limit:
            players[i].win = True
            return True

def dontFreeze():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

def instructions():
    dontFreeze()
    font = pygame.font.SysFont("comicsansms", 35)
    text = font.render("Player one will use the 'W' and 'S' keys to move up and down respectively", False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2), 5])
    text = font.render("Player two will use the up and down arrow keys to move up and down respectively", False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2), 5+int(text.get_height())+5])
    text = font.render("The goal of the game is to not let the ball past your paddle", False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2), 5+int(text.get_height())*2+5])
    pygame.draw.rect(screen, white, [int(screen_width/2-100), 700, 200, 100], 5)
    text = font.render("Got it :)", False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2), 750-int(text.get_height()/2)])
    pygame.display.flip()
    while not clicked(screen_width/2-100, screen_width/2+100, 700, 800):
        dontFreeze()
    updateTime()
    font = pygame.font.SysFont("comicsansms", 45)

def play():
    while not checkWin():
        dontFreeze()
    
        displayScore()
        for i in range(len(players)):
            players[i].draw()
            players[i].move()

        for i in range(len(balls)):
            balls[i].draw()
            balls[i].move()
            balls[i].scoring()
    
        pygame.display.flip()
        sleep(.02)
        pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
    font = pygame.font.SysFont("comicsansms", 55)
    if players[0].win:
        text = font.render("Player 1 Wins!!!", False, white)
        screen.blit(text, [int(screen_width/2-text.get_width()/2), int(screen_height/2)-int(text.get_height())-2])
    elif players[1].win:
        text = font.render("Player 2 Wins!!!", False, white)
        screen.blit(text, [int(screen_width/2-text.get_width()/2), int(screen_height/2)-int(text.get_height())-2])
    font = pygame.font.SysFont("comicsansms", 35)
    text = font.render("Quit", False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2)-210, int(screen_height/2)+53-text.get_height()/2])
    pygame.draw.rect(screen, white, [int(screen_width/2)-310, int(screen_height/2)+3, 200, 100], 5)
    text = font.render("Retry", False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2), int(screen_height/2)+53-text.get_height()/2])
    pygame.draw.rect(screen, white, [int(screen_width/2)-100, int(screen_height/2)+3, 200, 100], 5)
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Change settings", False, white)
    screen.blit(text, [int(screen_width/2-text.get_width()/2)+210, int(screen_height/2)+53-text.get_height()/2])
    pygame.draw.rect(screen, white, [int(screen_width/2)+110, int(screen_height/2)+3, 200, 100], 5)
    pygame.display.flip()
    while True:
        dontFreeze()
        if clicked(int(screen_width/2)-310, int(screen_width/2)-110, int(screen_height/2)+3, int(screen_height/2)+103):
            pygame.display.quit()
        elif clicked(int(screen_width/2)-100, int(screen_width/2)+100, int(screen_height/2)+3, int(screen_height/2)+103):
            players[0].win = False
            players[1].win = False
            players[0].score = 0
            players[1].score = 0
            pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
            play()
        elif clicked(int(screen_width/2)+110, int(screen_width/2)+310, int(screen_height/2)+3, int(screen_height/2)+103):
            players[0].win = False
            players[1].win = False
            players[0].score = 0
            players[1].score = 0
            pygame.draw.rect(screen, colors[background], [0, 0, screen_width, screen_height])
            setup()
            play()
    updateTime()


setup()
play()
