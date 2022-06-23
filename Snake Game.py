import random as rd
import pygame
import time as t

pygame.init()

yellow = (255,255,75)
green = (0,255,100)
white = (255, 255, 255)
black = (45, 45, 45)
red = (255, 50, 0)
blue = (75,150,255)
blackb = (0, 0, 0)

dis_height = 600
dis_width = 800

dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption('Jogo da cobrinha')

clock = pygame.time.Clock()

snake_speed = 15
PixelSize = 10

font_style = pygame.font.SysFont("comicsansms", 25)
score_font = pygame.font.SysFont("comicsansms", 25)

def pontuacao(score):
    valor = score_font.render("Pontuação: " + str(score), True, yellow)
    dis.blit(valor, [10, 10])

def cobrinha(PixelSize, snake_lista):
    for i in snake_lista:
        pygame.draw.rect(dis, blue, [i[0], i[1], PixelSize, PixelSize])

def message(msg,color):
    mesg = font_style.render(msg, True, color)

    text_w, text_h = font_style.size(msg)

    dis.blit(mesg, [dis_width/2 - text_w/2, dis_height/2 - text_h/2])

    rect = pygame.Rect(dis_width/2 -text_w/2 - 10, dis_height/2 -text_h/2 - 10, text_w + 20, text_h + 20)
    pygame.draw.rect(dis, blackb, rect)
    dis.blit(mesg, [dis_width/2 - text_w/2, dis_height/2 - text_h/2])

def gameLoop():  # creating a function
    game_over = False
    game_close = False

    x1 = dis_height/2
    y1 = dis_width/2
    
    x1_change = 0       
    y1_change = 0
 
    snake_lista = []
    snake_lenght = 1
 
    foodx = round(rd.randrange(2*PixelSize, dis_width - 2*PixelSize) / 10.0) * 10.0
    foody = round(rd.randrange(2*PixelSize, dis_width - 2*PixelSize) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Game Over! Aperte C-Jogar novamente ou Q-Sair", red)
 
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            # print(event)
            if event.type==pygame.QUIT:
                game_over=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and (x1_change == 0 or snake_lenght <= 2):
                    x1_change = -PixelSize
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and (x1_change == 0 or snake_lenght <= 2):
                    x1_change = PixelSize
                    y1_change = 0
                elif event.key == pygame.K_UP and (y1_change == 0 or snake_lenght <= 2):
                    y1_change = -PixelSize
                    x1_change = 0
                elif event.key == pygame.K_DOWN and (y1_change == 0 or snake_lenght <= 2):
                    y1_change = PixelSize
                    x1_change = 0

        if x1 >= dis_width or x1 < -PixelSize or y1 >= dis_height or y1 < -PixelSize:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, red, [foodx, foody, PixelSize, PixelSize])
        cabeca_snake = []
        cabeca_snake.append(x1)
        cabeca_snake.append(y1)
        snake_lista.append(cabeca_snake)
        if len(snake_lista) > snake_lenght:
            del snake_lista[0]

        for i in snake_lista[:-1]:
            if i == cabeca_snake:
                game_close = True

        cobrinha(PixelSize, snake_lista)
        pontuacao(snake_lenght - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            print("Comida oba")
            foodx = round(rd.randrange(PixelSize, dis_width - PixelSize) / 10.0) * 10.0
            foody = round(rd.randrange(PixelSize, dis_height - PixelSize) / 10.0) * 10.0
            snake_lenght += 1

        clock.tick(snake_speed)

    message("Game over! >:3", red)
    pygame.display.update()
    t.sleep(2)

    pygame.quit()
    quit()

gameLoop()