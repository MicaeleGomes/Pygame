import pygame
import sys
import random

pygame.init()

largura, altura = 800, 800 #--------Criação de variável de largura e altura para ser utilizada na janela.

#--------Definição de largura e altura do meteoro
largura_meteoro = 50
altura_meteoro = 38

#--------Criação da janela propriamente dito com 800 de largura e 800 de altura.
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Ameaça Interestelar')

font_path = 'Fontes/PressStart2P-Regular.ttf'  # Caminho do arquivo da fonte
font = pygame.font.Font(font_path, 50)  # Tamanho da fonte (50 aqui)

#--------Imagem utilizada no botão + coordenada do botão.
botao = pygame.font.Font(font_path, 50)
texto_botao = "Play"

#Substituição do ícone do pygame pelo ícone de "Ameaça Interestelar"
icone = pygame.image.load("imagens/logo.png")
pygame.display.set_icon(icone)

cor_fonte = (255, 255, 255)

texto_ameaca = "Ameaça" 
texto_interestelar = "Interestelar"

texto_renderizado = font.render(texto_ameaca, True, cor_fonte)
texto_renderizado2 = font.render(texto_interestelar, True, cor_fonte)
botao_renderizado = font.render(texto_botao, True, cor_fonte)



pos_x = (largura - texto_renderizado.get_width()) // 2  
pos_y = (altura // 2) - 100  

pos_x2 = (largura - texto_renderizado2.get_width()) // 2  
pos_y2 = pos_y + texto_renderizado.get_height() + 10  

bt_x = 300
bt_y = 600

area_botao = pygame.Rect(pos_x, pos_y, texto_renderizado.get_width(), texto_renderizado.get_height())

def acao_botao():
    print("Botão clicado! Ação sendo executada...")

pygame.mixer.music.load('snd/1_lift_off.flac')  
pygame.mixer.music.set_volume(0.4)        
pygame.mixer.music.play(-1, 0.0)          

#--------Imagem do meteoro + escala do meteoro
meteoro = pygame.image.load('imagens/astroid.png').convert_alpha()
meteoro = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))
meteoro_pequeno = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))

#--------Imagem de fundo do jogo
tela_de_fundo = pygame.image.load("imagens/SpaceBackGround.jpg")

clock = pygame.time.Clock()
FPS = 60

#--------Classe Meteor para criação dos meteoros
class Meteor(pygame.sprite.Sprite):
    def __init__(self, img): 
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura-largura_meteoro)
        self.rect.y = random.randint(-100, -altura_meteoro)
        self.speedx = random.randint(-4, -2)
        self.speedy = random.randint(-2, 3)

    def update(self): #--------Atualiza a posição do meteoro.

        self.rect.x += self.speedx
        self.rect.y += self.speedy
       
       #--------Redefine a posição se o meteoro sair da tela
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = random.randint(0, largura-largura_meteoro)
            self.rect.y = random.randint(-100, -altura_meteoro)
            self.speedx = random.randint(-3, 4)
            self.speedy = random.randint(6, 9)

game = True

meteoros = pygame.sprite.Group() #--------Cria um grupo de meteoros e adiciona múltiplos meteoros ao grupo

#--------Define a quantidade de meteoros.
for _ in range(3):  
    meteor = Meteor(meteoro)
    meteoros.add(meteor)

while game:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if area_botao.collidepoint(mouse_x, mouse_y):
                acao_botao()

    meteoros.update() #--------Atualiza a posição de todos os meteoros


    janela.fill((9, 3, 54))  #--------preenche o fundo da janela
    
    janela.blit(tela_de_fundo, (0, 0))
    janela.blit(texto_renderizado, (pos_x, pos_y))
    janela.blit(texto_renderizado2, (pos_x2, pos_y2))
    janela.blit(botao_renderizado, (bt_x, bt_y))


    meteoros.draw(janela) #--------Desenha todos os meteoros no grupo
    
    pygame.display.update() #--------Atualiza a tela 
pygame.quit()