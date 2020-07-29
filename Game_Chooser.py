#Written by: Nikolas Pensyl
#Started on: 4/19/2020
#Last Modified: 4/22/2020
import sys, pygame
pygame.init()

white = 255, 255, 255

def start():
    game_chosen = -1
    games = [["Chess", "Chess\Chess.py"], ["pong", "pong.py"]]
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("comicsansms", 20)
    while game_chosen == -1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
        for i in range(len(games)):
            pygame.draw.rect(screen, white, [(i%4)*250+25, (i//4)*150+50, 200, 100], 5)
            text = font.render(games[i][0], False, white)
            screen.blit(text, [(i%4)*250+125 - text.get_width()//2, (i//4)*150+100 - text.get_height()//2])
            if pygame.mouse.get_pressed()[0] and (i%4)*250+25<pygame.mouse.get_pos()[0] and (i%4)*250+225>pygame.mouse.get_pos()[0] and (i//4)*150+50<pygame.mouse.get_pos()[1] and (i//4)*150+150>pygame.mouse.get_pos()[1]:
                game_chosen = i
        pygame.display.flip()
    pygame.display.quit()
    if games[game_chosen][0] == "pong":
        import pong
    elif games[game_chosen][0] == "Chess":
        from Chess import Chess
    exec(open((games[game_chosen][1])).read())
    

start()
