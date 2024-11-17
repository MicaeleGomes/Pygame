import pygame
import sys
import os
from config import FPS, WIDTH, HEIGHT, BLACK, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT, SCORE_POSITION, SCORE_COLOR, SCORE_BG_COLOR
from assets import load_assets, BACKGROUND, SCORE_FONT, TIMER_ICON_IMG, ALIEN_ICON_IMG
from sprites import Ship, Alien, Meteor, Bullet, Explosion

pygame.init()

def game_screen(window):
    score = 0  # Pontuação inicial
    clock = pygame.time.Clock()

    # Carrega os assets
    assets = load_assets()

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    all_aliens = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    all_meteors = pygame.sprite.Group()
    groups = {'all_sprites': all_sprites, 'all_aliens': all_aliens, 'all_bullets': all_bullets, 'all_meteors': all_meteors}

    # Criação do jogador
    player = Ship(groups, assets)
    all_sprites.add(player)

    # Criação dos aliens
    for i in range(3):
        alien = Alien(assets)
        all_sprites.add(alien)
        all_aliens.add(alien)

    # Criação dos meteoros
    for _ in range(2):  
        meteor = Meteor(assets)
        all_sprites.add(meteor)
        all_meteors.add(meteor)

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}
    # GAME_DURATION = 60000  # 60 segundos
    GAME_DURATION = 10000  # 60 segundos
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
                assets['destroy_sound'].play()
                a = Alien(assets)
                all_sprites.add(a)
                all_aliens.add(a)
                explosao_alien = Explosion(alien.rect.center, assets)
                all_sprites.add(explosao_alien)
                score += 100

            # Penaliza se alien sair da tela
            for alien in all_aliens:
                if alien.rect.top > HEIGHT:
                    score -= 100
                    alien.kill()
                    a = Alien(assets)
                    all_sprites.add(a)
                    all_aliens.add(a)

            # Verifica colisões entre tiro e meteoro
            bullet_hits_meteors = pygame.sprite.groupcollide(all_bullets, all_meteors, True, False)
            for bullet in bullet_hits_meteors:
                bullet.kill()

            # Verifica colisões entre meteoro e nave
            colisao_meteoros = pygame.sprite.spritecollide(player, all_meteors, True, pygame.sprite.collide_mask)
            if len(colisao_meteoros) > 0:
                assets['boom_sound'].play()
                player.kill()
                explosao = Explosion(player.rect.center, assets)
                all_sprites.add(explosao)
                state = EXPLODING
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

        # Renderização
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

    return score
