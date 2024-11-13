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

#--------------- Placar
#---------------- Configurações do placar
SCORE_BOX_WIDTH = 250  # Largura da caixinha
SCORE_BOX_HEIGHT = 40  # Altura da caixinha
SCORE_POSITION = (20, 20)  # Posição da caixinha
SCORE_COLOR = (255, 255, 255)  # Cor do texto
SCORE_BG_COLOR = (100, 100, 200)  # Cor de fundo da caixinha

# ----- Inicia assets
FPS = 30
ALIEN_WIDTH = 100
ALIEN_HEIGHT = 76
SHIP_WIDTH = 110  
SHIP_HEIGHT = 90 
largura_meteoro = 50
altura_meteoro = 38
font = pygame.font.SysFont(None, 48)

def load_assets():
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
    assets['meteor_img'] = pygame.image.load('imagens/astroid.png').convert_alpha()
    assets['meteor_img'] = pygame.transform.scale(assets['meteor_img'], (largura_meteoro, altura_meteoro))

    # Carrega a imagem do cronômetro para o temporizador
    assets['timer_icon'] = pygame.image.load('imagens/timer_pygame.png').convert_alpha()
    assets['timer_icon'] = pygame.transform.scale(assets['timer_icon'], (30, 30))

    # Carrega e redimensiona a imagem do alien para o placar
    assets['alien_icon'] = pygame.transform.scale(assets['alien_img'], (30, 30))

    #---------------Adiciona imagems de explosão ao tiro colidir com o Alien
    explosion_anim = []
    for i in range(9):
        # Os arquivos de animação são numerados de 00 a 08
        filename = f'imagens/regularExplosion{str(i).zfill(2)}.png'
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (80, 80))
        explosion_anim.append(img)
    assets["explosion_anim"] = explosion_anim
    assets["score_font"] = pygame.font.Font('Fontes/PressStart2P.ttf', 28)

    #------------------ Carrega os sons do jogo
    pygame.mixer.music.load('snd/somprincipal.ogg')
    pygame.mixer.music.set_volume(0.4)
    # boom_sound = pygame.mixer.Sound('snd/expl3.wav')
    assets['boom_sound'] = pygame.mixer.Sound('snd/expl3.wav')
    assets['destroy_sound'] = pygame.mixer.Sound('snd/expl6.wav')
    # colisao = pygame.mixer.Sound('snd/crash.ogg')
    assets['colisao_sound'] = pygame.mixer.Sound('snd/crash.ogg')
    assets['pew_sound'] = pygame.mixer.Sound('snd/pew.wav')
    assets['boom_sound'] = pygame.mixer.Sound('snd/expl3.wav')

    return assets

#---------------- Fonte para o score
score_font = pygame.font.Font('Fontes/PressStart2P.ttf', 24)

#--------Carrega a fonte do jogo------------
font_path = 'Fontes/PressStart2P-Regular.ttf'  # Caminho do arquivo da fonte
font = pygame.font.Font(font_path, 50)  # Tamanho da fonte (50 aqui)
cor_fonte = (255, 255, 255)
oops = "Oops..."
oops_renderizado = font.render(oops, True, cor_fonte)

pos_x = (WIDTH - oops_renderizado.get_width()) // 2  
pos_y = (HEIGHT // 2) - 100  


class Meteor(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['meteor_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-largura_meteoro)
        self.rect.y = random.randint(-100, -altura_meteoro)
        self.speedx = random.randint(-2, 2) 
        self.speedy = random.randint(1, 4)

    def update(self): #--------Atualiza a posição do meteoro.
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    
    #--------Redefine a posição se o meteoro sair da tela
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-largura_meteoro)
            self.rect.y = random.randint(-100, -altura_meteoro)
            self.speedx = random.randint(-2, 2)
            self.speedy = random.randint(4, 7)

# ----- Inicia estruturas de dados
#Definindo os novos tipos de classes.
class Ship(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['ship_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.groups = groups
        self.assets = assets

        # Limitando os tiros da nave a um tiro a cada 500 milissegundos.
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500

    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx

        # Mantem a nave dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-ALIEN_WIDTH)
        self.rect.y = random.randint(-100, -ALIEN_HEIGHT)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        global score  # Declara `score` como global 
        # Atualizando a posição do alien
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            score -= 100
            
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
        self.mask = pygame.mask.from_surface(self.image)
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
        self.image = self.explosion_anim[self.frame]  
        self.rect = self.image.get_rect()
        self.rect.center = center 

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

def game_screen(window):
    global score  
    score = 0     

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando um grupo de aliens e tiros
    all_sprites = pygame.sprite.Group()
    all_aliens = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    all_meteors = pygame.sprite.Group()

    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_aliens'] = all_aliens
    groups['all_bullets'] = all_bullets
    groups['all_meteors'] = all_meteors

    # Criando o jogador
    player = Ship(groups, assets)
    all_sprites.add(player)

    # Criando os aliens
    for i in range(3):
        alien = Alien(assets)
        all_sprites.add(alien)
        all_aliens.add(alien)

    #--------Define a quantidade de meteoros.
    for _ in range(2):  
        # meteor = Meteor(meteoro)
        meteor = Meteor(assets)
        all_sprites.add(meteor)
        all_meteors.add(meteor)

    #---------Define estados da nave
    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}    

    # -------- Definindo temporizador
    GAME_DURATION = 60000  # Duração do jogo em milissegundos (60 segundos)
    start_time = pygame.time.get_ticks()  # Marca o tempo inicial do jogo

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    # while game:
    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                # game = False
                state = DONE
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 9
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 9
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 9
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 9

        # ----- Atualiza estado do jogo

        # Atualizando a posição dos aliens
        all_sprites.update()
        # Atualiza a posição de todos os meteoros
        all_meteors.update()

        if state == PLAYING:
            # Verifica se houve colisão entre tiro e o alien 
            hits = pygame.sprite.groupcollide(all_aliens, all_bullets, True, True, pygame.sprite.collide_mask)
            for alien in hits:
                # O alien é destruido e precisa ser recriado
                assets['destroy_sound'].play()
                a = Alien(assets)
                all_sprites.add(a)
                all_aliens.add(a)

                # No lugar do alien antigo, adicionar uma explosão.
                explosao_alien = Explosion(alien.rect.center, assets)
                all_sprites.add(explosao_alien)

                # Ganhou pontos!
                score += 100
            
            # Verifica se houve colisão entre tiros e meteoros
            bullet_hits_meteors = pygame.sprite.groupcollide(all_bullets, all_meteors, True, False)
            for bullet in bullet_hits_meteors:
                bullet.kill()  # Remove o tiro visualmente

            # Verifica se houve colisão entre meteoro e a nave
            colisao_meteoros = pygame.sprite.spritecollide(player, all_meteors, True, pygame.sprite.collide_mask)
            if len(colisao_meteoros) > 0:
                assets['boom_sound'].play()
                player.kill()
                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400
            
            #se o meteoro bater na nave, o jogador perde 200 pontos.
            if colisao_meteoros:
                score -= 200

            while len(all_meteors) < 2:  
                novo_meteoro = Meteor(assets)
                all_meteors.add(novo_meteoro)
                all_sprites.add(novo_meteoro)

        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                state = PLAYING
                player = Ship(groups, assets)
                all_sprites.add(player)

        # Calcula o tempo restante em segundos
        elapsed_time = pygame.time.get_ticks( ) - start_time
        remaining_time = max(0, (GAME_DURATION - elapsed_time) // 1000)  # Converte para segundos

        # Finaliza o jogo quando o tempo acaba
        if remaining_time <= 0:
            state = DONE
            with open("score.txt", "w") as file:
                file.write(str(score))

        # ----- Gera saídas
        window.fill((0, 0, 0))
        window.blit(assets['background'], (0, 0))

        #------------- Desenhando aliens e meteoros
        all_sprites.draw(window)
        all_meteors.draw(window) 

        # ------------ Desenha o placar com a imagem do alien ao lado do score
        pygame.draw.rect(window, SCORE_BG_COLOR, (*SCORE_POSITION, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), border_radius=10)

        alien_icon = assets['alien_icon']  # Carrega o ícone do alien
        alien_icon_position = (SCORE_POSITION[0] + 10, SCORE_POSITION[1] + (SCORE_BOX_HEIGHT - alien_icon.get_height()) // 2)
        window.blit(alien_icon, alien_icon_position)

        text_surface = assets['score_font'].render("{:07d}".format(score), True, SCORE_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (alien_icon_position[0] + 40, SCORE_POSITION[1] + (SCORE_BOX_HEIGHT - text_rect.height) // 2)
        window.blit(text_surface, text_rect)

        # Desenha a caixinha do temporizador
        TIMER_BOX_POSITION = (20, 70)  # Posição do temporizador (abaixo do placar)

        pygame.draw.rect(window, SCORE_BG_COLOR, (*TIMER_BOX_POSITION, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), border_radius=10)

        # Centralizando o ícone do cronômetro
        timer_icon = assets['timer_icon']  # Carrega o ícone do cronômetro de assets
        timer_icon_position = (TIMER_BOX_POSITION[0] + 10, TIMER_BOX_POSITION[1] + (SCORE_BOX_HEIGHT - timer_icon.get_height()) // 2)
        window.blit(timer_icon, timer_icon_position)

        time_surface = assets['score_font'].render("{:02d}".format(remaining_time), True, SCORE_COLOR)
        time_rect = time_surface.get_rect()
        time_rect.topleft = (timer_icon_position[0] + 40, TIMER_BOX_POSITION[1] + (SCORE_BOX_HEIGHT - time_rect.height) // 2)
        window.blit(time_surface, time_rect)

        pygame.display.update()  

    return score  # Retorna o score final antes de sair da função

# Chama a função game_screen e captura o score final
final_score = game_screen(window)
import tela_final
tela_final.exibir_tela_final(final_score)  

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
