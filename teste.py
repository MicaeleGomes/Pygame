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
        state = game_screen(window)
    else:
        # Quando o estado for QUIT, a execução do jogo termina
        state = QUIT

# Chama a função game_screen e captura o score final, apenas após a tela de jogo
final_score = game_screen(window)

# Exibe a tela final com a pontuação
tela_final.exibir_tela_final(final_score)

# Finaliza o Pygame
pygame.quit()
