import pygame
from config import WIDTH, HEIGHT, INIT, QUIT, GAME
from game_screen import game_screen
from init_screen import init_screen
from tela_final import exibir_tela_final  # Importando a tela final

pygame.init()
pygame.mixer.init()

# Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ameaça Interestelar')

state = INIT

while state != QUIT:
    if state == INIT:
        # Tela inicial
        state = init_screen(window)
    elif state == GAME:
        # Tela de jogo
        score = game_screen(window)
        state = exibir_tela_final(window, score)  # Chama a tela final com o score
    else:
        state = QUIT  # Sai do jogo

pygame.quit()

