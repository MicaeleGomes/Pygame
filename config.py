from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Dados gerais do jogo.
WIDTH = 1000  # Largura da tela
HEIGHT = 750  # Altura da tela
FPS = 30 # Frames por segundo

# Configurações do placar
SCORE_BOX_WIDTH = 250  # Largura da caixinha
SCORE_BOX_HEIGHT = 40  # Altura da caixinha
SCORE_POSITION = (20, 20)  # Posição da caixinha
SCORE_COLOR = (255, 255, 255)  # Cor do texto
SCORE_BG_COLOR = (118, 39, 139)  # Cor de fundo da caixinha

# Define tamanhos
ALIEN_WIDTH = 100
ALIEN_HEIGHT = 76
SHIP_WIDTH = 110  
SHIP_HEIGHT = 90 
largura_meteoro = 50
altura_meteoro = 38

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Estados para controle do fluxo da aplicação
INIT = 0
GAME = 1
QUIT = 2