# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT
from game_screen import game_screen


pygame.init()
pygame.mixer.init()


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ameaça Interestelar')

# Chama a função game_screen e captura o score final
final_score = game_screen(window)
import tela_final
tela_final.exibir_tela_final(final_score)  

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
