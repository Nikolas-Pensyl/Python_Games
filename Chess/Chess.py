#Written by: Nikolas Pensyl
#Started on: 4/19/2020
#Last Modified: 4/22/2020
import sys, pygame
pygame.init()

size = width, height = 1600, 1000 #size of board
board_width = 1000
SQUARE_SIZE = height/8 #size of each square on the board
offset_X = 10 #offset for each piece from the top left
offset_Y = 10 #offset for each piece from the top left
piece_selected = -1 #index of piece slected within array. if it = -1 no piece is selected


list_moves = []
change = 0
#These variables control the state of the game based on their desciption
tie = False 
white_win = False
black_win = False
white_turn = True

#these are colors and their rgb values
cyan = 0, 50, 255
green = 0, 255, 0
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0

screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("comicsansms", 35)

board = pygame.image.load("Chess/Chess Pieces/board.png")
boardrect = board.get_rect()

#Loads the pictures of the pieces
WHITE_PAWN = pygame.image.load("Chess/Chess Pieces/White Pawn.png")
WHITE_BISHOP = pygame.image.load("Chess/Chess Pieces/White Bishop.png")
WHITE_KING = pygame.image.load("Chess/Chess Pieces/White King.png")
WHITE_QUEEN = pygame.image.load("Chess/Chess Pieces/White Queen.png")
WHITE_KNIGHT = pygame.image.load("Chess/Chess Pieces/White Knight.png")
WHITE_ROOK = pygame.image.load("Chess/Chess Pieces/White Rook.png")

BLACK_PAWN = pygame.image.load("Chess/Chess Pieces/Black Pawn.png")
BLACK_BISHOP = pygame.image.load("Chess/Chess Pieces/Black Bishop.png")
BLACK_KING = pygame.image.load("Chess/Chess Pieces/Black King.png")
BLACK_QUEEN = pygame.image.load("Chess/Chess Pieces/Black Queen.png")
BLACK_KNIGHT = pygame.image.load("Chess/Chess Pieces/Black Knight.png")
BLACK_ROOK = pygame.image.load("Chess/Chess Pieces/Black Rook.png")


#0 = piece image//also serves as identifier of piece
#1 = alive(true or false)
#2 = X coord
#3 = Y coord
white_pieces = [[WHITE_PAWN, True, 0, 6], [WHITE_PAWN, True, 1, 6], [WHITE_PAWN, True, 2, 6], [WHITE_PAWN, True, 3, 6], [WHITE_PAWN, True, 4, 6], [WHITE_PAWN, True, 5, 6], [WHITE_PAWN, True, 6, 6], [WHITE_PAWN, True, 7, 6], [WHITE_BISHOP, True, 2, 7], [WHITE_BISHOP, True, 5, 7], [WHITE_QUEEN, True, 3, 7], [WHITE_KING, True, 4, 7], [WHITE_KNIGHT, True, 1, 7], [WHITE_KNIGHT, True, 6, 7], [WHITE_ROOK, True, 0, 7], [WHITE_ROOK, True, 7, 7]]

black_pieces = [[BLACK_PAWN, True, 0, 1], [BLACK_PAWN, True, 1, 1], [BLACK_PAWN, True, 2, 1], [BLACK_PAWN, True, 3, 1], [BLACK_PAWN, True, 4, 1], [BLACK_PAWN, True, 5, 1], [BLACK_PAWN, True, 6, 1], [BLACK_PAWN, True, 7, 1], [BLACK_BISHOP, True, 2, 0], [BLACK_BISHOP, True, 5, 0], [BLACK_QUEEN, True, 3, 0], [BLACK_KING, True, 4, 0], [BLACK_KNIGHT, True, 1, 0], [BLACK_KNIGHT, True, 6, 0], [BLACK_ROOK, True, 0, 0], [BLACK_ROOK, True, 7, 0]]


#0 = index of piece 
#1 = New X-coord
#2 = New y-coord
white_moves_possible = [[-1, -1, -1]]
black_moves_possible = [[-1, -1, -1]]

#0 = index of piece
#1 = index of piece to be taken
#2 = X-coord of piece to be taken
#3 = y-coord of piece to be taken
white_captures_possible = [[-1, -1, -1, -1]]
black_captures_possible = [[-1, -1, -1, -1]]

#this function displays all pieces and also checks to see if a piece was selected
def displayPieces(selected): 
    for i in range(len(white_pieces)):
        
        if white_pieces[i][1]:
            if checkClick(white_pieces[i][2], white_pieces[i][3]) and white_turn or (selected==i) and white_turn:
                pygame.draw.rect(screen, cyan, [int(white_pieces[i][2]*SQUARE_SIZE), int(white_pieces[i][3]*SQUARE_SIZE), int(SQUARE_SIZE), int(SQUARE_SIZE)])
                selected = i
            screen.blit(white_pieces[i][0], [int(white_pieces[i][2]*SQUARE_SIZE+offset_X), int(white_pieces[i][3]*SQUARE_SIZE+offset_Y)])
        if black_pieces[i][1]:
            if checkClick(black_pieces[i][2], black_pieces[i][3]) and not white_turn or (selected==i) and not white_turn:
                pygame.draw.rect(screen, cyan, [int(black_pieces[i][2]*SQUARE_SIZE), int(black_pieces[i][3]*SQUARE_SIZE), int(SQUARE_SIZE), int(SQUARE_SIZE)])
                selected = i
            screen.blit(black_pieces[i][0], [int(black_pieces[i][2]*SQUARE_SIZE+offset_X), int(black_pieces[i][3]*SQUARE_SIZE+offset_Y)])
    return selected

#this functon tests if the piece passed in was clicked and that it is that colors turn
def checkClick(x_pos, y_pos):
    if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0]>x_pos*SQUARE_SIZE and pygame.mouse.get_pos()[0]<x_pos*SQUARE_SIZE+SQUARE_SIZE and pygame.mouse.get_pos()[1]>y_pos*SQUARE_SIZE and pygame.mouse.get_pos()[1]<y_pos*SQUARE_SIZE+SQUARE_SIZE:
        return True
    
    return False

def getPiece(piece):
    if piece[0] is WHITE_PAWN:
        return "White Pawn"
    if piece[0] is WHITE_KNIGHT:
        return "White Knight"
    if piece[0] is WHITE_ROOK:
        return "White Rook"
    if piece[0] is WHITE_BISHOP:
        return "White Bishop"
    if piece[0] is WHITE_QUEEN:
        return "White Queen"
    if piece[0] is WHITE_KING:
        return "White King"
    if piece[0] is BLACK_PAWN:
        return "Black Pawn"
    if piece[0] is BLACK_KNIGHT:
        return "Black Knight"
    if piece[0] is BLACK_ROOK:
        return  "Black Rook"
    if piece[0] is BLACK_BISHOP:
        return "Black Bishop"
    if piece[0] is BLACK_QUEEN:
        return "Black Queen"
    if piece[0] is BLACK_KING:
        return "Black King"

def displayMoves(moves_made, change):
    pygame.draw.rect(screen, black, [1000, 0, 600, 1000])
    change = scrollBar(moves_made, change)
    font_piece = pygame.font.SysFont("comicsansms", 18)
    for i in range(len(moves_made)):
        if len(moves_made[i])==2:
            text = font_piece.render(str(i+1) + ": " + moves_made[i][0] + " transformed to " + moves_made[i][1], False, white)
        if len(moves_made[i])==5:
            text = font_piece.render(str(i+1) + ": " + moves_made[i][0] + " moved from (" + str(moves_made[i][1]) + ", " + str(moves_made[i][2]) + ") to (" + str(moves_made[i][3]) + ", " + str(moves_made[i][4]) + ")", False, white)
        if len(moves_made[i])==6:
            text = font_piece.render(str(i+1) + ": " + moves_made[i][0] + " moved from (" + str(moves_made[i][1]) + ", " + str(moves_made[i][2]) + ") to (" + str(moves_made[i][3]) + ", " + str(moves_made[i][4]) + ") and took " + moves_made[i][5], False, white)
        screen.blit(text, [board_width + 10, (i+1)*40+int(change)])
    pygame.draw.rect(screen, black, [1000, 0, 600, 30])
    font_piece = pygame.font.SysFont("comicsansms", 25)
    text = font_piece.render("Moves made: ", False, white)
    screen.blit(text, [board_width + 10, 0])
    return change

def scrollBar(moves_made, change):
    mouse_movement = pygame.mouse.get_rel()
    if len(moves_made)>24:
        bar_height = (height-40)*(24/len(moves_made))
        pygame.draw.rect(screen, white, [1590, int(-change*(24/len(moves_made)))+40, 10, int(bar_height)])
        if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0]>1565:
            change -= mouse_movement[1]/(24/len(moves_made))
        if change<-len(moves_made)*40+960:
            change = -len(moves_made)*40+960
        elif change>0:
            change = 0
    return change

def moveChange(change, moves_made):
    if len(moves_made)>24:
        change = -len(moves_made)*40+960
    return change


#shows available moves for piece selected and checks if one of the available spaces is clicked
#pieces is the array for the color up; other pieces is the list for the color not up; direction is -1 or 1 to tell the pieces which direction to move
def availableMoves(pieces, other_pieces, direction, selected, moves_made, change):
    pawn = False
    pawn_moved = False
    moves = []
    captures = []
    if pieces[selected][0] is WHITE_PAWN or pieces[selected][0] is BLACK_PAWN:
        pawn = True
        move_one = True
        move_two = False
        take_right = [False, -1]
        take_left = [False, -1]
        if pieces[selected][3]==6 and direction==-1 or pieces[selected][3]==1 and direction==1:
            move_two = True
        for i in range(len(pieces)):
            if pieces[i][1] and pieces[i][2]==pieces[selected][2] and pieces[i][3]==pieces[selected][3]+1*direction:
                move_one = False
            elif other_pieces[i][1] and other_pieces[i][2]==pieces[selected][2] and pieces[selected][3]+1*direction==other_pieces[i][3]:
                move_one = False
            if pieces[i][1] and pieces[i][2]==pieces[selected][2] and pieces[i][3]==pieces[selected][3]+2*direction:
                move_two = False
            elif other_pieces[i][1] and other_pieces[i][2]==pieces[selected][2] and pieces[selected][3]+2*direction==other_pieces[i][3]:
                move_two = False
            if other_pieces[i][1] and pieces[selected][2]+1==other_pieces[i][2] and pieces[selected][3]+1*direction==other_pieces[i][3]:
                take_right = [True, i]
            elif other_pieces[i][1] and pieces[selected][2]-1==other_pieces[i][2] and pieces[selected][3]+1*direction==other_pieces[i][3]:
                take_left = [True, i]
        if move_one:
            moves.append([int(pieces[selected][2]), int(pieces[selected][3]+1*direction)])
        if move_one and move_two:
            moves.append([int(pieces[selected][2]), int(pieces[selected][3]+2*direction)])
        if take_right[0]:
            captures.append([int(pieces[selected][2]+1), int(pieces[selected][3]+1*direction), take_right[1]])
        if take_left[0]:
            captures.append([int(pieces[selected][2]-1), int(pieces[selected][3]+1*direction), take_left[1]])
    elif pieces[selected][0] is WHITE_KNIGHT or pieces[selected][0] is BLACK_KNIGHT:
        knight_moves = [[True, -1, -2], [True, 1, -2], [True, -2, -1], [True, 2, -1], [True, -2, 1], [True, 2, 1], [True, -1, 2], [True, 1, 2]]
        for i in range(len(pieces)):
            for j in range(len(knight_moves)):
                if pieces[i][1] and pieces[i][2]==pieces[selected][2]+knight_moves[j][1] and pieces[i][3]==pieces[selected][3]+knight_moves[j][2]:
                    knight_moves[j][0] = False
                elif other_pieces[i][1] and other_pieces[i][2]==pieces[selected][2]+knight_moves[j][1] and other_pieces[i][3]==pieces[selected][3]+knight_moves[j][2]:
                    captures.append([pieces[selected][2]+knight_moves[j][1], pieces[selected][3]+knight_moves[j][2], i])
                    knight_moves[j][0] = False
                elif pieces[selected][2]+knight_moves[j][1]>7 or pieces[selected][2]+knight_moves[j][1]<0 or pieces[selected][3]+knight_moves[j][2]<0 or pieces[selected][3]+knight_moves[j][2]>7:
                    knight_moves[j][0] = False
        for i in range(len(knight_moves)):
            if knight_moves[i][0]:
                moves.append([pieces[selected][2]+knight_moves[i][1], pieces[selected][3]+knight_moves[i][2]])
    elif pieces[selected][0] is WHITE_QUEEN or pieces[selected][0] is BLACK_QUEEN:
        up = True
        left = True
        down = True
        right = True
        up_left = True
        up_right = True
        down_left = True
        down_right = True
        iterate = 1
        while not iterate==8 and (up or down or left or right or up_right or up_left or down_right or down_left):
            if pieces[selected][2]+iterate>7:
                right = False
                up_right = False
                down_right = False
            if pieces[selected][2]-iterate<0:
                left = False
                up_left = False
                down_left = False
            if pieces[selected][3]+iterate>7:
                down = False
                down_left = False
                down_right = False
            if pieces[selected][3]-iterate<0:
                up = False
                up_left = False
                up_right = False
            for i in range(len(pieces)):
                if right and pieces[i][1] and pieces[selected][2]+iterate==pieces[i][2] and pieces[selected][3]==pieces[i][3]:
                    right = False
                elif right and other_pieces[i][1] and pieces[selected][2]+iterate==other_pieces[i][2] and pieces[selected][3]==other_pieces[i][3]:
                    right = False
                    captures.append([pieces[selected][2]+iterate, pieces[selected][3], i])
                if left and pieces[i][1] and pieces[selected][2]-iterate==pieces[i][2] and pieces[selected][3]==pieces[i][3]:
                    left = False
                elif left and other_pieces[i][1] and pieces[selected][2]-iterate==other_pieces[i][2] and pieces[selected][3]==other_pieces[i][3]:
                    left = False
                    captures.append([pieces[selected][2]-iterate, pieces[selected][3], i])
                if down and pieces[i][1] and pieces[selected][3]+iterate==pieces[i][3] and pieces[selected][2]==pieces[i][2]:
                    down = False
                elif down and other_pieces[i][1] and pieces[selected][3]+iterate==other_pieces[i][3] and pieces[selected][2]==other_pieces[i][2]:
                    down = False
                    captures.append([pieces[selected][2], pieces[selected][3]+iterate, i])
                if up and pieces[i][1] and pieces[selected][3]-iterate==pieces[i][3] and pieces[selected][2]==pieces[i][2]:
                    up = False
                elif up and other_pieces[i][1] and pieces[i][3] and pieces[selected][3]-iterate==other_pieces[i][3] and pieces[selected][2]==other_pieces[i][2]:
                    up = False
                    captures.append([pieces[selected][2], pieces[selected][3]-iterate, i])
                if up_right and pieces[i][1] and pieces[selected][2]+iterate==pieces[i][2] and pieces[selected][3]-iterate==pieces[i][3]:
                    up_right = False
                elif up_right and other_pieces[i][1] and pieces[selected][2]+iterate==other_pieces[i][2] and pieces[selected][3]-iterate==other_pieces[i][3]:
                    up_right = False
                    captures.append([pieces[selected][2]+iterate, pieces[selected][3]-iterate, i])
                if up_left and pieces[i][1] and pieces[selected][2]-iterate==pieces[i][2] and pieces[selected][3]-iterate==pieces[i][3]:
                    up_left = False
                elif up_left and other_pieces[i][1] and pieces[selected][2]-iterate==other_pieces[i][2] and pieces[selected][3]-iterate==other_pieces[i][3]:
                    up_left = False
                    captures.append([pieces[selected][2]-iterate, pieces[selected][3]-iterate, i])
                if down_right and other_pieces[i][1] and pieces[selected][3]+iterate==pieces[i][3] and pieces[selected][2]+iterate==pieces[i][2]:
                    down_right = False
                elif down_right and other_pieces[i][1] and pieces[selected][3]+iterate==other_pieces[i][3] and pieces[selected][2]+iterate==other_pieces[i][2]:
                    down_right = False
                    captures.append([pieces[selected][2]+iterate, pieces[selected][3]+iterate, i])
                if down_left and pieces[i][1] and pieces[selected][3]+iterate==pieces[i][3] and pieces[selected][2]-iterate==pieces[i][2]:
                    down_left = False
                elif down_left and other_pieces[i][1] and pieces[selected][3]+iterate==other_pieces[i][3] and pieces[selected][2]-iterate==other_pieces[i][2]:
                    down_left = False
                    captures.append([pieces[selected][2]-iterate, pieces[selected][3]+iterate, i])
            if right:
                moves.append([pieces[selected][2]+iterate, pieces[selected][3]])
            if left:
                moves.append([pieces[selected][2]-iterate, pieces[selected][3]])
            if down:
                moves.append([pieces[selected][2], pieces[selected][3]+iterate])
            if up:
                moves.append([pieces[selected][2], pieces[selected][3]-iterate])
            if up_right:
                moves.append([pieces[selected][2]+iterate, pieces[selected][3]-iterate])
            if up_left:
                moves.append([pieces[selected][2]-iterate, pieces[selected][3]-iterate])
            if down_right:
                moves.append([pieces[selected][2]+iterate, pieces[selected][3]+iterate])
            if down_left:
                moves.append([pieces[selected][2]-iterate, pieces[selected][3]+iterate])
            iterate +=1
    elif pieces[selected][0] is WHITE_ROOK or pieces[selected][0] is BLACK_ROOK:
        up = True
        left = True
        down = True
        right = True
        iterate = 1
        while not iterate==7 and (up or down or left or right):
            if pieces[selected][2]+iterate>7:
                right = False
            if pieces[selected][2]-iterate<0:
                left = False
            if pieces[selected][3]+iterate>7:
                down = False
            if pieces[selected][3]-iterate<0:
                up = False
            for i in range(len(pieces)):
                if right and pieces[i][1] and pieces[selected][2]+iterate==pieces[i][2] and pieces[selected][3]==pieces[i][3]:
                    right = False
                elif right and other_pieces[i][1] and pieces[selected][2]+iterate==other_pieces[i][2] and pieces[selected][3]==other_pieces[i][3]:
                    right = False
                    captures.append([pieces[selected][2]+iterate, pieces[selected][3], i])
                if left and pieces[i][1] and pieces[selected][2]-iterate==pieces[i][2] and pieces[selected][3]==pieces[i][3]:
                    left = False
                elif left and other_pieces[i][1] and pieces[selected][2]-iterate==other_pieces[i][2] and pieces[selected][3]==other_pieces[i][3]:
                    left = False
                    captures.append([pieces[selected][2]-iterate, pieces[selected][3], i])
                if down and pieces[i][1] and pieces[selected][3]+iterate==pieces[i][3] and pieces[selected][2]==pieces[i][2]:
                    down = False
                elif down and other_pieces[i][1] and pieces[selected][3]+iterate==other_pieces[i][3] and pieces[selected][2]==other_pieces[i][2]:
                    down = False
                    captures.append([pieces[selected][2], pieces[selected][3]+iterate, i])
                if up and pieces[i][1] and pieces[selected][3]-iterate==pieces[i][3] and pieces[selected][2]==pieces[i][2]:
                    up = False
                elif up and other_pieces[i][1] and pieces[i][3] and pieces[selected][3]-iterate==other_pieces[i][3] and pieces[selected][2]==other_pieces[i][2]:
                    up = False
                    captures.append([pieces[selected][2], pieces[selected][3]-iterate, i])
            if right:
                moves.append([pieces[selected][2]+iterate, pieces[selected][3]])
            if left:
                moves.append([pieces[selected][2]-iterate, pieces[selected][3]])
            if down:
                moves.append([pieces[selected][2], pieces[selected][3]+iterate])
            if up:
                moves.append([pieces[selected][2], pieces[selected][3]-iterate])
            iterate +=1
    elif pieces[selected][0] is WHITE_BISHOP or pieces[selected][0] is BLACK_BISHOP:
        up_left = True
        up_right = True
        down_left = True
        down_right = True
        iterate = 1
        while not iterate==7 and (up_right or up_left or down_right or down_left):
            if pieces[selected][2]+iterate>7:
                up_right = False
                down_right = False
            if pieces[selected][2]-iterate<0:
                up_left = False
                down_left = False
            if pieces[selected][3]+iterate>7:
                down_left = False
                down_right = False
            if pieces[selected][3]-iterate<0:
                up_left = False
                up_right = False
            for i in range(len(pieces)):
                if up_right and pieces[i][1] and pieces[selected][2]+iterate==pieces[i][2] and pieces[selected][3]-iterate==pieces[i][3]:
                    up_right = False
                elif up_right and other_pieces[i][1] and pieces[selected][2]+iterate==other_pieces[i][2] and pieces[selected][3]-iterate==other_pieces[i][3]:
                    up_right = False
                    captures.append([pieces[selected][2]+iterate, pieces[selected][3]-iterate, i])
                if up_left and pieces[i][1] and pieces[selected][2]-iterate==pieces[i][2] and pieces[selected][3]-iterate==pieces[i][3]:
                    up_left = False
                elif up_left and other_pieces[i][1] and pieces[selected][2]-iterate==other_pieces[i][2] and pieces[selected][3]-iterate==other_pieces[i][3]:
                    up_left = False
                    captures.append([pieces[selected][2]-iterate, pieces[selected][3]-iterate, i])
                if down_right and other_pieces[i][1] and pieces[selected][3]+iterate==pieces[i][3] and pieces[selected][2]+iterate==pieces[i][2]:
                    down_right = False
                elif down_right and other_pieces[i][1] and pieces[selected][3]+iterate==other_pieces[i][3] and pieces[selected][2]+iterate==other_pieces[i][2]:
                    down_right = False
                    captures.append([pieces[selected][2]+iterate, pieces[selected][3]+iterate, i])
                if down_left and pieces[i][1] and pieces[selected][3]+iterate==pieces[i][3] and pieces[selected][2]-iterate==pieces[i][2]:
                    down_left = False
                elif down_left and other_pieces[i][1] and pieces[selected][3]+iterate==other_pieces[i][3] and pieces[selected][2]-iterate==other_pieces[i][2]:
                    down_left = False
                    captures.append([pieces[selected][2]-iterate, pieces[selected][3]+iterate, i])
            if up_right:
                moves.append([pieces[selected][2]+iterate, pieces[selected][3]-iterate])
            if up_left:
                moves.append([pieces[selected][2]-iterate, pieces[selected][3]-iterate])
            if down_right:
                moves.append([pieces[selected][2]+iterate, pieces[selected][3]+iterate])
            if down_left:
                moves.append([pieces[selected][2]-iterate, pieces[selected][3]+iterate])
            iterate +=1
    elif pieces[selected][0] is WHITE_KING or pieces[selected][0] is BLACK_KING:
        up = True
        left = True
        down = True
        right = True
        up_left = True
        up_right = True
        down_left = True
        down_right = True
        if pieces[selected][2]+1>7:
            right = False
            up_right = False
            down_right = False
        if pieces[selected][2]-1<0:
            left = False
            up_left = False
            down_left = False
        if pieces[selected][3]+1>7:
            down = False
            down_left = False
            down_right = False
        if pieces[selected][3]-1<0:
            up = False
            up_left = False
            up_right = False
        for i in range(len(pieces)):
            if right and pieces[i][1] and pieces[selected][2]+1==pieces[i][2] and pieces[selected][3]==pieces[i][3]:
                right = False
            elif right and other_pieces[i][1] and pieces[selected][2]+1==other_pieces[i][2] and pieces[selected][3]==other_pieces[i][3]:
                right = False
                captures.append([pieces[selected][2]+1, pieces[selected][3], i])
            if left and pieces[i][1] and pieces[selected][2]-1==pieces[i][2] and pieces[selected][3]==pieces[i][3]:
                left = False
            elif left and other_pieces[i][1] and pieces[selected][2]-1==other_pieces[i][2] and pieces[selected][3]==other_pieces[i][3]:
                left = False
                captures.append([pieces[selected][2]-1, pieces[selected][3], i])
            if down and pieces[i][1] and pieces[selected][3]+1==pieces[i][3] and pieces[selected][2]==pieces[i][2]:
                down = False
            elif down and other_pieces[i][1] and pieces[selected][3]+1==other_pieces[i][3] and pieces[selected][2]==other_pieces[i][2]:
                down = False
                captures.append([pieces[selected][2], pieces[selected][3]+1, i])
            if up and pieces[i][1] and pieces[selected][3]-1==pieces[i][3] and pieces[selected][2]==pieces[i][2]:
                up = False
            elif up and other_pieces[i][1] and pieces[i][3] and pieces[selected][3]-1==other_pieces[i][3] and pieces[selected][2]==other_pieces[i][2]:
                up = False
                captures.append([pieces[selected][2], pieces[selected][3]-1, i])
            if up_right and pieces[i][1] and pieces[selected][2]+1==pieces[i][2] and pieces[selected][3]-1==pieces[i][3]:
                up_right = False
            elif up_right and other_pieces[i][1] and pieces[selected][2]+1==other_pieces[i][2] and pieces[selected][3]-1==other_pieces[i][3]:
                up_right = False
                captures.append([pieces[selected][2]+1, pieces[selected][3]-1, i])
            if up_left and pieces[i][1] and pieces[selected][2]-1==pieces[i][2] and pieces[selected][3]-1==pieces[i][3]:
                up_left = False
            elif up_left and other_pieces[i][1] and pieces[selected][2]-1==other_pieces[i][2] and pieces[selected][3]-1==other_pieces[i][3]:
                up_left = False
                captures.append([pieces[selected][2]-1, pieces[selected][3]-1, i])
            if down_right and other_pieces[i][1] and pieces[selected][3]+1==pieces[i][3] and pieces[selected][2]+1==pieces[i][2]:
                down_right = False
            elif down_right and other_pieces[i][1] and pieces[selected][3]+1==other_pieces[i][3] and pieces[selected][2]+1==other_pieces[i][2]:
                down_right = False
                captures.append([pieces[selected][2]+1, pieces[selected][3]+1, i])
            if down_left and pieces[i][1] and pieces[selected][3]+1==pieces[i][3] and pieces[selected][2]-1==pieces[i][2]:
                down_left = False
            elif down_left and other_pieces[i][1] and pieces[selected][3]+1==other_pieces[i][3] and pieces[selected][2]-1==other_pieces[i][2]:
                down_left = False
                captures.append([pieces[selected][2]+1, pieces[selected][3]-1, i])
        if right:
            moves.append([pieces[selected][2]+1, pieces[selected][3]])
        if left:
            moves.append([pieces[selected][2]-1, pieces[selected][3]])
        if down:
            moves.append([pieces[selected][2], pieces[selected][3]+1])
        if up:
            moves.append([pieces[selected][2], pieces[selected][3]-1])
        if up_right:
            moves.append([pieces[selected][2]+1, pieces[selected][3]-1])
        if up_left:
            moves.append([pieces[selected][2]-1, pieces[selected][3]-1])
        if down_right:
            moves.append([pieces[selected][2]+1, pieces[selected][3]+1])
        if down_left:
            moves.append([pieces[selected][2]-1, pieces[selected][3]+1])
    
    
    #these last two loops show possible movements and captures in that order they also test for movements or captures
    for i in range(len(moves)):
       pygame.draw.rect(screen, green, [int(moves[i][0]*SQUARE_SIZE), int(moves[i][1]*SQUARE_SIZE), int(SQUARE_SIZE), int(SQUARE_SIZE)])
       pygame.draw.rect(screen, black, [int(moves[i][0]*SQUARE_SIZE), int(moves[i][1]*SQUARE_SIZE), int(SQUARE_SIZE), int(SQUARE_SIZE)], 5)
       if checkClick(moves[i][0], moves[i][1]) and not selected==-1:
           moves_made.append([getPiece(pieces[selected]), pieces[selected][2], pieces[selected][3], moves[i][0], moves[i][1]])
           change = moveChange(change, moves_made)
           pieces[selected][2] = moves[i][0]
           pieces[selected][3] = moves[i][1]
           if pawn:
               pawn_moved = True
           if pawn_moved and not (pieces[selected][3]==0 or pieces[selected][3]==7) or not pawn_moved:
                selected = -1
                pawn_moved = False
           break
    for i in range(len(captures)):
        pygame.draw.rect(screen, green, [int(captures[i][0]*SQUARE_SIZE), int(captures[i][1]*SQUARE_SIZE), int(SQUARE_SIZE), int(SQUARE_SIZE)])
        pygame.draw.rect(screen, black, [int(captures[i][0]*SQUARE_SIZE), int(captures[i][1]*SQUARE_SIZE), int(SQUARE_SIZE), int(SQUARE_SIZE)], 5)
        if checkClick(captures[i][0], captures[i][1]) and not selected==-1:
           moves_made.append([getPiece(pieces[selected]), pieces[selected][2], pieces[selected][3], captures[i][0], captures[i][1], getPiece(other_pieces[captures[i][2]])])
           change = moveChange(change, moves_made)
           pieces[selected][2] = captures[i][0]
           pieces[selected][3] = captures[i][1]
           other_pieces[captures[i][2]][1] = False
           if pawn:
               pawn_moved = True
           if pawn_moved and not (pieces[selected][3]==0 or pieces[selected][3]==7) or not pawn_moved:
                selected = -1
                pawn_moved = False
           break

    #this whole part lets the user pick their reward for getting thier pawn to thier opponents side
    if(pawn_moved):
        
        while not selected==-1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            if pygame.mouse.get_pressed()[0] and height//4 + 50<pygame.mouse.get_pos()[1] and height//4 + 200>pygame.mouse.get_pos()[1]:
                if  board_width//2 - 270<pygame.mouse.get_pos()[0] and board_width//2 - 150>pygame.mouse.get_pos()[0]:
                    if(direction==-1):
                        pieces[selected][0] = WHITE_QUEEN
                        moves_made.append(["White Pawn", "white Queen"])
                        change = moveChange(change, moves_made)
                        selected=-1
                    else:
                        pieces[selected][0] = BLACK_QUEEN
                        moves_made.append(["Black Pawn", "Black Queen"])
                        change = moveChange(change, moves_made)
                        selected=-1
                elif  board_width//2 - 130<pygame.mouse.get_pos()[0] and board_width//2 - 10>pygame.mouse.get_pos()[0]:
                    if(direction==-1):
                        pieces[selected][0] = WHITE_KNIGHT
                        moves_made.append(["White Pawn", "white Knight"])
                        change = moveChange(change, moves_made)
                        selected=-1
                    else:
                        pieces[selected][0] = BLACK_KNIGHT
                        moves_made.append(["Black Pawn", "Black Knight"])
                        change = moveChange(change, moves_made)
                        selected=-1
                elif  board_width//2 + 10<pygame.mouse.get_pos()[0] and board_width//2 + 130>pygame.mouse.get_pos()[0]:
                    if(direction==-1):
                        pieces[selected][0] = WHITE_ROOK
                        moves_made.append(["White Pawn", "white Rook"])
                        change = moveChange(change, moves_made)
                        selected=-1
                    else:
                        pieces[selected][0] = BLACK_ROOK
                        moves_made.append(["Black Pawn", "Black Rook"])
                        change = moveChange(change, moves_made)
                        selected=-1
                elif  board_width//2 + 150<pygame.mouse.get_pos()[0] and board_width//2 + 270>pygame.mouse.get_pos()[0]:
                    if(direction==-1):
                        pieces[selected][0] = WHITE_BISHOP
                        moves_made.append(["White Pawn", "white Bishop"])
                        change = moveChange(change, moves_made)
                        selected=-1
                    else:
                        pieces[selected][0] = BLACK_BISHOP
                        moves_made.append(["Black Pawn", "Black Bishop"])
                        change = moveChange(change, moves_made)
                        selected=-1
            for i in range(len(pieces)):
                if pieces[i][1]:
                    screen.blit(pieces[i][0], [int(pieces[i][2]*SQUARE_SIZE+offset_X), int(pieces[i][3]*SQUARE_SIZE+offset_Y)])
                if other_pieces[i][1]:
                    screen.blit(other_pieces[i][0], [int(other_pieces[i][2]*SQUARE_SIZE+offset_X), int(other_pieces[i][3]*SQUARE_SIZE+offset_Y)])
            
            
            
            if(direction==-1):
                text = font.render("What piece would you like in place of your pawn:", False, white)
                pygame.draw.rect(screen, black, [board_width//2 - text.get_width()//2-10, height//4 - text.get_height()//2, 800, 250])
                pygame.draw.rect(screen, white, [board_width//2 - 270, height//4 + 50, 120, 150], 5)
                pygame.draw.rect(screen, white, [board_width//2 - 130, height//4 + 50, 120, 150], 5)
                pygame.draw.rect(screen, white, [board_width//2 + 10, height//4 + 50, 120, 150], 5)
                pygame.draw.rect(screen, white, [board_width//2 + 150, height//4 + 50, 120, 150], 5)
                screen.blit(WHITE_QUEEN, [board_width//2 - 260, height//4 +70])
                screen.blit(WHITE_KNIGHT, [board_width//2 - 120, height//4 +70])
                screen.blit(WHITE_ROOK, [board_width//2 + 20, height//4 +70])
                screen.blit(WHITE_BISHOP, [board_width//2 + 160, height//4 +70])
            else:
                text = font.render("What piece would you like in place of your pawn:", False, black)
                pygame.draw.rect(screen, white, [board_width//2 - text.get_width()//2-10, height//4 - text.get_height()//2, 600, 200])
                pygame.draw.rect(screen, black, [board_width//2 - 270, height//4 + 50, 120, 150], 5)
                pygame.draw.rect(screen, black, [board_width//2 - 130, height//4 + 50, 120, 150], 5)
                pygame.draw.rect(screen, black, [board_width//2 + 10, height//4 + 50, 120, 150], 5)
                pygame.draw.rect(screen, black, [board_width//2 + 150, height//4 + 50, 120, 150], 5)
                screen.blit(BLACK_QUEEN, [board_width//2 - 260, height//4 +70])
                screen.blit(BLACK_KNIGHT, [board_width//2 - 120, height//4 +70])
                screen.blit(BLACK_ROOK, [board_width//2 + 20, height//4 +70])
                screen.blit(BLACK_BISHOP, [board_width//2 + 160, height//4 +70])
            screen.blit(text, [board_width//2 - text.get_width()//2, height//4 - text.get_height()//2])
            pygame.display.flip()
            screen.blit(board, boardrect)
    return pieces, other_pieces, selected, moves_made, change

"""def checkWIN(pieces, other_pieces):
    for i in range(len(pieces)):
        if pieces[i][0] is WHITE_KING or pieces[i][0] is BLACK_KING:
            for j in range(len(other_pieces)):

def inCheck():
    for i in range(len(pieces)):
        if pieces[i][0] is WHITE_KING or pieces[i][0] is BLACK_KING:
            for j in range(len(other_pieces)):"""

    


#This is the main loop that runs the game
while not tie and not white_win and not black_win:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
     
    screen.blit(board, boardrect)
    if not piece_selected==-1 and white_turn:
        white_pieces, black_pieces, piece_selected, list_moves, change = availableMoves(white_pieces, black_pieces, -1, piece_selected, list_moves, change)
        if piece_selected==-1:
            white_turn = not white_turn
    elif not piece_selected==-1 and not white_turn:
        black_pieces, white_pieces, piece_selected, list_moves, change = availableMoves(black_pieces, white_pieces, 1, piece_selected, list_moves, change)
        if piece_selected==-1:
            white_turn = not white_turn

    piece_selected = displayPieces(piece_selected)
    change = displayMoves(list_moves, change)
    pygame.display.flip()