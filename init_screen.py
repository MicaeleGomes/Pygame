import pygame
import random
from os import path

from config import IMG_DIR, BLACK, FPS, GAME, QUIT
from assets import load_assets  # Importando a função load_assets

def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega os assets
    assets = load_assets()  # Carrega os recursos do jogo

    # Acessa a imagem de fundo carregada a partir dos assets
    background = assets['background']
    background_rect = background.get_rect()

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

        # Depois de desenhar tudo, inverte o display
        pygame.display.flip()

    return state