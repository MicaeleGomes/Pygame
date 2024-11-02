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
alien_img = pygame.transform.scale(alien_img, (ALIEN_WIDTH, ALIEN_HEIGHT))

# ----- Inicia estruturas de dados
class Alien(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-ALIEN_WIDTH)
        self.rect.y = random.randint(-100, -ALIEN_HEIGHT)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        # Atualizando a posição do alien
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-ALIEN_WIDTH)
            self.rect.y = random.randint(-100, -ALIEN_HEIGHT)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)

game = True

clock = pygame.time.Clock()
FPS = 30

# Criando um grupo de meteoros
all_aliens = pygame.sprite.Group()
# Criando os aliens
for i in range(4):
    meteor = Alien(alien_img)
    all_aliens.add(meteor)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    # Atualizando a posição do alien
    all_aliens.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(background, (0, 0))

    # Desenhando meteoros
    all_aliens.draw(window)

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

