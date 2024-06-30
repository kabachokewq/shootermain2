from pygame import *
from random import randint
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
wn = display.set_mode((700,500))
clock = time.Clock()
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700,500))
FPS = 60
font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,100)
score = 0
lose = 0

win_score = 10
lose_score = 10
class GameSprite(sprite.Sprite):
    def __init__(self,pl_image,pl_x,pl_y,size_x,size_y,pl_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.speed = pl_speed
        self.size_x = size_x
    def reset(self):
        wn.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        #[K_a,K_k]
        #назва списку[номер елементу]
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - self.size_x:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top,15,20, -5)
        bullets.add(bullet)
class Enemy(GameSprite):
    
    
    def update(self):
        global lose

        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(80,620)
            self.speed = randint(1,5)
            lose +=1

class Bullet(GameSprite):
    def update(self):
            self.rect.y += self.speed
            if self.rect.y < 0:
                self.kill()

monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(80,620),-50,80,50,randint(1,5))
    monsters.add(monster)
rocket = Player("rocket.png",305,400,80,100,10) 

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy("asteroid.png", randint(80,620),-50,80,50,randint(1,5))
    asteroids.add(asteroid)
 
bullets = sprite.Group()

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
    if not finish:
        wn.blit(background,(0,0))
        text_score = font1.render("Рахунок: " + str(score),1,(255,255,255))
        wn.blit(text_score,(10,20))
        text_lose = font1.render("Пропущено: " + str(lose),1,(255,255,255))
        wn.blit(text_lose,(10,50))
        rocket.reset()
        rocket.update()
        monsters.draw(wn)
        monsters.update()
        asteroids.draw(wn)
        asteroids.update()
        bullets.draw(wn)
        bullets.update()

        collide_monster_bullet = sprite.groupcollide(monsters,bullets,True,True)
        for collide in collide_monster_bullet:
            score +=1
            monster = Enemy("ufo.png", randint(80,620),-50,80,50,randint(1,5))
            monsters.add(monster)

        collide_asteroid_bullet = sprite.groupcollide(asteroids,bullets,True,True)
        for collide in collide_asteroid_bullet:
            score +=1
            asteroid = Enemy("asteroid.png", randint(80,620),-50,80,50,randint(1,5))
            asteroids.add(asteroid)
    if score >= win_score:
        finish = True
        win = font2.render("YOU WIN!" + str(lose),1,(1,233,1))
        wn.blit(win,(200,200))
        mixer.music.stop()
    if lose >= lose_score:
        finish = True
        win = font2.render("YOU LOSE!" + str(lose),1,(1,233,1))
        wn.blit(win,(200,200))
        mixer.music.stop()
    clock.tick(FPS)
    display.update()