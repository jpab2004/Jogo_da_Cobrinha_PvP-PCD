import pygame as pg
import numpy as np
import sys

pg.init()

font_style = pg.font.SysFont("Time New Roman", 20)

flags = pg.SHOWN | pg.NOFRAME #| pg.FULLSCREEN
dis_w, dis_h = 1000, 1000
row, col = 20, 20
square_w, square_h = dis_w / row, dis_h / col

game = np.zeros((row, col))

screen = pg.display.set_mode((dis_w, dis_h), flags, 32)
pg.display.set_caption('Testes!')

white = (255, 255, 255)
red = (255, 0, 0)

def line(start, end, color):
    pg.draw.line(screen, color, start, end, 2)
    return

def write_s(mesg, pos):
    msg = font_style.render(mesg, True, white)
    screen.blit(msg, pos)

def matrix():
    for i in range(1, row):
        start = (square_w * i, 0)
        end = (square_w * i, dis_h)
        line(start, end, white)

    for i in range(1, col):
        start = (0, square_h * i)
        end = (dis_w, square_h * i)
        line(start, end, white)

    pg.display.update()
    return

def update_m():
    matrix()
    for i in range(col):
        for j in range(row):
            msg = '%i, %i' % (i, j)
            text_w, text_h = font_style.size(msg)
            
            pos = [(square_w * j) + (square_w / 2) - (text_w / 2), (square_h * i) + (square_h / 2) - (text_h / 2)]
            write_s(msg, pos)

update_m()
pg.display.update()



running = True
while running:
    for e in pg.event.get():
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_q:
                running = False

print('Close')
pg.quit()
sys.exit()
