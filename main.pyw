#!/usr/bin/env python3
import pygame as pg
from pygame.locals import *
import random, sys, itertools

pg.init()
pg.font.init()
pg.mixer.init()

#own imports
from data import IMAGES, SOUNDS, MUSIC
from constants import *
from game_objects import EnemyShip, PlayerShip


def terminate():
    pg.font.quit()
    pg.mixer.quit()
    pg.quit()
    sys.exit()


def draw_stars(screen):
    density = 4
    for x, y in itertools.product(range(density), range(density)):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pg.draw.circle(screen, WHITE, (x, y), 1)


def draw_health(screen, player_hp):
    max_hp = MAX_HP
    for i in range(player_hp):
        pg.draw.rect(screen, GREEN, (15, 5 + (10 * max_hp) - i * 10, 20, 10))
    for i in range(max_hp):
        pg.draw.rect(screen, WHITE, (15, 5 + (10 * max_hp) - i * 10, 20, 10), 1)


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    pg.display.set_caption(TITLE)

    player = PlayerShip(x=int(WIDTH * 0.05), y=HEIGHT // 2, img=IMAGES['player'], hp=MAX_HP)
    score_font = pg.font.SysFont('arial liberationsans', 14, True, False)

    pb_img = IMAGES['player_bullet']
    ebimg = IMAGES['enemy_bullet']
    enimg = IMAGES['enemy']
    points_img = IMAGES['points']
    expl_img = IMAGES['explosion']

    exp_sound = SOUNDS['explosion_sound']
    pb_sound = SOUNDS['laser']
    pickup_sound = SOUNDS['pickup_sound']

    enemies = []

    for _ in range(STARTING_ENEMIES):
        enemies.append(EnemyShip(x=WIDTH + 50, 
                        y=random.randint(50, HEIGHT - 50), 
                        img=enimg, hp=1))

    enemy_speed = 10

    volume = 0.5
    pg.mixer.music.play()
    pg.mixer.music.set_volume(volume)

    turn_dir = random.randint(1, 3)
    turn_range = random.randint(CENTERX - 80, CENTERX + 150)
    volume_diff = 0.2

    # main loop
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    player.fire_bullet(pb_img, pb_sound)
                elif event.key == K_RETURN:
                    if player.hp < 1:
                        player.revive(new_hp=3, img=IMAGES['player'])
                elif event.key == K_e:
                    volume += volume_diff
                    pg.mixer.music.set_volume(volume)
                elif event.key == K_r:
                    volume -= volume_diff
                    pg.mixer.music.set_volume(volume)
            elif event.type == MOUSEBUTTONDOWN:
                player.fire_bullet(pb_img, pb_sound)

        keys = pg.key.get_pressed()
        score_surf = score_font.render(f'Score: {player.score}', True, WHITE)
        score_rect = score_surf.get_rect()
        score_rect.center = (80, 30)

        if not pg.mixer.music.get_busy():
            pg.mixer.music.rewind()
            pg.mixer.music.play()

        if keys[K_w]:
            player.move(0, -PLAYERSPEED)
        if keys[K_s]:
            player.move(0, PLAYERSPEED)
        if keys[K_a]:
            player.move(-PLAYERSPEED, 0)
        if keys[K_d]:
            player.move(PLAYERSPEED, 0)

        player.update()

        # a big enemy for loop
        for enemy in enemies:
            enemy.move(-enemy_speed, 0)

            if enemy.x <= 0:
                enemies.remove(enemy)

            if enemy.img != points_img and enemy.x <= turn_range + random.randint(0, 150):
                enemy.fire_bullet(ebimg)

            if enemy.x < turn_range and enemy.img != points_img:
                if turn_dir == 1:
                    enemy.move(0, -enemy_speed)
                elif turn_dir == 2:
                    enemy.move(enemy_speed, 0)
                else:
                    enemy.move(0, enemy_speed)

            if enemy.img == points_img and player.rect.colliderect(enemy.rect) and player.img != expl_img and enemy in enemies:
                enemies.remove(enemy)
                player.score += random.randint(20, 40)
                pickup_sound.play()
                if player.hp < MAX_HP:
                    player.hp += 1

            if player.rect.colliderect(enemy.rect) and enemy.img != points_img:
                player.hp = 0

            enemy.update(player)

            for bullet in player.ammo:
                if bullet.rect.colliderect(enemy.rect) and enemy.img != points_img:
                    player.ammo.remove(bullet)
                    enemy.hp -= 1
                    if enemy.hp < 1:
                        exp_sound.play()
                        player.score += random.randint(10, 20)
                    turn_dir = random.randint(1, 3)
                    turn_range = random.randint(CENTERX - 80, CENTERX + 150)

        if len(enemies) < STARTING_ENEMIES:
            enemies.append(EnemyShip(WIDTH + 50, random.randint(50, HEIGHT - 50), img=enimg, hp=1))

        # drawing stuff
        screen.fill(BLACK)
        draw_stars(screen)

        player.draw(screen)

        for entity in itertools.chain(enemies, player.ammo):
            entity.draw(screen)

        for i in range(len(enemies) - 1, -1, -1):
            for eblt in enemies[i].ammo:
                eblt.draw(screen)

        draw_health(screen, player.hp)
        screen.blit(score_surf, score_rect)

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
