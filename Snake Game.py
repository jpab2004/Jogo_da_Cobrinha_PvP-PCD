from tabulate import tabulate as tb
import random as rd
import pygame as pg
import numpy as np
import time as t
import sys

pg.init()

dis_width, dis_height = 500, 500
row, col = 20, 20
clock = 0.5

game = np.zeros((row, col))
head = [10, 10]
game[head[0]][head[0]] = 2

tail = []

def create_tail(n):
    for i in range(1, n + 1):
        tail.append([head[0], head[1] - i])

create_tail(2)

for i in tail:
        game[i[0]][i[1]] = 1

dir = 1

dis = pg.display.set_mode((dis_width, dis_height))
pg.display.set_caption('Jogo da Cobrinha!')

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
    
    t.sleep(clock)
