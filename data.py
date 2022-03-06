import pygame as pg
import os

MUSIC = pg.mixer.music.load(os.path.join('music', 'Mercury.ogg'))

IMAGES = {
    'player': pg.image.load(os.path.join('gfx', 'player.png')),
    'enemy': pg.image.load(os.path.join('gfx', 'enemy.png')),
    'player_bullet': pg.image.load(os.path.join('gfx', 'player_bullet.png')),
    'enemy_bullet': pg.image.load(os.path.join('gfx', 'enemy_bullet.png')),
    'points': pg.image.load(os.path.join('gfx', 'points.png')),
    'explosion': pg.image.load(os.path.join('gfx', 'explosion.png'))
}


SOUNDS = {
    'enemy_laser': pg.mixer.Sound(os.path.join('sound', 'enemy_laser.ogg')),
    'explosion_sound': pg.mixer.Sound(os.path.join('sound', 'explosion.ogg')),
    'laser': pg.mixer.Sound(os.path.join('sound', 'laser.ogg')),
    'pickup_sound': pg.mixer.Sound(os.path.join('sound', 'pickup.ogg'))
}
