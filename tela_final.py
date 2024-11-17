import pygame
import os
import textwrap
from config import WIDTH, HEIGHT, GAME, QUIT, BLACK

def exibir_tela_final(window, score):
    pygame.display.set_caption('Ameaça Interestelar')

    # Carrega a fonte
    font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
    font_large = pygame.font.Font(font_path, 50)
    font_medium = pygame.font.Font(font_path, 30)
    font_small = pygame.font.Font(font_path, 20)
    cor_fonte = (255, 255, 255)

    # Textos a serem exibidos
    titulo = "Sua Pontuação"
    texto_pontuacao = f"{score}"
    texto_instrucoes = "Pressione ENTER para jogar novamente\nou ESC para sair"

    # Calcula a altura total dos elementos para centralização
    titulo_height = font_large.get_height()
    pontuacao_height = font_medium.get_height()
    instrucoes_height = font_small.get_height() * len(textwrap.wrap(texto_instrucoes, width=40))
    altura_total = titulo_height + pontuacao_height + instrucoes_height + 60

    # Calcula as posições para centralizar os textos
    y_inicial = (HEIGHT - altura_total) // 2
    y_titulo = y_inicial
    y_pontuacao = y_titulo + titulo_height + 30
    y_instrucoes = y_pontuacao + pontuacao_height + 40

    # Carrega o fundo
    tela_de_fundo = pygame.image.load(os.path.join('assets', 'img', 'SpaceBackGround.jpg'))
    tela_de_fundo = pygame.transform.scale(tela_de_fundo, (WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT  # Retorna QUIT se o jogador fechar a janela
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER para reiniciar
                    return GAME  # Retorna GAME para reiniciar o jogo
                if event.key == pygame.K_ESCAPE:  # ESC para sair
                    return QUIT  # Retorna QUIT para encerrar o jogo

        # Desenha o fundo e os textos
        window.blit(tela_de_fundo, (0, 0))

        # Desenha o título
        titulo_renderizado = font_large.render(titulo, True, cor_fonte)
        titulo_x = (WIDTH - titulo_renderizado.get_width()) // 2
        window.blit(titulo_renderizado, (titulo_x, y_titulo))

        # Desenha a pontuação
        pontuacao_renderizada = font_medium.render(texto_pontuacao, True, cor_fonte)
        pontuacao_x = (WIDTH - pontuacao_renderizada.get_width()) // 2
        window.blit(pontuacao_renderizada, (pontuacao_x, y_pontuacao))

        # Desenha as instruções
        y_atual_instrucoes = y_instrucoes
        for linha in textwrap.wrap(texto_instrucoes, width=40):
            instrucoes_renderizadas = font_small.render(linha, True, cor_fonte)
            instrucoes_x = (WIDTH - instrucoes_renderizadas.get_width()) // 2
            window.blit(instrucoes_renderizadas, (instrucoes_x, y_atual_instrucoes))
            y_atual_instrucoes += font_small.get_height()

        pygame.display.update()  # Atualiza a tela para exibir os elementos


