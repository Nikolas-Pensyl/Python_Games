import sys, pygame
from random import randint 
from time import time, sleep
#pygame.init()

#size = screen_width, screen_height = 900, 900
#screen = pygame.display.set_mode(size)

white = 255, 255, 255
black = 0, 0, 0

prev_time = 0
start_time = time()

GridComplete = [[0 for x in range(9)] for y in range(9)]
Grid = [0 for x in range(81)]
GridSorted = [False for x in range(81)]

def MakeGrid():
    global Grid, GridComplete
    notused = []
    for box in range(9):
        notused = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(3):
            for j in range(3):
                ran = notused.pop(randint(0, len(notused)-1))
                GridComplete[int(box/3)*3+int((i*3+j)/3)][(box%3)*3+((i*3+j)%3)] = ran
                Grid[(j+(box*3)%9)+(((box/3)+i)*9)] = ran
    sortGrid()

def sortGrid():
    global Grid, GridComplete, GridSorted
    backtrack = False
    for i in range(9):
        rowing = False
        for a in range(2):
            rowing = not rowing
            registered = [False for x in range(10)]
            rowOrgin = i*9
            colOrgin = i
            Row_Col: for j in range(9):
                num = 0
                step = rowOrgin + j if rowing else step = colOrgin + j*9
                num = Grid[step]
                if not registered[num]:
                    registered[num] = True
                else:
                    for y in range(j, -1, -1):
                        scan = i*9 + y if rowing else scan = i + 9*y
                        if Grid[scan] == num:
                            k = i%3+1 if rowing else k = 0
                            for z in range(k, 9):
                                if not rowing and z%3<=%3:
                                    continue
                                boxOrigin = ((scan % 9) / 3) * 3 + (scan / 27) * 27
                                boxStep = boxOrigin + (z / 3) * 9 + (z % 3)
                                boxNum = grid[boxStep]
                                if((not sorted[scan] and not sorted[boxStep] and not registered[boxNum])
                                 or (sorted[scan] and not registered[boxNum] and (rowing and boxStep%9==scan%9 or not rowing and boxStep/9==scan/9))):
                                    Grid[scan] = boxNum
                                    Grid[boxStep] = num
                                    registered[boxNum] = True
                                    z = 9
                                    y = -1
                                    break
                                

                                



def removeNums():
    global Grid
    count = randint(62, 71)
    for i in range(count):
        x = randint(0, 8)
        y = randint(0, 8)
        while Grid[y][x] == 0:
            x = randint(0, 8)
            y = randint(0, 8)
        Grid[y][x] = 0
    return Grid

def checkRow(index):
    global Grid
    used = Grid[index]
    used.sort()
    for x in range(8):
        if used[x] == used[x+1]:
            return False
    return True

def checkCol(index):
    global Grid
    used = [0 for x in range(9)]
    for x in range(9):
        used[x] = Grid[x][index]
    used.sort()
    for x in range(8):
        if used[x] == used[x+1]:
            return False
    return True

def checkBox(index):
    global Grid
    used = [0 for x in range(9)]
    for x in range(9):
        used[x] = Grid[int(index/3)*3+int(x/3)][(index%3)*3+(x%3)]
    used.sort()
    for x in range(8):
        if used[x] == used[x+1]:
            return False
    return True
    
def isPossible():
    for i in range(9):
        if not checkBox(i) or not checkRow(i) or not checkCol(i):
            return False
    return True

def dontFreeze():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

def updateTime():
    global prev_time
    prev_time = time()

def clicked():
    global prev_time
    if time()-prev_time>2:
        return pygame.mouse.get_pressed()[0]
    return False

def displayGrid():
    global prev_time, Grid
    updateTime()
    while not clicked():
        dontFreeze()
        pygame.draw.rect(screen, white, [0, 0, screen_width, screen_height])
        pygame.draw.line(screen, black, [0, 0], [0, 900])
        pygame.draw.line(screen, black, [0, 0], [900, 0])
        font = pygame.font.SysFont("comicsansms", 30)
        for y in range(9):
            pygame.draw.line(screen, black, [y*100+100, 0], [y*100+100, 900])
            pygame.draw.line(screen, black, [0, y*100+100], [900, y*100+100])
            for x in range(9):
                if not Grid[y][x]==0:
                    text = font.render(str(Grid[y][x]), False, black)
                    screen.blit(text, [int(x*100+50-text.get_width()/2), int(y*100+50-text.get_height()/2)])
        pygame.display.flip()


MakeGrid()

displayGrid()
removeNums()
displayGrid()