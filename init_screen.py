import pygame
from os import path
import os
import textwrap  

from config import IMG_DIR, BLACK, FPS, GAME, QUIT, WIDTH, HEIGHT
from assets import load_assets  
from config import ALIEN_WIDTH, ALIEN_HEIGHT, largura_meteoro, altura_meteoro, SHIP_WIDTH, SHIP_HEIGHT, IMG_DIR, SND_DIR, FNT_DIR


def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    cor_fonte = 255, 255, 255

    # Carrega os assets
    assets = load_assets() 

    # Acessa a imagem de fundo 
    background = assets['background']
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Ajusta o fundo ao tamanho da tela
    background_rect = background.get_rect()

    font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
    font = pygame.font.Font(font_path, 20)  # Fonte para a mensagem
    font_butbigger = pygame.font.Font(font_path, 50)  # Fonte para o título 

    titulo = "Ameaça Interestelar"
    texto_inicial = "Aperte qualquer tecla para iniciar!"

    # Carrega a logo principal e redimensiona 
    logo_principal = assets['logo_principal']
    logo_width, logo_height = logo_principal.get_size()
    scale_factor = 0.35 

    # Redimensiona o logo com o fator de escala
    new_width = int(logo_width * scale_factor)
    new_height = int(logo_height * scale_factor)
    logo_principal = pygame.transform.scale(logo_principal, (new_width, new_height))

    # Calcula a altura total dos elementos para centralização
    logo_rect = logo_principal.get_rect()
    titulo_height = font_butbigger.get_height() * 2  
    mensagem_height = font.get_height() * len(textwrap.wrap(texto_inicial, width=30))
    altura_total = new_height + titulo_height + mensagem_height + 60 

    # Centraliza os elementos verticalmente
    y_inicial = (HEIGHT - altura_total) // 2
    logo_rect.centerx = WIDTH // 2
    logo_rect.top = y_inicial

    # Posiciona o título logo abaixo do logo
    y_titulo = logo_rect.bottom + 30

    # Posiciona a mensagem abaixo do título
    y_mensagem = y_titulo + titulo_height + 40

    # Quebra o título "Ameaça Interestelar" em duas palavras
    titulo_linhas = ["Ameaça", "Interestelar"]

    # Dentro do loop principal
    running = True
    while running:
        # Ajusta a velocidade do jogo
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                state = GAME
                running = False

        # Redesenha o fundo e os elementos
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Desenha a logo principal
        screen.blit(logo_principal, logo_rect.topleft)

        # Desenha o título em duas linhas
        y_atual_titulo = y_titulo
        for linha in titulo_linhas:
            titulo_renderizado = font_butbigger.render(linha, True, cor_fonte)
            texto_pos_x = (WIDTH - titulo_renderizado.get_width()) // 2
            screen.blit(titulo_renderizado, (texto_pos_x, y_atual_titulo))
            y_atual_titulo += font_butbigger.get_height()

        # Desenha cada linha da mensagem de teclas com a fonte menor
        y_atual = y_mensagem
        for linha in textwrap.wrap(texto_inicial, width=20):
            texto_renderizado = font.render(linha, True, cor_fonte)
            texto_pos_x = (WIDTH - texto_renderizado.get_width()) // 2
            screen.blit(texto_renderizado, (texto_pos_x, y_atual))
            y_atual += font.get_height()

        # Depois de desenhar tudo, inverte o display
        pygame.display.flip()

    return state
