# import pygame
# import random
# from os import path
# import os

# from config import IMG_DIR, BLACK, FPS, GAME, QUIT, WIDTH, HEIGHT
# from assets import load_assets  # Importando a função load_assets

# def init_screen(screen):
#     # Variável para o ajuste de velocidade
#     clock = pygame.time.Clock()
#     cor_fonte = 255, 255, 255

#     # Carrega os assets
#     assets = load_assets()  # Carrega os recursos do jogo

#     # Acessa a imagem de fundo carregada a partir dos assets
#     background = assets['background']
#     background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Ajusta o fundo ao tamanho da tela
#     background_rect = background.get_rect()

#     font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
#     font = pygame.font.Font(font_path, 50)  # Tamanho da fonte

#     texto_inicial = "Aperte qualquer tecla para inciar." 
#     texto_renderizado = font.render(texto_inicial, True, cor_fonte)

#     running = True
#     while running:

#         # Ajusta a velocidade do jogo
#         clock.tick(FPS)

#         # Processa os eventos (mouse, teclado, botão, etc)
#         for event in pygame.event.get():
#             # Verifica se foi fechado
#             if event.type == pygame.QUIT:
#                 state = QUIT
#                 running = False

#             if event.type == pygame.KEYUP:
#                 state = GAME
#                 running = False

#         # A cada loop, redesenha o fundo e os sprites
#         screen.fill(BLACK)
#         screen.blit(background, background_rect)
#         screen.blit(texto_renderizado, (100, 100))

#         # Depois de desenhar tudo, inverte o display
#         pygame.display.flip()

#     return state



import pygame
import random
from os import path
import os
import textwrap  # Para quebrar a linha do texto

from config import IMG_DIR, BLACK, FPS, GAME, QUIT, WIDTH, HEIGHT
from assets import load_assets  # Importando a função load_assets
from config import ALIEN_WIDTH, ALIEN_HEIGHT, largura_meteoro, altura_meteoro, SHIP_WIDTH, SHIP_HEIGHT, IMG_DIR, SND_DIR, FNT_DIR


def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    cor_fonte = 255, 255, 255

    # Carrega os assets
    assets = load_assets()  # Carrega os recursos do jogo

    # Acessa a imagem de fundo carregada a partir dos assets
    background = assets['background']
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Ajusta o fundo ao tamanho da tela
    background_rect = background.get_rect()

    font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
    font = pygame.font.Font(font_path, 30)  # Fonte para a mensagem
    font_butbigger = pygame.font.Font(font_path, 50)  # Fonte para o título 

    titulo = "Ameaça Interestelar"
    texto_inicial = "Aperte qualquer tecla para iniciar."

    # Carregar a imagem que ficará ao lado de "Ameaça"
    img_alien = assets['alien_img'] = pygame.image.load(os.path.join(IMG_DIR, 'alien.png')).convert_alpha()
    img_alien = assets['alien_img'] = pygame.transform.scale(assets['alien_img'], (ALIEN_WIDTH, ALIEN_HEIGHT))

    # Quebra o título "Ameaça Interestelar" em duas palavras com textwrap
    titulo_linhas = ["Ameaça", "Interestelar"]

    # Quebra o texto automaticamente em várias linhas com base na largura da tela
    linhas = textwrap.wrap(texto_inicial, width=30)  # 30 é o número máximo de caracteres por linha

    # Calculando a altura total do texto da mensagem de teclas
    altura_total_linhas = len(linhas) * font.get_height()
    altura_titulo = sum([font_butbigger.get_height() for _ in titulo_linhas])  # Altura do título dividido em duas linhas

    # Calculando a posição vertical inicial para centralizar o título um pouco acima do meio
    y_titulo = (HEIGHT // 2) - altura_titulo - 50 

    # Calculando a posição inicial para a mensagem de teclas 
    y_inicial = (HEIGHT + altura_titulo) // 2 + 50  

    # Inicializando a posição Y para a primeira linha do texto da mensagem
    y_atual = y_inicial

    running = True
    while running:
        # Ajusta a velocidade do jogo
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc)
        for event in pygame.event.get():
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                state = GAME
                running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Desenha a imagem ao lado da palavra "Ameaça"
        x_imagem_ameaca = (WIDTH // 2) - (font_butbigger.size("Ameaça")[0] // 2) + font_butbigger.size("Ameaça")[0] + 20  # 20px à direita de "Ameaça"
        y_imagem_ameaca = y_titulo - 12  # Move a imagem 12px para cima

        # Desenha a imagem na tela
        screen.blit(img_alien, (x_imagem_ameaca, y_imagem_ameaca))

        # Desenha o título em duas linhas (
        y_atual_titulo = y_titulo
        for linha in titulo_linhas:
            titulo_renderizado = font_butbigger.render(linha, True, cor_fonte)
            texto_pos_x = (WIDTH - titulo_renderizado.get_width()) // 2
            screen.blit(titulo_renderizado, (texto_pos_x, y_atual_titulo))
            y_atual_titulo += font_butbigger.get_height()  # Move para a próxima linha do título

        # Desenha cada linha da mensagem de teclas com a fonte menor
        y_atual = y_inicial  # Reseta a posição Y para o início a cada frame
        for linha in linhas:
            texto_renderizado = font.render(linha, True, cor_fonte)
            # Centraliza cada linha horizontalmente
            texto_pos_x = (WIDTH - texto_renderizado.get_width()) // 2
            screen.blit(texto_renderizado, (texto_pos_x, y_atual))
            y_atual += font.get_height()  # Move para a próxima linha

        # Depois de desenhar tudo, inverte o display
        pygame.display.flip()

    return state
