import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ameaça Interestelar')

# ----- Inicia assets
ALIEN_WIDTH = 100
ALIEN_HEIGHT = 76
font = pygame.font.SysFont(None, 48)
background = pygame.image.load('imagens/SpaceBackGround.jpg').convert()
alien_img = pygame.image.load('imagens/alien.png').convert_alpha()
alien_img_small = pygame.transform.scale(alien_img, (ALIEN_WIDTH, ALIEN_HEIGHT))

# ----- Inicia estruturas de dados
game = True
alien_x = random.randint(0, WIDTH-ALIEN_WIDTH)
# y negativo significa que está acima do topo da janela. O alien começa fora da janela
alien_y = -random.randint(-100, -ALIEN_HEIGHT)
alien_speedx = random.randint(-3, 3)
alien_speedy = random.randint(2, 9)
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 30

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    # Atualizando a posição do alienígena
    alien_x += alien_speedx
    alien_y += alien_speedy
    # Se o alienígena passar do final da tela, volta para cima
    if alien_y > HEIGHT or alien_x + ALIEN_WIDTH < 0 or alien_x > WIDTH:
        alien_x = random.randint(0, WIDTH-ALIEN_WIDTH)
        alien_y = -random.randint(-100, -ALIEN_HEIGHT)

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(background, (0, 0))
    window.blit(alien_img_small, (alien_x, alien_y))
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

