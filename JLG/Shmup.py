# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

#Starting by setting up the screen dimensions
WIDTH = 480
HEIGHT = 600
FPS = 60

#And setting up Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init() #revving up pygame
pygame.mixer.init() #revving up sounds
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmoop")
clock = pygame.time.Clock()
collision_time = 0
shoot_delay = 0
mercy = False

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale (player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.life = 3
        self.shootspeed = 100

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_w]:
            self.speedy = -8
        if keystate[pygame.K_s]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if mercy == True:
            self.image = pygame.transform.scale (hurt_img, (50, 38))
            self.image.set_colorkey(BLACK)
        else:
            self.image = pygame.transform.scale (player_img, (50, 38))
            self.image.set_colorkey(BLACK)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-5, 5)
        self.rot_speed = random.randrange(-8, 8)
        self.rot = 0
        self.last_update = pygame.time.get_ticks()
        self.maxhealth = int (self.rect.width / 10)
        self.health = self.maxhealth

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -30 or self.rect.right > WIDTH + 30:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 16)
        if self.health <= 0:
            self.kill

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale (bullet_img, (5, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        #if it reaches offscreen it dies
        if self.rect.bottom < 0:
            self.kill()


#Load game assets
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
hurt_img = pygame.image.load(path.join(img_dir, 'playerShip1_hurt.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png','meteorBrown_med1.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
#sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir,'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)



all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0
pygame.mixer.music.play(loops=-1)
# Game loop
running = True

while running:
    #keep loop running
    clock.tick(FPS)
    #inputs
    for event in pygame.event.get():
        #Check for closing window
        if event.type == pygame.QUIT:
                running = False
        #elif event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_SPACE:
                #player.shoot()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE] and pygame.time.get_ticks() - shoot_delay > player.shootspeed:
        player.shoot()
        shoot_delay = pygame.time.get_ticks()

    # Update
    all_sprites.update()
    #Check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits and mercy == False:
        player.life -= 1
        mercy = True
        collision_time = pygame.time.get_ticks()
    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        hit.health -= 1
        if hit.health <= 0:
            hit.kill()
            random.choice(expl_sounds).play()
            score += int(round(hit.maxhealth) * 10)
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)



    if mercy == True:
        if pygame.time.get_ticks() - collision_time > 3000:
            mercy = False

#    if Mob.health <= 0:
#        Mob.kill
#        m = Mob()
#        all_sprites.add(m)
#        mobs.add(m)

    if player.life <= 0:
        player.kill
        running = False

    #draw
    screen.fill (BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    #lastly, renew the screenpygame.display.flip()
    pygame.display.flip()

pygame.quit
