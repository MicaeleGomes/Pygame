# ----- Importa e inicia pacotes
import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 850
HEIGHT = 750
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ameaça Interestelar')

# ----- Inicia assets
ALIEN_WIDTH = 100
ALIEN_HEIGHT = 76
SHIP_WIDTH = 110  
SHIP_HEIGHT = 90  
font = pygame.font.SysFont(None, 48)

#Adiciona fundo.
background = pygame.image.load('imagens/SpaceBackGround.jpg').convert()
#Adiciona imagem do Alien (invasor).
alien_img = pygame.image.load('imagens/alien.png').convert_alpha()
alien_img = pygame.transform.scale(alien_img, (ALIEN_WIDTH, ALIEN_HEIGHT))
#Adiciona imagem da nave (jogador)
ship_img = pygame.image.load('imagens/ship.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (SHIP_WIDTH, SHIP_HEIGHT))

# ----- Inicia estruturas de dados
# Definindo os novos tipos de classes.
class Ship(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx

        # Mantem a nave dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

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
        # Se o alien passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-ALIEN_WIDTH)
            self.rect.y = random.randint(-100, -ALIEN_HEIGHT)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)

game = True

clock = pygame.time.Clock()
FPS = 30

# Criando um grupo de aliens
all_sprites = pygame.sprite.Group()

# Criando o jogador
player = Ship(ship_img)
all_sprites.add(player)

# Criando os aliens
for i in range(4):
    alien = Alien(alien_img)
    all_sprites.add(alien)

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
    all_sprites.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(background, (0, 0))

    # Desenhando aliens
    all_sprites.draw(window)

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

