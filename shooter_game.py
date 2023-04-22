# Створи власний Шутер!

from pygame import *
from random import randint
from time import


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        # TODO Написати управління гравцем для руху в сторони (ширина гравця 80 px)
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed
        if keys[K_RIGHT] and self.rect.x < width - 85:
            self.rect.x = self.rect.x + self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-7,
                        self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(0, width-85)
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -50:
            self.kill()

class statistics:
    def __init__(self, st_point_win=0, st_point_losse=0, duration=0, level=0):
        self._st_point_win = st_point_win
        self._st_point_losse = st_point_losse
        self._duration = duration
        self._level = level

    def __repr__(self):
        return f'{self._st_point_win}, {self._st_point_losse}, {self._duration}, {self._level}'

def save_statisties(filename):
    with open(filename, 'w', encoding='UTF-8') as f:
        for row in stat:
            f.write(str(row)+ '\n')

font.init()
text1 = font.Font(None, 36)
text2 = font.Font(None, 80)

# TODO Напис виграв та напис програв. Описати новий шрифт (80 px)
win = text2.render("YOU WIN!", True, (0, 255, 0))
lose = text2.render("ENEMY WIN!", True, (255, 0, 0))


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

img_back = "galaxy.jpg"
img_player = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"



width, height = 700, 500

window = display.set_mode((width, height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (width, height))

# Sprites
player = Player(img_player, 250, height-100, 80, 100, 10)  # ! Описати


clock = time.Clock()
FPS = 30


game = True
finish = False
lost = 0
score = 0
goal = 10
max_lost = 3
level = 1
file_start = "game_start.txt"

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(0, width-85), 0, 80, 40, randint(1, 5))
    monsters.add(monster)

stat = []

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if level < 1:
        game = False
    if not finish:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
    if level == 1:
        for collide in collides:
            score += 1
            monster = Enemy(img_enemy, randint(0, width-85), 0, 80, 40, randint(1, 5))
            monsters.add(monster)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for coliide in collides:
            score += 1
            monster = Enemy(img_enemy, randint(0, width-85), 0, 80, 40, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text_score = text1.render("Рахунок: "+str(score), 1, (3, 9, 9), (1, 116, 225))
        window.blit(text_score, (10, 20))
        text_level = text1.render("Уровень: "+str(level), 1, (3, 9, 9), (1, 116, 225))
        window.blit(text_level, (300, 20))
        # TODO текст для пропущених ворогів і промалювати

        text_lost = text1.render("Пропущено: "+str(lost), 1, (3, 9, 9), (1, 116, 225))
        window.blit(text_lost, (10, 50))

        display.update()
    else:
        stat.append(statistics(score, lost, level))
        finish = False
        score = 0
        lost = 0
        level += 1
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(0, width-85),0, 80, 40, randint(1, 5))
            monsters.add(monster)

    clock.tick(FPS)


save_statisties(file_start)