# import pygame
# import sys
# import random
# import os
# from os import path
# from config import WIDTH, HEIGHT
# from assets import load_assets
# from game_screen import game_screen

# # Configurações de diretórios e cores
# IMG_DIR = 'assets/img'  # Diretório das imagens
# BLACK = (0, 0, 0)
# FPS = 60
# GAME = "game"
# QUIT = "quit"

# pygame.init()

# # Largura e altura da tela
# largura, altura = 800, 800

# # Definindo a largura e altura do meteoro
# largura_meteoro = 50
# altura_meteoro = 38

# # Tela do jogo
# janela = pygame.display.set_mode((largura, altura))
# pygame.display.set_caption('Ameaça Interestelar')

# # Fontes
# font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
# font = pygame.font.Font(font_path, 50)

# # Texto do botão Play
# texto_botao = "Play"
# cor_fonte = (255, 255, 255)

# texto_ameaca = "Ameaça"
# texto_interestelar = "Interestelar"

# texto_renderizado = font.render(texto_ameaca, True, cor_fonte)
# texto_renderizado2 = font.render(texto_interestelar, True, cor_fonte)
# botao_renderizado = font.render(texto_botao, True, cor_fonte)

# # Posicionamento do título
# pos_x = (largura - texto_renderizado.get_width()) // 2
# pos_y = (altura // 2) - 100

# pos_x2 = (largura - texto_renderizado2.get_width()) // 2
# pos_y2 = pos_y + texto_renderizado.get_height() + 10

# # Posicionamento do botão
# bt_x = (largura - botao_renderizado.get_width()) // 2
# bt_y = altura - 200

# # Definindo a área do botão
# area_botao = pygame.Rect(bt_x, bt_y, botao_renderizado.get_width(), botao_renderizado.get_height())

# # Música de fundo
# pygame.mixer.music.load(path.join('assets', "snd", '1_lift_off.flac'))
# pygame.mixer.music.set_volume(0.4)
# pygame.mixer.music.play(-1, 0.0)

# # Tela de fundo do jogo
# tela_de_fundo = pygame.image.load(path.join(IMG_DIR, "SpaceBackGround.jpg")).convert()

# # Carregar a imagem do meteoro
# meteoro_img = pygame.image.load(os.path.join(IMG_DIR, 'astroid.png')).convert_alpha()
# meteoro_img = pygame.transform.scale(meteoro_img, (largura_meteoro, altura_meteoro))

# # Classe do meteoro
# class Meteor(pygame.sprite.Sprite):
#     def _init_(self, img):
#         pygame.sprite.Sprite._init_(self)
#         self.image = img
#         self.rect = self.image.get_rect()
#         self.rect.x = random.randint(0, largura - largura_meteoro)
#         self.rect.y = random.randint(-100, -altura_meteoro)
#         self.speedx = random.randint(-4, -2)
#         self.speedy = random.randint(-2, 3)

#     def update(self):
#         self.rect.x += self.speedx
#         self.rect.y += self.speedy
#         if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
#             self.rect.x = random.randint(0, largura - largura_meteoro)
#             self.rect.y = random.randint(-100, -altura_meteoro)
#             self.speedx = random.randint(-3, 4)
#             self.speedy = random.randint(6, 9)

# # Função da tela inicial

# def init_screen(screen):
#     clock = pygame.time.Clock()
#     try:
#         background = pygame.image.load(path.join(IMG_DIR, 'inicio.png')).convert()
#         background_rect = background.get_rect()
#     except pygame.error as e:
#         print("Erro ao carregar a imagem de fundo da tela inicial:", e)
#         screen.fill(BLACK)
#         background = None
#         background_rect = None

#     running = True
#     while running:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return QUIT
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_x, mouse_y = event.pos
#                 if area_botao.collidepoint(mouse_x, mouse_y):
#                     return GAME
        
#         # Desenho da tela inicial
#         screen.fill(BLACK)
#         if background:
#             screen.blit(background, background_rect)
#         screen.blit(texto_renderizado, (pos_x, pos_y))
#         screen.blit(texto_renderizado2, (pos_x2, pos_y2))
#         screen.blit(botao_renderizado, (bt_x, bt_y))
#         pygame.display.flip()
        
#         return QUIT

# # def init_screen(screen):
# #     clock = pygame.time.Clock()
# #     background = pygame.image.load(path.join(IMG_DIR, 'inicio.png')).convert()
# #     background_rect = background.get_rect()

# #     running = True
# #     while running:
# #         clock.tick(FPS)
# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 return QUIT
# #             if event.type == pygame.MOUSEBUTTONDOWN:
# #                 mouse_x, mouse_y = event.pos
# #                 if area_botao.collidepoint(mouse_x, mouse_y):
# #                     return GAME  # Somente inicia o jogo se o botão "Play" for clicado
# #         screen.fill(BLACK)
# #         screen.blit(background, background_rect)
# #         screen.blit(texto_renderizado, (pos_x, pos_y))
# #         screen.blit(texto_renderizado2, (pos_x2, pos_y2))
# #         screen.blit(botao_renderizado, (bt_x, bt_y))
# #         pygame.display.flip()

# #     return QUIT

# # Loop principal do jogo
# def game_loop():
#     clock = pygame.time.Clock()
#     meteoros = pygame.sprite.Group()
#     for _ in range(3):
#         meteor = Meteor(meteoro_img)
#         meteoros.add(meteor)

#     running = True
#     while running:
#         clock.tick(FPS)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         meteoros.update()

#         janela.fill((9, 3, 54))
#         janela.blit(tela_de_fundo, (0, 0))
#         meteoros.draw(janela)

#         pygame.display.update()

#     pygame.quit()

# # Função principal
# def main():
#     screen = pygame.display.set_mode((largura, altura))
#     pygame.display.set_caption("Ameaça Interestelar")
#     game_state = init_screen(screen)

#     if game_state == GAME:
#         game_loop()

#     pygame.quit()
#     sys.exit()

# # Inicia o jogo
# if __name__ == "_main_":
#     main()
# # import pygame
# # import sys
# # import random
# # import os
# # from os import path
# # from config import WIDTH, HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT, largura_meteoro, altura_meteoro, SHIP_WIDTH, SHIP_HEIGHT
# # from assets import SHIP_IMG, PEW_SOUND, METEOR_IMG, BULLET_IMG, EXPLOSION_ANIM
# # import tela_inicial
# # from game_screen import game_screen

# # # Configurações de diretórios e cores
# # IMG_DIR = 'imagens'  # Diretório das imagens
# # BLACK = (0, 0, 0)
# # FPS = 60
# # GAME = "game"
# # QUIT = "quit"

# # pygame.init()

# # # Largura e altura da tela
# # largura, altura = 800, 800

# # # Definindo a largura e altura do meteoro
# # largura_meteoro = 50
# # altura_meteoro = 38

# # # Tela do jogo
# # janela = pygame.display.set_mode((largura, altura))
# # pygame.display.set_caption('Ameaça Interestelar')

# # # Fontes
# # font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
# # font = pygame.font.Font(font_path, 50)

# # # Texto do botão Play
# # botao = pygame.font.Font(font_path, 50)
# # texto_botao = "Play"


# # cor_fonte = (255, 255, 255)

# # texto_ameaca = "Ameaça"
# # texto_interestelar = "Interestelar"

# # texto_renderizado = font.render(texto_ameaca, True, cor_fonte)
# # texto_renderizado2 = font.render(texto_interestelar, True, cor_fonte)
# # botao_renderizado = font.render(texto_botao, True, cor_fonte)

# # # Posicionamento do título
# # pos_x = (largura - texto_renderizado.get_width()) // 2
# # pos_y = (altura // 2) - 100

# # pos_x2 = (largura - texto_renderizado2.get_width()) // 2
# # pos_y2 = pos_y + texto_renderizado.get_height() + 10

# # # Posicionamento do botão
# # bt_x = 300
# # bt_y = 600

# # # Definindo a área do botão
# # area_botao = pygame.Rect(bt_x, bt_y, texto_renderizado.get_width(), texto_renderizado.get_height())

# # # Função de ação do botão
# # def acao_botao():
# #     print("Botão clicado! Ação sendo executada...")

# # # Música de fundo
# # pygame.mixer.music.load(path.join('assets',"snd", '1_lift_off.flac'))
# # pygame.mixer.music.set_volume(0.4)
# # pygame.mixer.music.play(-1, 0.0)

# # # Imagem do meteoro
# # # meteoro = pygame.image.load(path.join(IMG_DIR, 'astroid.png')).convert_alpha()
# # # meteoro = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))
# # assets[METEOR_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'astroid.png')).convert_alpha()
# # assets[METEOR_IMG] = pygame.transform.scale(assets[METEOR_IMG], (largura_meteoro, altura_meteoro))

# # # Tela de fundo do jogo
# # tela_de_fundo = pygame.image.load(path.join(IMG_DIR, "SpaceBackGround.jpg"))

# # # Classe do meteoro
# # class Meteor(pygame.sprite.Sprite):
# #     def __init__(self, img):
# #         pygame.sprite.Sprite.__init__(self)
# #         self.image = img
# #         self.rect = self.image.get_rect()
# #         self.rect.x = random.randint(0, largura - largura_meteoro)
# #         self.rect.y = random.randint(-100, -altura_meteoro)
# #         self.speedx = random.randint(-4, -2)
# #         self.speedy = random.randint(-2, 3)

# #     def update(self):
# #         self.rect.x += self.speedx
# #         self.rect.y += self.speedy
# #         if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
# #             self.rect.x = random.randint(0, largura - largura_meteoro)
# #             self.rect.y = random.randint(-100, -altura_meteoro)
# #             self.speedx = random.randint(-3, 4)
# #             self.speedy = random.randint(6, 9)

# # # Função da tela inicial (do tutorial)
# # def init_screen(screen):
# #     clock = pygame.time.Clock()
# #     background = pygame.image.load(path.join(IMG_DIR, 'inicio.png')).convert()
# #     background_rect = background.get_rect()

# #     running = True
# #     while running:
# #         clock.tick(FPS)
# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 return QUIT
# #             if event.type == pygame.MOUSEBUTTONDOWN:
# #                 mouse_x, mouse_y = event.pos
# #                 if area_botao.collidepoint(mouse_x, mouse_y):
# #                     return GAME
# #         screen.fill(BLACK)
# #         screen.blit(background, background_rect)
# #         screen.blit(texto_renderizado, (pos_x, pos_y))
# #         screen.blit(texto_renderizado2, (pos_x2, pos_y2))
# #         screen.blit(botao_renderizado, (bt_x, bt_y))
# #         pygame.display.flip()

# #     return QUIT

# # # Loop principal do jogo
# # def game_loop():
# #     clock = pygame.time.Clock()
# #     meteoros = pygame.sprite.Group()
# #     for _ in range(3):
# #         meteor = Meteor(meteoro)
# #         meteoros.add(meteor)

# #     running = True
# #     while running:
# #         clock.tick(FPS)

# #         for event in pygame.event.get():
# #             if event.type == pygame.QUIT:
# #                 running = False

# #         meteoros.update()

# #         janela.fill((9, 3, 54))
# #         janela.blit(tela_de_fundo, (0, 0))
# #         meteoros.draw(janela)

# #         pygame.display.update()

# #     pygame.quit()

# # # Função principal
# # def main():
# #     screen = pygame.display.set_mode((largura, altura))
# #     pygame.display.set_caption("Ameaça Interestelar")
# #     game_state = init_screen(screen)

# #     if game_state == GAME:
# #         game_loop()

# #     pygame.quit()
# #     sys.exit()

# # # Inicia o jogo
# # if __name__ == "__main__":
# #     main()


# # # import pygame
# # # import sys
# # # import random

# # # pygame.init()

# # # largura, altura = 800, 800 #--------Criação de variável de largura e altura para ser utilizada na janela.

# # # #--------Definição de largura e altura do meteoro
# # # largura_meteoro = 50
# # # altura_meteoro = 38

# # # #--------Criação da janela propriamente dito com 800 de largura e 800 de altura.
# # # janela = pygame.display.set_mode((largura, altura))
# # # pygame.display.set_caption('Ameaça Interestelar')

# # # font_path = 'Fontes/PressStart2P-Regular.ttf'  # Caminho do arquivo da fonte
# # # font = pygame.font.Font(font_path, 50)  # Tamanho da fonte (50 aqui)

# # # #--------Imagem utilizada no botão + coordenada do botão.
# # # botao = pygame.font.Font(font_path, 50)
# # # texto_botao = "Play"

# # # #Substituição do ícone do pygame pelo ícone de "Ameaça Interestelar"
# # # icone = pygame.image.load("imagens/logo.png")
# # # pygame.display.set_icon(icone)

# # # cor_fonte = (255, 255, 255)

# # # texto_ameaca = "Ameaça" 
# # # texto_interestelar = "Interestelar"

# # # texto_renderizado = font.render(texto_ameaca, True, cor_fonte)
# # # texto_renderizado2 = font.render(texto_interestelar, True, cor_fonte)
# # # botao_renderizado = font.render(texto_botao, True, cor_fonte)



# # # pos_x = (largura - texto_renderizado.get_width()) // 2  
# # # pos_y = (altura // 2) - 100  

# # # pos_x2 = (largura - texto_renderizado2.get_width()) // 2  
# # # pos_y2 = pos_y + texto_renderizado.get_height() + 10  

# # # bt_x = 300
# # # bt_y = 600

# # # area_botao = pygame.Rect(bt_x, bt_y, texto_renderizado.get_width(), texto_renderizado.get_height())

# # # def acao_botao():
# # #     print("Botão clicado! Ação sendo executada...")

# # # pygame.mixer.music.load('snd/1_lift_off.flac')  
# # # pygame.mixer.music.set_volume(0.4)        
# # # pygame.mixer.music.play(-1, 0.0)          

# # # #--------Imagem do meteoro + escala do meteoro
# # # meteoro = pygame.image.load('imagens/astroid.png').convert_alpha()
# # # meteoro = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))
# # # meteoro_pequeno = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))

# # # #--------Imagem de fundo do jogo
# # # tela_de_fundo = pygame.image.load("imagens/SpaceBackGround.jpg")

# # # clock = pygame.time.Clock()
# # # FPS = 60

# # # #--------Classe Meteor para criação dos meteoros
# # # class Meteor(pygame.sprite.Sprite):
# # #     def __init__(self, img): 
# # #         pygame.sprite.Sprite.__init__(self)

# # #         self.image = img
# # #         self.rect = self.image.get_rect()
# # #         self.rect.x = random.randint(0, largura-largura_meteoro)
# # #         self.rect.y = random.randint(-100, -altura_meteoro)
# # #         self.speedx = random.randint(-4, -2)
# # #         self.speedy = random.randint(-2, 3)

# # #     def update(self): #--------Atualiza a posição do meteoro.

# # #         self.rect.x += self.speedx
# # #         self.rect.y += self.speedy
       
# # #        #--------Redefine a posição se o meteoro sair da tela
# # #         if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
# # #             self.rect.x = random.randint(0, largura-largura_meteoro)
# # #             self.rect.y = random.randint(-100, -altura_meteoro)
# # #             self.speedx = random.randint(-3, 4)
# # #             self.speedy = random.randint(6, 9)

# # # game = True

# # # meteoros = pygame.sprite.Group() #--------Cria um grupo de meteoros e adiciona múltiplos meteoros ao grupo

# # # #--------Define a quantidade de meteoros.
# # # for _ in range(3):  
# # #     meteor = Meteor(meteoro)
# # #     meteoros.add(meteor)

# # # while game:
# # #     clock.tick(FPS)
# # #     for event in pygame.event.get():
# # #         if event.type == pygame.QUIT:
# # #             game = False
# # #             sys.exit()
            
# # #         if event.type == pygame.MOUSEBUTTONDOWN:
# # #             mouse_x, mouse_y = event.pos
# # #             if area_botao.collidepoint(mouse_x, mouse_y):
# # #                 acao_botao()

# # #     meteoros.update() #--------Atualiza a posição de todos os meteoros


# # #     janela.fill((9, 3, 54))  #--------preenche o fundo da janela
    
# # #     janela.blit(tela_de_fundo, (0, 0))
# # #     janela.blit(texto_renderizado, (pos_x, pos_y))
# # #     janela.blit(texto_renderizado2, (pos_x2, pos_y2))
# # #     janela.blit(botao_renderizado, (bt_x, bt_y))


# # #     meteoros.draw(janela) #--------Desenha todos os meteoros no grupo
    
# # #     pygame.display.update() #--------Atualiza a tela 
# # # pygame.quit()