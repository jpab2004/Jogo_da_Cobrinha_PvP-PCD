from tabulate import tabulate as tb
import random as rd
import pygame as pg
import numpy as np
import time as t
import pyautogui
import sys

pg.init()

flags = pg.SHOWN | pg.NOFRAME | pg.FULLSCREEN

screen_size = pyautogui.size()

dis_width, dis_height = screen_size
game_percentage = 0.93
dis_height *= game_percentage

zoom = 45

col, row = int(dis_width / zoom), int(dis_height / zoom)
#col, row = 30, 30
square_w, square_h = dis_width / col, dis_height / row
clock = (zoom/10000)**(1/2)

IA = False
back_line = False

font_scale = 1
if row < col:
    font_size = int(square_h * font_scale)
else:
    font_size = int(square_w * font_scale)

dis = pg.display.set_mode((dis_width, dis_height), flags)
pg.display.set_caption('Jogo da Cobrinha!')

#font_style = pg.font.SysFont('Time New Roman', int(dis_width * font_scale))
font_game = pg.font.SysFont('Comic Sans MS', font_size)
font_score = pg.font.SysFont('Comic Sans MS', int(750 * (1 - game_percentage)))
font_reset = pg.font.SysFont('Comic Sans MS', int(screen_size[1] * 0.05))

game = np.zeros((row, col))
initial_head_pos = [int(row / 2), int(col / 2)]
head = initial_head_pos
game[head[0]][head[1]] = 2

blocks = []
block_limit = 5
block_apple_radius = 1
block_head_radius = 2
placed_blocks = 0

score = 0
apple_position = []
tail = []
dir = 1

background_color = (30, 30, 30)
apple_color = (255, 0, 0)
tail_color = (50, 50, 255)
head_color = (255, 50, 255)
block_color = (117, 117, 117)
score_color = (255, 255, 50)
reset_background_color = (75, 147, 219)
reset_square_background_color = (30, 30, 30)
reset_text_color = (140, 245, 148)

if back_line:
    line_color = (55, 55, 55)
else:
    line_color = background_color

def create_tail(n):
    for i in range(1, n + 1):
        tail.append([head[0], head[1] - i])

def show_tail():
    for i in tail:
        game[i[0]][i[1]] = 1

def find_cor(n):
    if n == 0:
        return background_color
    elif n == 1:
        return tail_color
    elif n == 2:
        return head_color
    elif n == -1:
        return apple_color
    elif n == -2:
        return block_color

def line(start, end, color):
    pg.draw.line(dis, color, start, end, 2)
    return

def write_game(mesg, pos, cor):
    msg = font_game.render(mesg, True, cor)
    dis.blit(msg, pos)
    return
    
def write_score(mesg, pos, cor):
    msg = font_score.render(mesg, True, cor)
    dis.blit(msg, pos)
    return
    
def write_reset(mesg, pos, cor):
    msg = font_reset.render(mesg, True, cor)
    dis.blit(msg, pos)
    return

def matrix():
    pg.draw.rect(dis, background_color, (0, 0, screen_size[0], screen_size[1]))

    for i in range(1, row):
        start = (0, square_h * i)
        end = (dis_width, square_h * i)
        line(start, end, line_color)
    
    for i in range(1, col):
        start = (square_w * i, 0)
        end = (square_w * i, dis_height)
        line(start, end, line_color)

    return
    
def draw_score():
    score_msg = f'Score: {score}'
    block_score = f'Blocos colocados: {placed_blocks}'
    
    score_w, score_h = font_score.size(score_msg)
    block_score_w, block_score_h = font_score.size(block_score)
    
    pos = [screen_size[0] * 0.01, (screen_size[1] * (game_percentage + (1 - game_percentage) / 2)) - (score_h / 2)]
    pos_block_score = [screen_size[0] - block_score_w - screen_size[0] * 0.01, (screen_size[1] * (game_percentage + (1 - game_percentage) / 2)) - (block_score_h / 2)]
    
    write_score(score_msg, pos, score_color)
    write_score(block_score, pos_block_score, score_color)
    
    line([0,dis_height], [dis_width, dis_height], (255, 255, 255))

def turn_m():
    game2 = np.char.mod('%s', game)

    for i in range(block_limit):
        game2 = np.char.replace(game2, '-2', '#')

    game2 = np.char.replace(game2, '2', 'O')
    game2 = np.char.replace(game2, '0', ' ')
    game2 = np.char.replace(game2, '-1', '©')
    game2 = np.char.replace(game2, '1', 'o')
    return game2

def update_screen():
    matrix()
    draw_score()
    
    gameDis = turn_m()
    for i in range(row):
        for j in range(col):
            msg = '%s' % gameDis[i][j]
            msg = msg[:-2]
            text_w, text_h = font_game.size(msg)

            cor = find_cor(game[i][j])

            pos = [(square_w * j) + (square_w / 2) - (text_w / 2), (square_h * i) + (square_h / 2) - (text_h / 2)]
            write_game(msg, pos, cor)
    pg.display.update()

def game_over():
    print('Game Over!')
    
    reset_msg = 'Aperte ESC para sair do jogo ou R para reiniciar o jogo!'
    reset_text_w, reset_text_h = font_reset.size(reset_msg)
    
    reset_square_pos = ((screen_size[0] / 2) - (reset_text_w / 2) - (screen_size[0] * 0.02), (screen_size[1] / 2) - (reset_text_h / 2) - (screen_size[1] * 0.02),
                         reset_text_w + (screen_size[0] * 0.04), reset_text_h + (screen_size[1] * 0.04))
    
    pg.draw.rect(dis, reset_background_color, (0, 0, screen_size[0], screen_size[1]))
    pg.draw.rect(dis, reset_square_background_color, reset_square_pos)
    
    reset_text_pos = [(screen_size[0] / 2) - (reset_text_w / 2), (screen_size[1] / 2) - (reset_text_h / 2)]
    write_reset(reset_msg, reset_text_pos, reset_text_color)
    
    pg.display.update()
    
    while True:
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif e.key == pg.K_r:
                    reset_game()
                    update_screen()
                    return
        t.sleep(clock)
    
def remove_around_apple(row, column):
    for y in range(-block_apple_radius, block_apple_radius + 1):
        for x in range(-block_apple_radius, block_apple_radius + 1):
            try:
                if game[row + x][column + y] == -2:
                    game[row + x][column + y] = 0
            except:
                continue

def create_apple():
    rdr = rd.randint(0, row - 1)
    rdc = rd.randint(0, col - 1)
    while(game[rdr][rdc] != 0):
        rdr = rd.randint(0, row - 1)
        rdc = rd.randint(0, col - 1)
        
    remove_around_apple(rdr, rdc)
        
    global apple_position
    apple_position = [rdr, rdc]
        
    game[rdr][rdc] = -1

def elong_tail():
    tail.append(tail[-1])

def update_tail(head):
    aux = tail.pop()
    game[aux[0]][aux[1]] = 0
    tail.insert(0, head)
    for i in tail:
        game[i[0]][i[1]] = 1

def update_dir(dir):
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
    if destiny == 1 or destiny == -2:
        game_over()
        return initial_head_pos
    if destiny == -1:
        elong_tail()
        global score
        score += 1
        create_apple()
    
    head_new = [new_row, new_col]

    update_tail(head)
    
    game[head_new[0]][head_new[1]] = 2
    print(tb(game))
    return head_new

def check_if_apple(box_row, box_column):
    x_apple = apple_position[0]
    y_apple = apple_position[1]
    
    for y in range(-block_apple_radius, block_apple_radius + 1):
        for x in range(-block_apple_radius, block_apple_radius + 1):
            try:
                if x_apple + x == box_row and y_apple + y == box_column:
                    return True
            except:
                continue
                
def check_if_head(box_row, box_column):
    x_head = head[0]
    y_head = head[1]
    
    for y in range(-block_head_radius, block_head_radius + 1):
        for x in range(-block_head_radius, block_head_radius + 1):
            try:
                if x_head + x == box_row and y_head + y == box_column:
                    return True
            except:
                continue

def create_block(pos):
    x = pos[0]
    y = pos[1]

    if x > dis_width or y > dis_height:
        return
    
    box_row = int(y / square_h)
    box_column = int(x / square_w)
    
    #print(f'X value: {x}\nY value: {y}\n\nBox: [{box_row},{box_column}]')

    if game[box_row][box_column] != 0:
        return
        
    if check_if_apple(box_row, box_column):
        return
    
    if check_if_head(box_row, box_column):
        return

    if len(blocks) < block_limit:
        game[box_row][box_column] = -2
        blocks.append([box_row, box_column])
    else:
        remove = blocks.pop(0)
        game[remove[0]][remove[1]] = 0
        game[box_row][box_column] = -2
        blocks.append([box_row, box_column])
    global placed_blocks 
    placed_blocks += 1
        

def reset_game():
    global game, head, blocks, placed_blocks, score, apple_position, tail, dir
    game = np.zeros((row, col))
    head = initial_head_pos
    game[head[0]][head[1]] = 2

    blocks = []
    placed_blocks = 0
    
    score = 0
    apple_position = []
    tail = []
    dir = 1

    create_tail(2)
    show_tail()
    
    create_apple()
    
    update_screen()
    pg.display.update()
    t.sleep(1)

reset_game()
print(tb(game))
t.sleep(clock)

while True:
    for e in pg.event.get():
        if e.type == pg.MOUSEBUTTONDOWN:
            create_block(pg.mouse.get_pos())
            break
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_r:
                reset_game()
            if e.key == pg.K_ESCAPE:
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
        if e.type != pg.MOUSEBUTTONDOWN:
            print('Throwaway!')

    head = update_dir(dir)
    update_screen()

    if IA:
        clock = 1 / (len(tail) + 1)
    
    t.sleep(clock)
