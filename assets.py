import pygame
import os
from config import ALIEN_WIDTH, ALIEN_HEIGHT, largura_meteoro, altura_meteoro, SHIP_WIDTH, SHIP_HEIGHT, IMG_DIR, SND_DIR, FNT_DIR


BACKGROUND = 'background'
ALIEN_IMG = 'alien_img'
SHIP_IMG = 'ship_img'
BULLET_IMG = 'bullet_img'
METEOR_IMG = 'meteor_img'
EXPLOSION_ANIM = 'explosion_anim'
SCORE_FONT = 'score_font'
BOOM_SOUND = 'boom_sound'
DESTROY_SOUND = 'destroy_sound'
COLISAO_SOUND = 'colisao_sound'
PEW_SOUND = 'pew_sound'

TIMER_ICON_IMG = 'timer_icon'
ALIEN_ICON_IMG = 'alien_icon'


def load_assets():
    assets = {}

    # Carrega as imagens e configura tamanhos
    assets[BACKGROUND] = pygame.image.load(os.path.join(IMG_DIR, 'SpaceBackGround.jpg')).convert()
    assets[ALIEN_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'alien.png')).convert_alpha()
    assets[ALIEN_IMG] = pygame.transform.scale(assets[ALIEN_IMG], (ALIEN_WIDTH, ALIEN_HEIGHT))
    assets[SHIP_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'ship.png')).convert_alpha()
    assets[SHIP_IMG] = pygame.transform.scale(assets[SHIP_IMG], (SHIP_WIDTH, SHIP_HEIGHT))
    assets[BULLET_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'laser.png')).convert_alpha()
    assets[METEOR_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'astroid.png')).convert_alpha()
    assets[METEOR_IMG] = pygame.transform.scale(assets[METEOR_IMG], (largura_meteoro, altura_meteoro))

    # Ícones do temporizador e do alien para o placar
    assets[TIMER_ICON_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'timer_pygame.png')).convert_alpha()
    assets[TIMER_ICON_IMG] = pygame.transform.scale(assets[TIMER_ICON_IMG], (30, 30))
    assets[ALIEN_ICON_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'alien.png')).convert_alpha()
    assets[ALIEN_ICON_IMG] = pygame.transform.scale(assets[ALIEN_ICON_IMG], (30, 30))

    #Adiciona imagems de explosão ao tiro colidir com o Alien
    explosion_anim = []
    for i in range(9):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join(IMG_DIR, 'regularExplosion{:02}.png'.format(i))
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (80, 80))
        explosion_anim.append(img)

    assets[EXPLOSION_ANIM] = explosion_anim
    assets[SCORE_FONT] = pygame.font.Font(os.path.join(FNT_DIR, 'PressStart2P.ttf'), 28)

    #Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SND_DIR, 'somprincipal.ogg'))
    pygame.mixer.music.set_volume(0.4)
    assets[BOOM_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'expl3.wav'))
    assets[DESTROY_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'expl6.wav'))
    assets[COLISAO_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'crash.ogg'))
    assets[PEW_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'pew.wav'))

    return assets