import pygame
import sys
import random

pygame.init()
def exibir_tela_final(score):
    largura, altura = 800, 800 #--------Criação de variável de largura e altura para ser utilizada na janela.

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

    texto_ameaca = "Sua pontuação:" 

    texto_renderizado = font.render(texto_ameaca, True, cor_fonte)


    pos_x = (largura - texto_renderizado.get_width()) // 2  
    pos_y = (altura // 2) - 100  

    pos_y2 = pos_y + texto_renderizado.get_height() + 10  


    pygame.mixer.music.load('snd/1_lift_off.flac')  
    pygame.mixer.music.set_volume(0.4)        
    pygame.mixer.music.play(-1, 0.0)          


    #--------Imagem de fundo do jogo
    tela_de_fundo = pygame.image.load("imagens/SpaceBackGround.jpg")
    try:
        with open('score.txt', 'r') as file:
            score = int(file.read())  
    except FileNotFoundError:
        score = 0

    texto_interestelar = f"{score}"

    texto_renderizado2 = font.render(texto_interestelar, True, cor_fonte)

    texto_renderizado2 = font.render(texto_interestelar, True, cor_fonte)

    pos_x2 = (largura - texto_renderizado2.get_width()) // 2  




    game = True


    #--------Define a quantidade de meteoros.

    while game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                sys.exit()
                
        janela.fill((9, 3, 54))  #--------preenche o fundo da janela
        
        janela.blit(tela_de_fundo, (0, 0))
        janela.blit(texto_renderizado, (pos_x, pos_y))
        janela.blit(texto_renderizado2, (pos_x2, pos_y2))
        
        pygame.display.update() #--------Atualiza a tela 
    pygame.quit()