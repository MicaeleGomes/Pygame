import pygame
import sys
import os
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT, SCORE_POSITION, SCORE_COLOR, SCORE_BG_COLOR
from assets import load_assets, DESTROY_SOUND, BOOM_SOUND, BACKGROUND, SCORE_FONT, TIMER_ICON_IMG, ALIEN_ICON_IMG
from sprites import Ship, Alien, Meteor, Bullet, Explosion

pygame.init()

def exibir_tela_final(score, window):
    largura, altura = 800, 800  # Definindo o tamanho da janela

    # Criação da janela de exibição final
    pygame.display.set_caption('Ameaça Interestelar')

    # Fonte
    font_path = os.path.join('assets', 'font', 'PressStart2P-Regular.ttf')
    font = pygame.font.Font(font_path, 50)  # Fonte para os textos

    cor_fonte = (255, 255, 255)  # Cor da fonte (branca)

    # Texto que aparece na tela final
    texto_ameaca = "Sua pontuação:" 
    texto_renderizado = font.render(texto_ameaca, True, cor_fonte)

    # Posições para centralizar o texto
    pos_x = (largura - texto_renderizado.get_width()) // 2
    pos_y = (altura // 2) - 100
    pos_y2 = pos_y + texto_renderizado.get_height() + 10

    # Música de fundo
    pygame.mixer.music.load(os.path.join('assets', 'snd', '1_lift_off.flac'))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1, 0.0)

    # Imagem de fundo
    tela_de_fundo = pygame.image.load(os.path.join('assets', 'img', 'SpaceBackGround.jpg'))

    # Texto de pontuação
    texto_interestelar = f"{score}"
    texto_renderizado2 = font.render(texto_interestelar, True, cor_fonte)
    pos_x2 = (largura - texto_renderizado2.get_width()) // 2

    # Mensagem para reiniciar o jogo
    texto_reiniciar = "Aperte Enter para jogar novamente!"
    texto_renderizado_reiniciar = font.render(texto_reiniciar, True, cor_fonte)
    pos_x_reiniciar = (largura - texto_renderizado_reiniciar.get_width()) // 2
    pos_y_reiniciar = pos_y2 + texto_renderizado2.get_height() + 20  # Ajustando a posição

    game = True  # Controla o loop da tela final

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                sys.exit()

            # Detecta quando a tecla Enter é pressionada
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # A tecla Enter
                    game = False  # Sai do loop da tela final
                    return "REINICIAR"  # Retorna o comando para reiniciar o jogo

        # Preenche o fundo da janela com a cor escolhida
        window.fill((9, 3, 54))
        window.blit(tela_de_fundo, (0, 0))  # Exibe a imagem de fundo
        window.blit(texto_renderizado, (pos_x, pos_y))  # Exibe a pontuação
        window.blit(texto_renderizado2, (pos_x2, pos_y2))  # Exibe o valor da pontuação
        window.blit(texto_renderizado_reiniciar, (pos_x_reiniciar, pos_y_reiniciar))  # Exibe a mensagem para reiniciar

        pygame.display.update()  # Atualiza a tela para mostrar as mudanças


def game_screen(window):
    score = 0  # Pontuação inicial
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando grupos de sprites
    all_sprites = pygame.sprite.Group()
    all_aliens = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    all_meteors = pygame.sprite.Group()
    groups = {'all_sprites': all_sprites, 'all_aliens': all_aliens, 'all_bullets': all_bullets, 'all_meteors': all_meteors}

    # Criando o jogador
    player = Ship(groups, assets)
    all_sprites.add(player)

    # Criando os aliens
    for i in range(3):
        alien = Alien(assets)
        all_sprites.add(alien)
        all_aliens.add(alien)

    # Criando meteoros
    for _ in range(2):  
        meteor = Meteor(assets)
        all_sprites.add(meteor)
        all_meteors.add(meteor)

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}    
    GAME_DURATION = 10000  # Duração do jogo em milissegundos
    start_time = pygame.time.get_ticks()

    pygame.mixer.music.play(loops=-1)
    
    while state != DONE:
        clock.tick(FPS)

        # Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
            if state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 9
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 9
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                if event.type == pygame.KEYUP:
                    if event.key in keys_down:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 9
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 9

        # Atualiza o estado do jogo
        all_sprites.update()
        all_meteors.update()

        if state == PLAYING:
            # Verifica colisões entre tiro e alien
            hits = pygame.sprite.groupcollide(all_aliens, all_bullets, True, True, pygame.sprite.collide_mask)
            for alien in hits:
                assets[DESTROY_SOUND].play()
                a = Alien(assets)
                all_sprites.add(a)
                all_aliens.add(a)
                explosao_alien = Explosion(alien.rect.center, assets)
                all_sprites.add(explosao_alien)
                score += 100

            # Atualiza a pontuação se o alien passar da tela
            for alien in all_aliens:
                if alien.rect.top > HEIGHT:
                    score -= 100
                    alien.kill()
                    a = Alien(assets)
                    all_sprites.add(a)
                    all_aliens.add(a)

            # Verifica colisões entre tiros e meteoros
            bullet_hits_meteors = pygame.sprite.groupcollide(all_bullets, all_meteors, True, False)
            for bullet in bullet_hits_meteors:
                bullet.kill()

            # Verifica colisões entre meteoro e nave
            colisao_meteoros = pygame.sprite.spritecollide(player, all_meteors, True, pygame.sprite.collide_mask)
            if len(colisao_meteoros) > 0:
                assets[BOOM_SOUND].play()
                player.kill()
                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_tick = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks * len(explosao.explosion_anim) + 400

            if colisao_meteoros:
                score -= 200

            while len(all_meteors) < 2:
                novo_meteoro = Meteor(assets)
                all_meteors.add(novo_meteoro)
                all_sprites.add(novo_meteoro)

        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                state = PLAYING
                player = Ship(groups, assets)
                all_sprites.add(player)

        # Calcula o tempo restante
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, (GAME_DURATION - elapsed_time) // 1000)

        if remaining_time <= 0:
            state = DONE
            with open("score.txt", "w") as file:
                file.write(str(score))

        # Gera saídas
        window.fill(BLACK)
        window.blit(assets[BACKGROUND], (0, 0))

        all_sprites.draw(window)
        all_meteors.draw(window)

        # Desenha o placar
        pygame.draw.rect(window, SCORE_BG_COLOR, (*SCORE_POSITION, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), border_radius=10)
        alien_icon = assets[ALIEN_ICON_IMG]
        alien_icon_position = (SCORE_POSITION[0] + 10, SCORE_POSITION[1] + (SCORE_BOX_HEIGHT - alien_icon.get_height()) // 2)
        window.blit(alien_icon, alien_icon_position)

        text_surface = assets[SCORE_FONT].render("{:07d}".format(score), True, SCORE_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (alien_icon_position[0] + 40, SCORE_POSITION[1] + (SCORE_BOX_HEIGHT - text_rect.height) // 2)
        window.blit(text_surface, text_rect)

        # Desenha o temporizador
        TIMER_BOX_POSITION = (20, 70)
        pygame.draw.rect(window, SCORE_BG_COLOR, (*TIMER_BOX_POSITION, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), border_radius=10)
        timer_icon = assets[TIMER_ICON_IMG]
        timer_icon_position = (TIMER_BOX_POSITION[0] + 10, TIMER_BOX_POSITION[1] + (SCORE_BOX_HEIGHT - timer_icon.get_height()) // 2)
        window.blit(timer_icon, timer_icon_position)

        time_surface = assets[SCORE_FONT].render("{:02d}".format(remaining_time), True, SCORE_COLOR)
        time_rect = time_surface.get_rect()
        time_rect.topleft = (timer_icon_position[0] + 40, TIMER_BOX_POSITION[1] + (SCORE_BOX_HEIGHT - time_rect.height) // 2)
        window.blit(time_surface, time_rect)

        pygame.display.update()

    # Exibe a tela final após o término do jogo
    return exibir_tela_final(score, window)