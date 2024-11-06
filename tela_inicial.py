import pygame
import sys
import random

pygame.init()

largura, altura = 800, 800 #Criação de variável de largura e altura para ser utilizada na janela.

#Definição de largura e altura do meteoro
largura_meteoro = 50
altura_meteoro = 38

#Criação da janela propriamente dito com 800 de largura e 800 de altura.
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Ameaça Interestelar')

#Imagem utilizada no botão + coordenada do botão.
imagem_botao = pygame.image.load('imagens/botaov2.png')
botao = imagem_botao.get_rect(center=(390, 600))

#Substituição do ícone do pygame pelo ícone de "Ameaça Interestelar"
icone = pygame.image.load("imagens/logo.png")
pygame.display.set_icon(icone)

#Imagem do meteoro + escala do meteoro
meteoro = pygame.image.load('imagens/astroid.png').convert_alpha()
meteoro = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))
meteoro_pequeno = pygame.transform.scale(meteoro, (largura_meteoro, altura_meteoro))

#Imagem de fundo do jogo
tela_de_fundo = pygame.image.load("imagens/SpaceBackGround.jpg")

#Nome do jogo (logo) na tela.
logo = pygame.image.load('imagens/logo.png')
pygame.display.set_icon(logo)

# Classe Meteor para criação dos meteoros
class Meteor(pygame.sprite.Sprite):
    def __init__(self, img): 
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura-largura_meteoro)
        self.rect.y = random.randint(-100, -altura_meteoro)
        self.speedx = random.randint(-4, -2)
        self.speedy = random.randint(-2, 3)

    def update(self): # Atualiza a posição do meteoro.

        self.rect.x += self.speedx
        self.rect.y += self.speedy
       
       # Redefine a posição se o meteoro sair da tela
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = random.randint(0, largura-largura_meteoro)
            self.rect.y = random.randint(-100, -altura_meteoro)
            self.speedx = random.randint(-1, 1)
            self.speedy = random.randint(1, 3)

game = True

meteoros = pygame.sprite.Group() # Cria um grupo de meteoros e adiciona múltiplos meteoros ao grupo

#Define a quantidade de meteoros.
for _ in range(3):  
    meteor = Meteor(meteoro)
    meteoros.add(meteor)

while game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if botao.collidepoint(mouse_x, mouse_y):
                print("Botão clicado!")

    meteoros.update() # Atualiza a posição de todos os meteoros


    janela.fill((9, 3, 54))  #preenche o fundo da janela
    
    janela.blit(tela_de_fundo, (0, 0))
    janela.blit(logo, (150, 80))
    janela.blit(imagem_botao, botao)

    meteoros.draw(janela) # Desenha todos os meteoros no grupo

    pygame.display.update() #Atualiza a tela 
pygame.quit()