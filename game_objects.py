from constants import WIDTH, HEIGHT, MAX_BULLETS, BULLETS_PER_ENEMY
from data import IMAGES, SOUNDS


class Ship:
    __slots__ = ('x', 'y', 'img', 'ammo', 'hp')
    def __init__(self, x, y, img, hp):
        self.x = x
        self.y = y
        self.img = img
        self.hp = hp
        self.ammo = []

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self, dx, dy):
        if self.hp > 0:
            self.x += dx
            self.y += dy

    def __repr__(self):
        return f"Ship(x={self.x}, y={self.y}, img={self.img})"

    def __str__(self):
        return f"Ship(x={self.x}, y={self.y}, img={self.img})"


class PlayerShip(Ship):
    __slots__ = ('rect', 'score')
    def __init__(self, x, y, img, hp):
        super().__init__(x, y, img, hp)
        self.rect = self.img.get_rect()
        self.score = 0

    def update(self):
        width = self.img.get_width()
        height = self.img.get_height()
        bullet_speed = 12

        self.rect.x = self.x
        self.rect.y = self.y

        if self.y <= 0:
            self.y = 0
        if self.y >= HEIGHT - height:
            self.y = HEIGHT - height
        if self.x <= 0:
            self.x = 0
        if self.x >= WIDTH - width:
            self.x = WIDTH - width
            
        for bullet in self.ammo:
            bullet.x += bullet_speed
            if bullet.x >= WIDTH:
                self.ammo.remove(bullet)
            bullet.update()

        if self.hp < 1:
            self.img = IMAGES['explosion']
            self.score = 0


    def fire_bullet(self, bimg, bsound):
        if len(self.ammo) < MAX_BULLETS and self.hp > 0:
            bullet = Bullet(self.x + 10, self.y, bimg)
            self.ammo.append(bullet)
            bsound.play()
        else:
            return None

    def revive(self, new_hp, img):
        self.hp = new_hp
        self.img = img


class EnemyShip(Ship):
    __slots__ = ('rect',)
    def __init__(self, x, y, img, hp):
        super().__init__(x, y, img, hp)
        self.rect = self.img.get_rect()

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self, player):
        ebul_speed = 20
        ex_img = IMAGES['explosion']
        self.rect.x = self.x
        self.rect.y = self.y

        for ebullet in self.ammo:
            ebullet.update()
            ebullet.x -= ebul_speed
            if ebullet.x < 0:
                self.ammo.remove(ebullet)

            elif ebullet.rect.colliderect(player.rect) and player.img != ex_img:
                self.ammo.remove(ebullet)
                player.hp -= 1
                SOUNDS['enemy_laser'].play()

        if self.hp < 1:
            self.img = IMAGES['points']


    def fire_bullet(self, bimg):
        if len(self.ammo) < BULLETS_PER_ENEMY and self.hp > 0:
            bullet = Bullet(self.x - 10, self.y, bimg)
            self.ammo.append(bullet)


class Bullet:
    __slots__ = ('x', 'y', 'img', 'rect')
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rect = self.img.get_rect()

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
