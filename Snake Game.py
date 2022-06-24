######## Integrantes:
######## João Pedro Aroucha de Brito
######## Lorraine Cristina Silva Casseano
######## Monyque Karolina de Paula Silva
######## Pedro Henrique Sophia


##### Importação e definição de alias para bibliotecas
from tabulate import tabulate as tb
import random as rd
import pygame as pg
import numpy as np
import time as t
import pyautogui
import sys

#####


# Inicialização do PyGame
pg.init()


# Definição das flags(opções) do PyGame
flags = pg.SHOWN | pg.NOFRAME | pg.FULLSCREEN


# Obtenção do tamanho da tela (largura e altura = width, height)
screen_size = pyautogui.size()


# Definição da área jogável (93% da tela)
dis_width, dis_height = screen_size
game_percentage = 0.93
dis_height *= game_percentage


# Definição do zoom do jogo, aproximação da tela
zoom = 45


# Definição da quantidade de linhas e colunas da matriz em relação a tela (row, col)
col, row = int(dis_width / zoom), int(dis_height / zoom)


# Definição do tamanho de cada quadrado/célula do jogo
square_w, square_h = dis_width / col, dis_height / row


# Definição do timer do jogo (clock)
clock = (zoom / 10000) ** (1 / 2)


# Definição das opções do jogo
IA = False  # IA ativada
back_line = False  # Linhas do fundo da tela (matriz)


# Definição do tamanho da fonte para os caracteres do jogo
font_scale = 1
if row < col:
    font_size = int(square_h * font_scale)
else:
    font_size = int(square_w * font_scale)
# Definição das fontes para o jogo, sistema de score e tela de game over
font_game = pg.font.SysFont("Comic Sans MS", font_size)
font_score = pg.font.SysFont("Comic Sans MS", int(750 * (1 - game_percentage)))
font_reset = pg.font.SysFont("Comic Sans MS", int(screen_size[1] * 0.05))


# Obtenção do display do PyGame
dis = pg.display.set_mode((dis_width, dis_height), flags)


# Setando o nome da tela do jogo
pg.display.set_caption("Jogo da Cobrinha!")


# Criação da matriz do jogo
game = np.zeros((row, col))


# Definição da posição inicial da cobrinha para o meio da matriz
initial_head_pos = [int(row / 2), int(col / 2)]


# Setando a posição da cabeça da cobra e colocando-a na matriz do game
head = initial_head_pos
game[head[0]][head[1]] = 2


# Definição das variáveis para o sistema de blocos
blocks = []  # Posição de cada bloco
block_limit = 5  # Limite de blocos
block_apple_radius = 1  # Raio de restrição ao redor da maçã
block_head_radius = 2  # Raio de restrição ao redor da cabeça da cobra
placed_blocks = 0  # Quantidade de blocos colocados


# Definição da variável de pontos (quantidade de maçãs comidas)
score = 0


# Definição da variável que guardará a posição da maçã
apple_position = []


# Definição da lista de posições de cada segmento da cauda
tail = []


# Definição da direção de deslocamento da cobra
dir = 1


# Definição das cores utilizadas
background_color = (30, 30, 30)  # Fundo
apple_color = (255, 0, 0)  # Maçã
tail_color = (50, 50, 255)  # Cauda da cobra
head_color = (255, 50, 255)  # Cabeça da cobra
block_color = (117, 117, 117)  # Blocos
score_color = (255, 255, 50)  # Escrita do Score
reset_background_color = (75, 147, 219)  # Fundo do game over
reset_square_background_color = (30, 30, 30)  # Quadrado do texto do game over
reset_text_color = (140, 245, 148)  # Escrita do game over


# Verificação e definição da cor das linhas
if back_line:
    line_color = (55, 55, 55)
else:
    line_color = background_color
# Função para criação da cauda da cobra
def create_tail(n):
    """
    Função para criação da cauda da cobra

    A função pegará a posição da cabeça da cobra e colocará a cauda para a esquerda da cobra

    Vars:
        n: quantidade de segmentos que a cauda terá
    """
    for i in range(1, n + 1):
        tail.append([head[0], head[1] - i])


# Função para colocar a cauda dentro da matriz do jogo
def show_tail():
    """A função pegará as posições da cauda da cobra e as colocará dentro da matriz principal do jogo"""
    for i in tail:
        game[i[0]][i[1]] = 1


# Função para pegar a cor do caractere de acordo com o objeto
def find_cor(n):
    """
    Função para definição de cor de acordo com o objeto

    A função pegará a variável 'n' e definirá a cor do objeto de acordo com seu número

    Vars:
        n: número que representa o objeto a definir sua cor

    Returns: A função retornará a cor desejada para o objeto
    """
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


# Função para criação de uma linha na tela
def line(start, end, color):
    """
    Função para criação de uma linha na tela

    A função criará uma linha na tela do jogo de acordo com as informações passadas

    Vars:
        start: Posição inicial da linha
        end: Posição final da linha
        color: Cor a ser usada para a linha
    """
    pg.draw.line(dis, color, start, end, 2)
    return


# Função para escrever os caracteres do jogo
def write_game(mesg, pos, cor):
    """
    Função para escrever os caracteres do jogo

    A função escreverá na tela os caracteres responsáveis por representar todos os objetos

    Vars:
        mesg: O caractere a ser representado (Ex. '#' = Bloco)
        pos: Posição do caractere na tela
        cor: Cor que será usada para escrever o caractere
    """
    msg = font_game.render(mesg, True, cor)
    dis.blit(msg, pos)
    return


# Função encarregada de escrever utilizando a fonte de score na tela
def write_score(mesg, pos, cor):
    """
    Função encarregada de escrever utilizando a fonte de score na tela

    A função escreverá o score na posição desejada

    Vars:
        mesg: Mensagem a ser escrita
        pos: Posição que será escrito o score
        cor: Cor que será escrito o score
    """
    msg = font_score.render(mesg, True, cor)
    dis.blit(msg, pos)
    return


# Função encarregada de escrever utilizando a fonte de game over na tela
def write_reset(mesg, pos, cor):
    """
    Função encarregada de escrever utilizando a fonte de game over na tela

    A função escreverá o texto da tela de game over na posição desejada

    Vars:
        mesg: Mensagem a ser escrita
        pos: Posição que será escrito o texto de game over
        cor: Cor que será escrito o texto de game over
    """
    msg = font_reset.render(mesg, True, cor)
    dis.blit(msg, pos)
    return


# Função encarregada de desenhar a matriz na tela do jogo
def matrix():
    """
    Função encarregada de desenhar a matriz na tela do jogo

    A função irá pintar a tela com a cor de background definida e depois irá desenhar as linhas da matriz, formando uma grade que será a área do jogo
    """
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


# Função encarregada de escrever o score na tela do jogo, calculando sua posição e número
def draw_score():
    """
    Função para escrever o score e a quantidade de blocos

    A função irá calcular a posição do canto inferior esquerdo da tela para escrever o score e irá também calcular o canto inferior direito para escrever a
    quantidade de blocos colocados
    """
    score_msg = f"Score: {score}"
    block_score = f"Blocos colocados: {placed_blocks}"

    score_w, score_h = font_score.size(score_msg)
    block_score_w, block_score_h = font_score.size(block_score)

    pos = [
        screen_size[0] * 0.01,
        (screen_size[1] * (game_percentage + (1 - game_percentage) / 2))
        - (score_h / 2),
    ]
    pos_block_score = [
        screen_size[0] - block_score_w - screen_size[0] * 0.01,
        (screen_size[1] * (game_percentage + (1 - game_percentage) / 2))
        - (block_score_h / 2),
    ]

    write_score(score_msg, pos, score_color)
    write_score(block_score, pos_block_score, score_color)

    line([0, dis_height], [dis_width, dis_height], (255, 255, 255))
    return


# Função que tranformará a matriz numerica do jogo em uma matriz de caracteres usada para a tela do jogo
def turn_m():
    """
    Função que transformará o jogo em caracteres

    A função pegará a matriz do jogo e transformará seus números em caracteres relevantes, que representarão os objetos

    Returns: A função retornará a matriz de caracteres com os objetos
    """
    game2 = np.char.mod("%s", game)

    for i in range(block_limit):
        game2 = np.char.replace(game2, "-2", "#")
    game2 = np.char.replace(game2, "2", "O")
    game2 = np.char.replace(game2, "0", " ")
    game2 = np.char.replace(game2, "-1", "©")
    game2 = np.char.replace(game2, "1", "o")
    return game2


# Função que atualiza a tela
def update_screen():
    """
    Função que atualiza a tela

    A função desenhará a matriz, o score (normal e blocos) e desenhará os objetos na tela, representando o jogo de forma visual
    """
    matrix()
    draw_score()

    gameDis = turn_m()
    for i in range(row):
        for j in range(col):
            msg = "%s" % gameDis[i][j]
            msg = msg[:-2]
            text_w, text_h = font_game.size(msg)

            cor = find_cor(game[i][j])

            pos = [
                (square_w * j) + (square_w / 2) - (text_w / 2),
                (square_h * i) + (square_h / 2) - (text_h / 2),
            ]
            write_game(msg, pos, cor)
    pg.display.update()
    return


# Função encarregada da tela de game over
def game_over():
    """
    Função encarregada da tela de game over

    A função desenhará a tela de game over, incluindo a escrita e verificará se os jogadores gostariam de reiniciar o jogo ou fecha-lo
    """
    print("Game Over!")

    reset_msg = "Aperte ESC para sair do jogo ou R para reiniciar o jogo!"
    reset_text_w, reset_text_h = font_reset.size(reset_msg)

    reset_square_pos = (
        (screen_size[0] / 2) - (reset_text_w / 2) - (screen_size[0] * 0.02),
        (screen_size[1] / 2) - (reset_text_h / 2) - (screen_size[1] * 0.02),
        reset_text_w + (screen_size[0] * 0.04),
        reset_text_h + (screen_size[1] * 0.04),
    )

    pg.draw.rect(dis, reset_background_color, (0, 0, screen_size[0], screen_size[1]))
    pg.draw.rect(dis, reset_square_background_color, reset_square_pos)

    reset_text_pos = [
        (screen_size[0] / 2) - (reset_text_w / 2),
        (screen_size[1] / 2) - (reset_text_h / 2),
    ]
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


# Função que remove os blocos no entrono da maçã
def remove_around_apple(row, column):
    """
    Função que remove os blocos no entrono da maçã

    A função irá pegar as coordenadas passadas e irá remover todos os bloco no entorno da maçã recentemente criada

    Vars:
        row: Linha que a maçã será criada (spawnada)
        column: Coluna que a maçã será criada (spawnada)
    """
    for y in range(-block_apple_radius, block_apple_radius + 1):
        for x in range(-block_apple_radius, block_apple_radius + 1):
            try:
                if game[row + x][column + y] == -2:
                    game[row + x][column + y] = 0
            except:
                continue
    return


# Função de criação da maçã
def create_apple():
    """
    Função de criação da maçã

    A função irá gerar uma nova linha e coluna para a criação da maçã, checando se o novo local está disponível ou não para ser spawnada a maçã
    """
    rdr = rd.randint(0, row - 1)
    rdc = rd.randint(0, col - 1)
    while game[rdr][rdc] != 0:
        rdr = rd.randint(0, row - 1)
        rdc = rd.randint(0, col - 1)
    remove_around_apple(rdr, rdc)

    global apple_position
    apple_position = [rdr, rdc]

    game[rdr][rdc] = -1
    return


# Função para aumentar a cauda
def elong_tail():
    """
    Função para aumentar a cauda

    A função irá pegar a lista de posições da cauda e a expanderá para ter mais um item
    """
    tail.append(tail[-1])
    return


# Função encarregada de atualizar a posição da cauda
def update_tail(head):
    """
    Função encarregada de atualizar a posição da cauda

    A função irá pegar a lista das posições da cauda e irá atualizar-la para seguir a nova posição da cabeça da cobra

    Vars:
        head: A nova posição da cabeça
    """
    aux = tail.pop()
    game[aux[0]][aux[1]] = 0
    tail.insert(0, head)
    for i in tail:
        game[i[0]][i[1]] = 1
    return


# Função que atualizará a cabeça
def update_dir(dir):
    """
    Função que atualizará a cabeça

    A função pegará a direção para qual a cabeça esta se movendo e a moverá para aquela posição, verificando se o novo local será uma mação, parte da cauda ou um bloco,
    caso seja, ela ativará função game over

    Vars:
        dir: Direção para qual a cobra esta se movendo
    """
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


# Função que verifica a posição do novo bloco para a maçã
def check_if_apple(box_row, box_column):
    """
    Função que verifica a posição do novo bloco para a maçã

    A função irá verificar se o local selecionado pelo jogador do mouse é uma maçã ou se esta em um raio ao redor desta

    Vars:
        box_row: Linha do novo local de spawn do bloco
        box_column: Coluna do novo local de spawn do bloco
    """
    x_apple = apple_position[0]
    y_apple = apple_position[1]

    for y in range(-block_apple_radius, block_apple_radius + 1):
        for x in range(-block_apple_radius, block_apple_radius + 1):
            try:
                if x_apple + x == box_row and y_apple + y == box_column:
                    return True
            except:
                continue


# Função que verifica a posição do novo bloco para a cabeça
def check_if_head(box_row, box_column):
    """
    Função que verifica a posição do novo bloco para a cabeça da cobra

    A função irá verificar se o local selecionado pelo jogador do mouse é a cabeça da cobra ou se esta em um raio ao redor desta

    Vars:
        box_row: Linha do novo local de spawn do bloco
        box_column: Coluna do novo local de spawn do bloco
    """
    x_head = head[0]
    y_head = head[1]

    for y in range(-block_head_radius, block_head_radius + 1):
        for x in range(-block_head_radius, block_head_radius + 1):
            try:
                if x_head + x == box_row and y_head + y == box_column:
                    return True
            except:
                continue


# Função para criação de um novo bloco
def create_block(pos):
    """
    Função para criação de um novo bloco

    A função irá pegar o local selecionado pelo jogador para colocar um novo bloco, verificando se este é permitido pelas regras do jogo (raio da maçã e da cabeça)

    Vars:
        pos: Posição para posicionar o novo bloco
    """
    x = pos[0]
    y = pos[1]

    if x > dis_width or y > dis_height:
        return
    box_row = int(y / square_h)
    box_column = int(x / square_w)

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


# Função para reiniciar o jogo
def reset_game():
    """
    Função para reiniciar o jogo

    A função irá reiniciar todos as variáveis necessárias para seu valor padrão, reiniciando o jogo para seu estado inicial
    """
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
    return


# Função principal do jogo
def main_game():
    """
    Função principal do jogo

    A função é responsável por rodar o jogo e tudo necessário, sendo encarregada de detectar todos os inputs e causar os outputs
    """
    global clock, dir, game, tail, head

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
                    print("Game closed!")
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
                print("Throwaway!")
        head = update_dir(dir)
        update_screen()

        if IA:
            clock = 1 / (len(tail) + 1)
        t.sleep(clock)


# Chamada da função principal do jogo
main_game()
