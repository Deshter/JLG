import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")

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
mercy = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale (player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.life = 3

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

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale (meteor_img, (40, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 16)

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
meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()
    #Check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits and mercy == False:
        player.life -= 1
        mercy = True
        collision_time = pygame.time.get_ticks()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    if mercy == True:
        if pygame.time.get_ticks() - collision_time > 3000:
            mercy = False

    if player.life <= 0:
        player.image.fill(BLACK)
        running = False

    #draw
    screen.fill (BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    #lastly, renew the screenpygame.display.flip()
    pygame.display.flip()

pygame.quit
