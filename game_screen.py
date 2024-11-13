import pygame
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT, SCORE_POSITION, SCORE_COLOR, SCORE_BG_COLOR
from assets import load_assets, DESTROY_SOUND, BOOM_SOUND, BACKGROUND, SCORE_FONT, TIMER_ICON_IMG, ALIEN_ICON_IMG
from sprites import Ship, Alien, Meteor, Bullet, Explosion

def game_screen(window):
    # global score  
    score = 0     

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando um grupo de aliens e tiros
    all_sprites = pygame.sprite.Group()
    all_aliens = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    all_meteors = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_aliens'] = all_aliens
    groups['all_bullets'] = all_bullets
    groups['all_meteors'] = all_meteors

    # Criando o jogador
    player = Ship(groups, assets)
    all_sprites.add(player)

    # Criando os aliens
    for i in range(3):
        alien = Alien(assets)
        all_sprites.add(alien)
        all_aliens.add(alien)

    #--------Define a quantidade de meteoros.
    for _ in range(2):  
        # meteor = Meteor(meteoro)
        meteor = Meteor(assets)
        all_sprites.add(meteor)
        all_meteors.add(meteor)

    #---------Define estados da nave
    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}    

    # -------- Definindo temporizador
    GAME_DURATION = 60000  # Duração do jogo em milissegundos (60 segundos)
    start_time = pygame.time.get_ticks()  

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 9
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 9
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 9
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 9

        # Atualiza estado do jogo

        # Atualizando a posição dos aliens
        all_sprites.update()
        # Atualiza a posição de todos os meteoros
        all_meteors.update()

        if state == PLAYING:
            # Verifica se houve colisão entre tiro e o alien 
            hits = pygame.sprite.groupcollide(all_aliens, all_bullets, True, True, pygame.sprite.collide_mask)
            for alien in hits:
                # O alien é destruido e precisa ser recriado
                assets[DESTROY_SOUND].play()
                a = Alien(assets)
                all_sprites.add(a)
                all_aliens.add(a)

                # No lugar do alien antigo, adicionar uma explosão.
                explosao_alien = Explosion(alien.rect.center, assets)
                all_sprites.add(explosao_alien)

                # Ganhou pontos!
                score += 100

            # Atualize o score se o alien passar da borda da tela
            for alien in all_aliens:
                if alien.rect.top > HEIGHT:  
                    score -= 100  
                    alien.kill() 
                    # Reposicione um novo alien
                    a = Alien(assets)
                    all_sprites.add(a)
                    all_aliens.add(a)
            
            # Verifica se houve colisão entre tiros e meteoros
            bullet_hits_meteors = pygame.sprite.groupcollide(all_bullets, all_meteors, True, False)
            for bullet in bullet_hits_meteors:
                bullet.kill()  # Remove o tiro visualmente

            # Verifica se houve colisão entre meteoro e a nave
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
            
            #se o meteoro bater na nave, o jogador perde 200 pontos.
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

        # Calcula o tempo restante em segundos
        elapsed_time = pygame.time.get_ticks( ) - start_time
        remaining_time = max(0, (GAME_DURATION - elapsed_time) // 1000)  # Converte para segundos

        # Finaliza o jogo quando o tempo acaba
        if remaining_time <= 0:
            state = DONE
            with open("score.txt", "w") as file:
                file.write(str(score))

        # ----- Gera saídas
        window.fill(BLACK)
        window.blit(assets[BACKGROUND], (0, 0))

        #------------- Desenhando aliens e meteoros
        all_sprites.draw(window)
        all_meteors.draw(window) 

        # ------------ Desenha o placar com a imagem do alien ao lado do score
        pygame.draw.rect(window, SCORE_BG_COLOR, (*SCORE_POSITION, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), border_radius=10)

        alien_icon = assets[ALIEN_ICON_IMG]  # Carrega o ícone do alien
        alien_icon_position = (SCORE_POSITION[0] + 10, SCORE_POSITION[1] + (SCORE_BOX_HEIGHT - alien_icon.get_height()) // 2)
        window.blit(alien_icon, alien_icon_position)

        text_surface = assets[SCORE_FONT].render("{:07d}".format(score), True, SCORE_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (alien_icon_position[0] + 40, SCORE_POSITION[1] + (SCORE_BOX_HEIGHT - text_rect.height) // 2)
        window.blit(text_surface, text_rect)

        # Desenha a caixinha do temporizador
        TIMER_BOX_POSITION = (20, 70)  # Posição do temporizador (abaixo do placar)

        pygame.draw.rect(window, SCORE_BG_COLOR, (*TIMER_BOX_POSITION, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), border_radius=10)

        # Centralizando o ícone do cronômetro
        timer_icon = assets[TIMER_ICON_IMG]  # Carrega o ícone do cronômetro de assets
        timer_icon_position = (TIMER_BOX_POSITION[0] + 10, TIMER_BOX_POSITION[1] + (SCORE_BOX_HEIGHT - timer_icon.get_height()) // 2)
        window.blit(timer_icon, timer_icon_position)

        time_surface = assets[SCORE_FONT].render("{:02d}".format(remaining_time), True, SCORE_COLOR)
        time_rect = time_surface.get_rect()
        time_rect.topleft = (timer_icon_position[0] + 40, TIMER_BOX_POSITION[1] + (SCORE_BOX_HEIGHT - time_rect.height) // 2)
        window.blit(time_surface, time_rect)

        pygame.display.update()

    return score  