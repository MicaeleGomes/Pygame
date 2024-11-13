import pygame
from config import WIDTH, HEIGHT, INIT, QUIT, GAME
from game_screen import game_screen
from init_screen import init_screen
import tela_final  # Importando a tela final

pygame.init()
pygame.mixer.init()

# Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ameaça Interestelar')

state = INIT

while state != QUIT:
    if state == INIT:
        # Tela inicial chamada uma vez
        state = init_screen(window)
    elif state == GAME:
        # Tela de jogo
        score = game_screen(window)  # Captura o score ao final do jogo
        state = QUIT  # Finaliza o estado do jogo, pois o jogo terminou
    else:
        # Quando o estado for QUIT, a execução do jogo termina
        state = QUIT

# Exibe a tela final com o score
tela_final.exibir_tela_final(score)  # Exibe a tela final com a pontuação

# Finaliza o Pygame
pygame.quit()