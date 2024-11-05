# ----- Importa e inicia pacotes
import pygame
import random

pygame.init()
pygame.mixer.init()

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
largura_meteoro = 50
altura_meteoro = 38
font = pygame.font.SysFont(None, 48)

assets = {}
#-------------Adiciona imagem de fundo.
assets['background'] = pygame.image.load('imagens/SpaceBackGround.jpg').convert()
#-------------Adiciona imagem do Alien (invasor)
assets['alien_img'] = pygame.image.load('imagens/alien.png').convert_alpha()
assets['alien_img'] = pygame.transform.scale(assets['alien_img'], (ALIEN_WIDTH, ALIEN_HEIGHT))
#--------------Adiciona imagem da nave (jogador)
assets['ship_img'] = pygame.image.load('imagens/ship.png').convert_alpha()
assets['ship_img'] = pygame.transform.scale(assets['ship_img'], (SHIP_WIDTH, SHIP_HEIGHT))
#--------------Adiciona imagem do tiro
assets['bullet_img'] = pygame.image.load('imagens/laser.png').convert_alpha()

#--------Imagem do meteoro + escala do meteoro
meteoro = pygame.image.load('imagens/astroid.png').convert_alpha()
meteoro = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))
meteoro_pequeno = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))

#---------------Adiciona imagems de explosão ao tiro colidir com o Alien
explosion_anim = []
for i in range(9):
    # Os arquivos de animação são numerados de 00 a 08
    filename = f'imagens/regularExplosion{str(i).zfill(2)}.png'
    img = pygame.image.load(filename).convert()
    img = pygame.transform.scale(img, (80, 80))
    explosion_anim.append(img)
assets["explosion_anim"] = explosion_anim


# Carrega os sons do jogo
pygame.mixer.music.load('snd/somprincipal.ogg')
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound('snd/expl3.wav')
destroy_sound = pygame.mixer.Sound('snd/expl6.wav')
colisao = pygame.mixer.Sound('snd/crash.ogg')
assets['pew_sound'] = pygame.mixer.Sound('snd/pew.wav')

class Meteor(pygame.sprite.Sprite):
    def __init__(self, img): 
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-largura_meteoro)
        self.rect.y = random.randint(-100, -altura_meteoro)
        self.speedx = random.randint(-4, -2)
        self.speedy = random.randint(-2, 3)

    def update(self): #--------Atualiza a posição do meteoro.

        self.rect.x += self.speedx
        self.rect.y += self.speedy
       
       #--------Redefine a posição se o meteoro sair da tela
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-largura_meteoro)
            self.rect.y = random.randint(-100, -altura_meteoro)
            self.speedx = random.randint(-3, 4)
            self.speedy = random.randint(6, 9)

# ----- Inicia estruturas de dados
#Definindo os novos tipos de classes.
class Ship(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['ship_img']
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.groups = groups
        self.assets = assets

    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx

        # Mantem a nave dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # A nova bala vai ser criada logo acima e no centro horizontal da nave
        new_bullet = Bullet(self.assets, self.rect.top, self.rect.centerx)
        self.groups['all_sprites'].add(new_bullet)
        self.groups['all_bullets'].add(new_bullet)
        self.assets['pew_sound'].play()

class Alien(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['alien_img']
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
            self.speedx = random.randint(-3, 4)
            self.speedy = random.randint(2, 9)

# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['bullet_img']
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedy = -10  # Velocidade fixa para cima

    def update(self):
        # A bala só se move no eixo y
        self.rect.y += self.speedy

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()

# Classe que representa uma explosão de alien
class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = assets['explosion_anim']

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.explosion_anim[self.frame]  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.center = center  # Posiciona o centro da imagem

        # Guarda o tick da primeira imagem, ou seja, o momento em que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        # Quando pygame.time.get_ticks() - self.last_update > self.frame_ticks a
        # próxima imagem da animação será mostrada
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

game = True

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 30

# Criando um grupo de aliens e tiros
all_sprites = pygame.sprite.Group()
all_aliens = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
groups = {}
groups['all_sprites'] = all_sprites
groups['all_aliens'] = all_aliens
groups['all_bullets'] = all_bullets

meteoros = pygame.sprite.Group() #--------Cria um grupo de meteoros e adiciona múltiplos meteoros ao grupo


# Criando o jogador
player = Ship(groups, assets)
all_sprites.add(player)

# Criando os aliens
for i in range(4):
    alien = Alien(assets)
    all_sprites.add(alien)
    all_aliens.add(alien)

#--------Define a quantidade de meteoros.
for _ in range(3):  
    meteor = Meteor(meteoro)
    meteoros.add(meteor)


# ===== Loop principal =====
pygame.mixer.music.play(loops=-1)
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False
        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx -= 9
            if event.key == pygame.K_RIGHT:
                player.speedx += 9
            if event.key == pygame.K_SPACE:
                player.shoot()
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx += 9
            if event.key == pygame.K_RIGHT:
                player.speedx -= 9

    colisao_meteoros = pygame.sprite.spritecollide(player, meteoros, True)
    if colisao_meteoros:
        colisao.play()  # Toca o som de colisão
        pass  # Aqui você pode adicionar outras ações em caso de colisão, se necessário


    # ----- Atualiza estado do jogo
    # Atualizando a posição dos aliens
    all_sprites.update()
    #------ Atualiza a posição de todos os meteoros
    meteoros.update() 


     # Verifica se houve colisão entre tiro e o alien 
    hits = pygame.sprite.groupcollide(all_aliens, all_bullets, True, True)
    for alien in hits: # As chaves são os elementos do primeiro grupo (aliens) que colidiram com alguma bala
        # O alien e destruido e precisa ser recriado
        #----------------------COLOCA SOM------------------
        # assets['destroy_sound'].play()
        #----------------------COLOCA SOM-------------------
        a = Alien(assets)
        all_sprites.add(a)
        all_aliens.add(a)

        # No lugar do alien antigo, adicionar uma explosão.
        explosao_alien = Explosion(alien.rect.center, assets)
        all_sprites.add(explosao_alien)

    # ----- Gera saídas
    window.fill((0, 0, 0))
    window.blit(assets['background'], (0, 0))

    #-------------Desenhando aliens
    all_sprites.draw(window)
    #-------------Desenha todos os meteoros no grupo
    meteoros.draw(window) 

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

