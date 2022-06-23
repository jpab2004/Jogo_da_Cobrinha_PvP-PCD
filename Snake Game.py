from tabulate import tabulate as tb
import random as rd
import pygame as pg
import numpy as np
import time as t
import sys

pg.init()

flags = pg.SHOWN | pg.NOFRAME | pg.FULLSCREEN
dis_width, dis_height = 1920, 1080
col, row = int(dis_width / 100), int(dis_height / 100)
square_w, square_h = dis_width / col, dis_height / row
clock = 0.2

IA = False

font_scale = 1
if row < col:
    font_size = int(square_h * font_scale)
else:
    font_size = int(square_w * font_scale)

dis = pg.display.set_mode((dis_width, dis_height), flags)
pg.display.set_caption('Jogo da Cobrinha!')

#font_style = pg.font.SysFont('Time New Roman', int(dis_width * font_scale))
font_style = pg.font.SysFont('Comic Sans MS', font_size)

game = np.zeros((row, col))
head = [0, 2]
game[head[0]][head[1]] = 2

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (50, 50, 255)
pink = (255, 50, 255)

tail = []

def create_tail(n):
    for i in range(1, n + 1):
        tail.append([head[0], head[1] - i])

create_tail(2)

for i in tail:
        game[i[0]][i[1]] = 1

dir = 1

def find_cor(n):
    if n == 0:
        return white
    elif n == 1:
        return blue
    elif n == 2:
        return pink
    elif n == -1:
        return red

def line(start, end, color):
    pg.draw.line(dis, color, start, end, 2)
    return

def write_s(mesg, pos, cor):
    msg = font_style.render(mesg, True, cor)
    dis.blit(msg, pos)
    return

def matrix():
    pg.draw.rect(dis, black, (0, 0, dis_width, dis_height))

    for i in range(1, row):
        start = (0, square_h * i)
        end = (dis_width, square_h * i)
        line(start, end, white)
    
    for i in range(1, col):
        start = (square_w * i, 0)
        end = (square_w * i, dis_height)
        line(start, end, white)

    return

def update_m():
    matrix()
    for i in range(row):
        for j in range(col):
            msg = '%i' % game[i][j]
            text_w, text_h = font_style.size(msg)

            cor = find_cor(game[i][j])

            pos = [(square_w * j) + (square_w / 2) - (text_w / 2), (square_h * i) + (square_h / 2) - (text_h / 2)]
            write_s(msg, pos, cor)
    pg.display.update()

def game_over():
    print('Game Over!')
    pg.quit()
    sys.exit()

def create_apple():
    rdr = rd.randint(0, row - 1)
    rdc = rd.randint(0, col - 1)
    while(game[rdr][rdc] != 0):
        rdr = rd.randint(0, row - 1)
        rdc = rd.randint(0, col - 1)
    game[rdr][rdc] = -1

def elong_tail():
    tail.append(tail[-1])

def update_tail(head):
    aux = tail.pop()
    game[aux[0]][aux[1]] = 0
    tail.insert(0, head)
    for i in tail:
        game[i[0]][i[1]] = 1

def update(dir):
    if dir == 0:
        new_row = head[0] - 1
        new_col = head[1]
    if dir == 1:
        new_row = head[0]
        new_col = head[1] + 1
    if dir == 2:
        new_row = head[0] + 1
        new_col = head[1]
    if dir == 3:
        new_row = head[0]
        new_col = head[1] - 1

    if new_row < 0:
        new_row = row - 1
    if new_row > row - 1:
        new_row = 0
    if new_col < 0:
        new_col = col - 1
    if new_col > col - 1:
        new_col = 0

    destiny = game[new_row][new_col]
    if destiny == 1:
        game_over()
    if destiny == -1:
        elong_tail()
        create_apple()
    
    head_new = [new_row, new_col]

    update_tail(head)
    
    game[head_new[0]][head_new[1]] = 2
    print(tb(game))
    return head_new


create_apple()
print(tb(game))
update_m()
t.sleep(clock)

while True:
    for e in pg.event.get():
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_q:
                print('Game closed!')
                pg.quit()
                sys.exit()
            elif (e.key == pg.K_UP or e.key == pg.K_w) and (dir != 2):
                dir = 0
                break
            elif (e.key == pg.K_RIGHT or e.key == pg.K_d) and (dir != 3):
                dir = 1
                break
            elif (e.key == pg.K_DOWN or e.key == pg.K_s) and (dir != 0):
                dir = 2
                break
            elif (e.key == pg.K_LEFT or e.key == pg.K_a) and (dir != 1):
                dir = 3
                break
    
    for e in pg.event.get():
        print('Throwaway!')

    head = update(dir)
    update_m()

    if IA:
        clock = 1 / (len(tail) + 1)
    
    t.sleep(clock)
