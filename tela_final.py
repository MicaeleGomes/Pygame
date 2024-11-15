import pygame
import os
import sys
from config import WIDTH, HEIGHT, INIT, QUIT, GAME, BLACK

def exibir_tela_final(window, score):
    largura, altura = 800, 800  # Definição da largura e altura da tela

    # Criação da janela
    pygame.display.set_caption('Ameaça Interestelar')

    font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
    font = pygame.font.Font(font_path, 20)  # Tamanho da fonte

    # Texto que mostra a pontuação
    texto_ameaca = "Sua pontuação:" 
    texto_renderizado = font.render(texto_ameaca, True, (255, 255, 255))

    # Posições dos textos
    pos_x = (largura - texto_renderizado.get_width()) // 2  
    pos_y = (altura // 2) - 100  
    pos_y2 = pos_y + texto_renderizado.get_height() + 10  

    # Música de fundo
    pygame.mixer.music.load(os.path.join('assets', 'snd', '1_lift_off.flac'))
    pygame.mixer.music.set_volume(0.4)        
    pygame.mixer.music.play(-1, 0.0)          

    # Imagem de fundo do jogo
    tela_de_fundo = pygame.image.load(os.path.join('assets', 'img', 'SpaceBackGround.jpg'))

    texto_interestelar = f"{score}"

    texto_renderizado2 = font.render(texto_interestelar, True, (255, 255, 255))
    pos_x2 = (largura - texto_renderizado2.get_width()) // 2  

    # Texto para reiniciar o jogo
    texto_reiniciar = "Aperte ENTER para jogar novamente"
    texto_renderizado_reiniciar = font.render(texto_reiniciar, True, (255, 255, 255))
    pos_x_reiniciar = (largura - texto_renderizado_reiniciar.get_width()) // 2  
    pos_y_reiniciar = pos_y2 + texto_renderizado2.get_height() + 10

    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
                sys.exit()

            # Verifica se pressionou a tecla ENTER para reiniciar
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:  # Se pressionou ENTER
                    return GAME  # Retorna para o estado de jogo (REINICIAR)

        # Preenche o fundo da janela com uma cor
        window.fill(BLACK)  
        
        # Desenha o fundo e os textos na tela
        window.blit(tela_de_fundo, (0, 0))
        window.blit(texto_renderizado, (pos_x, pos_y))
        window.blit(texto_renderizado2, (pos_x2, pos_y2))
        window.blit(texto_renderizado_reiniciar, (pos_x_reiniciar, pos_y_reiniciar))
        
        # Atualiza a tela
        pygame.display.update()

    return QUIT  # Se o jogador fechar a tela final
