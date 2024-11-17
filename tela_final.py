import pygame
import os
import textwrap
from config import WIDTH, HEIGHT, GAME, QUIT, BLACK

def exibir_tela_final(window, score):
    pygame.display.set_caption('Ameaça Interestelar')

    # Configurações de cores e fontes
    font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
    font_large = pygame.font.Font(font_path, 40)
    font_medium = pygame.font.Font(font_path, 70)
    font_small = pygame.font.Font(font_path, 25)
    cor_fonte_branca = (255, 255, 255)
    cor_fonte_roxa = (128, 0, 128)  

    # Carrega o fundo
    tela_de_fundo = pygame.image.load(os.path.join('assets', 'img', 'SpaceBackGround.jpg'))
    tela_de_fundo = pygame.transform.scale(tela_de_fundo, (WIDTH, HEIGHT))

    # Carrega o ícone da nave ao lado do score
    alien_img = pygame.image.load(os.path.join('assets', 'img', 'nave_telafinal.png'))
    alien_img = pygame.transform.scale(alien_img, (70, 70))  # Ajusta o tamanho da nave

    # Textos
    titulo = "Sua Pontuação"
    texto_instrucoes = "Pressione ENTER para jogar novamente ou ESC para sair"

    # Configura a música de fundo
    pygame.mixer.music.load(os.path.join('assets', 'snd', '1_lift_off.flac'))
    pygame.mixer.music.set_volume(0.4)        
    pygame.mixer.music.play(-1, 0.0)

    # Calcula posições dos elementos
    titulo_height = font_large.get_height()
    pontuacao_height = font_medium.get_height()
    instrucoes_height = font_small.get_height() * len(textwrap.wrap(texto_instrucoes, width=30))
    altura_total = titulo_height + pontuacao_height + instrucoes_height + 90

    y_inicial = (HEIGHT - altura_total) // 2
    y_titulo = y_inicial
    y_pontuacao = y_titulo + titulo_height + 50  # Espaçamento entre textos
    y_instrucoes = y_pontuacao + pontuacao_height + 70  # Espaçamento entre textos

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Para a música ao sair
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()  # Para a música ao reiniciar
                    return GAME
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()  # Para a música ao sair
                    return QUIT

        # Desenha o fundo
        window.blit(tela_de_fundo, (0, 0))

        # Desenha o título
        titulo_renderizado = font_large.render(titulo, True, cor_fonte_branca)
        titulo_x = (WIDTH - titulo_renderizado.get_width()) // 2
        window.blit(titulo_renderizado, (titulo_x, y_titulo))

        # Desenha o score com o alien ao lado
        pontuacao_renderizada = font_medium.render(f"{score}", True, cor_fonte_roxa)
        pontuacao_x = (WIDTH - pontuacao_renderizada.get_width()) // 2
        alien_x = pontuacao_x + pontuacao_renderizada.get_width() + 10
        alien_y = y_pontuacao + (pontuacao_height - alien_img.get_height()) // 2
        window.blit(pontuacao_renderizada, (pontuacao_x, y_pontuacao))
        window.blit(alien_img, (alien_x, alien_y))

        # Desenha as instruções
        y_atual_instrucoes = y_instrucoes
        for linha in textwrap.wrap(texto_instrucoes, width=30):
            instrucoes_renderizadas = font_small.render(linha, True, cor_fonte_branca)
            instrucoes_x = (WIDTH - instrucoes_renderizadas.get_width()) // 2
            window.blit(instrucoes_renderizadas, (instrucoes_x, y_atual_instrucoes))
            y_atual_instrucoes += font_small.get_height()

        pygame.display.update()
        clock.tick(60)
