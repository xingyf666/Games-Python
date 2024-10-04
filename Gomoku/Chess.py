import pygame
from pygame.locals import *
import sys
import cc

pygame.init()
pygame.mixer.init()

size = width, height = 881, 681
WHITE = 255, 255, 255
screen = pygame.display.set_mode(size)
pygame.display.set_caption('五子棋')
clock = pygame.time.Clock()
background = pygame.image.load("images//棋盘.png").convert_alpha()
white = pygame.image.load("images//白棋.png").convert_alpha()
black = pygame.image.load("images//黑棋.png").convert_alpha()
victory = pygame.image.load("images//胜利.png").convert_alpha()
defeat = pygame.image.load("images//失败.png").convert_alpha()
beside = pygame.image.load("images//侧面.png").convert_alpha()
menu_1 = pygame.image.load("images//菜单1.png").convert_alpha()
regret_1 = pygame.image.load("images//悔棋1.png").convert_alpha()
new_1 = pygame.image.load("images//新局1.png").convert_alpha()
menu_2 = pygame.image.load("images//菜单2.png").convert_alpha()
regret_2 = pygame.image.load("images//悔棋2.png").convert_alpha()
new_2 = pygame.image.load("images//新局2.png").convert_alpha()
regret_3 = pygame.image.load("images//悔棋3.png").convert_alpha()
menu_3 = pygame.image.load("images//菜单3.png").convert_alpha()

pygame.mixer.music.load("music//棋魂钢琴曲.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

play = pygame.mixer.Sound("music//下棋.wav")
play.set_volume(0.5)
win_sound = pygame.mixer.Sound("music//胜利.wav")
win_sound.set_volume(0.5)
lose_sound = pygame.mixer.Sound("music//失败.wav")
lose_sound.set_volume(0.5)

def main():
    Board = cc.Game()
    running = True
    side = 0
    chess = []
    begin = True
    new = False
    menu = False
    regret = False
    count = 0
    over = False
    menu_open = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type==MOUSEBUTTONDOWN and event.button==1:
                pos = event.pos
                x = pos[0] // 40
                y = pos[1] // 40
                if 0<x<16 and 0<y<16 and Board.board[y-1][x-1]==0 and begin:
                    Board.x = x
                    Board.y = y
                    chess.append((0, (x*40, y*40)))
                    play.play()
                    count += 1
                    side = 1

                if 691<pos[0]<691+180 and 30<pos[1]<30+100:
                    new = True
                elif 691<pos[0]<691+180 and 160<pos[1]<160+100 and begin and count:
                    regret = True
                elif 691<pos[0]<691+180 and 290<pos[1]<290+100:
                    menu = True

            elif event.type==MOUSEBUTTONUP and event.button==1:
                if new:
                    Board = cc.Game()
                    begin = True
                    side = 0
                    chess = []
                    new = False
                    count = 0
                    over = False

                if regret:
                    regret = False
                    count -= 1
                    
                    x = chess[-1][1][0] // 40
                    y = chess[-1][1][1] // 40
                    Board.board[y-1][x-1] = 0
                    chess.pop()

                    x = chess[-1][1][0] // 40
                    y = chess[-1][1][1] // 40
                    Board.board[y-1][x-1] = 0
                    chess.pop()

                if menu:
                    menu = False
                    menu_open = not menu_open
                
        if side==1:
            Board.game()
            if Board.win==0:
                chess.append((1, (Board.x*40, Board.y*40)))
            side = 0
            Board.check_five()

        screen.blit(background, (0, 0))
        screen.blit(beside, (681, 0))

        if new:
            screen.blit(new_2, (681+10, 30))
        else:
            screen.blit(new_1, (681+10, 30))

        if regret:
            screen.blit(regret_2, (681+10, 160))
        elif begin and count:
            screen.blit(regret_1, (681+10, 160))
        else:
            screen.blit(regret_3, (681+10, 160))

        if menu:
            screen.blit(menu_2, (681+10, 290))
        else:
            screen.blit(menu_1, (681+10, 290))

        for each in chess:
            if each[0]==0:
                screen.blit(white, each[1])
            else:
                screen.blit(black, each[1])

        if Board.win==-1:
            if not over:
                win_sound.play()
                over = True
            screen.blit(victory, (0, 0))
            begin = False
        elif Board.win==-2:
            if not over:
                lose_sound.play()
                over = True
            screen.blit(defeat, (0, 0))
            begin = False

        if menu_open:
            screen.blit(menu_3, (240, 140))
        
        pygame.display.flip()
        clock.tick(30)

    
if __name__ == '__main__':
    main()
