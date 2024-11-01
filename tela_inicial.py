import pygame

pygame.init()

largura, altura = 800, 800

METEOR_WIDTH = 50
METEOR_HEIGHT = 38

janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Ameaça Interestelar')

icone = pygame.image.load("imagens/logo.png")
pygame.display.set_icon(icone)

meteoro = pygame.image.load('imagens/astroid.png')
meteoro_pequeno = pygame.transform.scale(meteoro, (METEOR_WIDTH, METEOR_HEIGHT))


tela_de_fundo = pygame.image.load("imagens/SpaceBackGround.jpg")

logo = pygame.image.load('imagens/logo.png')
pygame.display.set_icon(logo)

game = True

meteoro_x = 200
meteoro_y = -METEOR_HEIGHT
meteor_speedx = 3
meteor_speedy = 4

while game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    
    meteoro_x += meteor_speedx
    meteoro_y += meteor_speedy

    if meteoro_y > altura or meteoro_x + METEOR_WIDTH < 0 or meteoro_x > largura:
        meteoro_x = 200
        meteoro_y = -METEOR_HEIGHT

    janela.fill((9, 3, 54))  
    
    janela.blit(tela_de_fundo, (0, 0))
    janela.blit(meteoro_pequeno, (meteoro_x, meteoro_y))
    janela.blit(logo, (150, 80))


    pygame.display.update()  
pygame.quit()