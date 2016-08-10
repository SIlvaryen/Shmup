import pygame, sys, random, os

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(imgFolder, 'spaceShip.png')).convert()
        self.image.set_colorkey(allColors['black'])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (screenSize[0] / 2, screenSize[1] / 4 * 3)

        self.health = 100
        self.maxHealth = 100

        self.speedx = 0
        self.speedy = 0

        self.speed = 5

        self.counterShoot = 0
        self.counterShootWhen = 4
        self.isShooting = False

        self.bullets = pygame.sprite.Group()

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -self.speed
        elif keystate[pygame.K_RIGHT]:
            self.speedx = self.speed
        if keystate[pygame.K_UP]:
            self.speedy = -self.speed
        elif keystate[pygame.K_DOWN]:
            self.speedy = self.speed

        #add Speed on keydown
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        #make sure player doesnt go off screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screenSize[0]:
            self.rect.right = screenSize[0]
        if self.rect.bottom > screenSize[1]:
            self.rect.bottom = screenSize[1]
        elif self.rect.top < 0:
            self.rect.top = 0

        if self.isShooting and self.counterShoot >= self.counterShootWhen:
            self.shoot()
            self.counterShoot = 0

        self.counterShoot += 1

    def shoot(self):
        bullet = Bullet(self)
        allSprites.add(bullet)
        self.bullets.add(bullet)
        random.choice(sounds.laserList).play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        self.width = 8
        self.height = 12

        self.image = pygame.image.load(os.path.join(imgFolder, 'bullet.png')).convert()
        self.image.set_colorkey(allColors['black'])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.speed = -10

        self.rect.bottom = player.rect.top - self.speed
        self.rect.centerx = player.rect.centerx

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom < 0:
            self.kill()

class EnemyShip(pygame.sprite.Sprite):
    amount = 1
    def __init__(self):
        super().__init__()

        self.width = 32
        self.height = 32

        self.image = pygame.image.load(os.path.join(imgFolder, 'enemySpaceShip.png')).convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(allColors['white'])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.left = random.randrange(0, screenSize[0] - self.rect.width)
        self.rect.bottom = 0

        self.speedx = 0
        self.speedy = random.randrange(4,8)

        self.counterShoot = 0
        self.counterShootWhen = 20

        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        #reset if out of screen
        if (self.rect.y > screenSize[1] + self.height) or \
        (self.rect.x < - self.width) or \
        (self.rect.x > screenSize[0] + self.width):
            self.reset()

        self.counterShoot += 1

        if self.counterShoot >= self.counterShootWhen:
            self.shoot()
            self.counterShoot = 0

    def shoot(self):
        eb = EnemyBullet(self)
        self.bullets.add(eb)
        allSprites.add(eb)

    def reset(self):
        self.rect.left = random.randrange(0, screenSize[0] - self.rect.width)
        self.rect.bottom = 0

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()

        self.height = 12
        self.width = 8

        self.image = pygame.image.load(os.path.join(imgFolder, 'enemyBullet.png')).convert()
        self.image.set_colorkey(allColors['black'])
        self.image = pygame.transform.rotate(self.image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.speed = 10

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.centery

    def update(self):
        self.rect.centery += self.speed

        if self.rect.top > screenSize[1]:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    amount = 10
    def __init__(self):
        super().__init__()

        self.image = random.choice(meteor_imgs)
        self.origImg = self.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.reset()

        self.speedx = random.randrange(3)
        if self.rect.centerx >= screenSize[0] / 2:
            self.speedx = -self.speedx
        self.speedy = random.randrange(2, 8)

        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.oldCenter = (0,0)

    def rotate(self):
        self.oldCenter = self.rect.center
        self.rot += self.rot_speed
        self.image = pygame.transform.rotate(self.origImg, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.oldCenter

    def update(self):
        if self.rect.top > screenSize[1] or self.rect.left > screenSize[0] or self.rect.right < 0:
            self.reset()

        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        self.rotate()

    def reset(self):
        self.rect.centerx = random.randrange(0, screenSize[0])
        self.rect.centery = random.randrange(-150, -100)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.frame = 0
        self.image = explosionAnim[self.size][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.lastUpdate = pygame.time.get_ticks()
        self.frameRate = 15

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frameRate > self.lastUpdate:
            self.lastUpdate = now
            self.frame += 1
            if self.frame >= len(explosionAnim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosionAnim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Background(pygame.sprite.Sprite):
    def __init__(self, y, speed):
        super().__init__()

        self.image = pygame.image.load(os.path.join(imgFolder, 'weltraum.png')).convert()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * screenSize[0] / self.rect.width), int(self.rect.height * screenSize[0] / self.rect.width)))
        self.rect = self.image.get_rect()

        self.speed = speed

        self.rect.left = 0
        self.rect.top = y

    def update(self):
        self.rect.centery -= self.speed
        if self.rect.bottom <= 0:
            self.rect.top = self.rect.height

    def render(self):
        surface.blit(self.image, self.rect.topleft)

class Score():
    def __init__(self):
        self.score = 0
        self.x = screenSize[0] / 2
        self.y = 20
        self.color = allColors['white']

    def render(self):
        drawText('Score: ' + str(self.score), self.color, self.x, self.y, 'mid', 32)

class HealthBar():
    def __init__(self, maxHealth):
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.percentageHealth = self.health / self.maxHealth

        self.x = 10
        self.y = 10

        self.width = 100
        self.height = 20

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.orgRect = self.rect.copy()

    def update(self, health):
        self.health = health

        if self.health <= 0:
            self.health = 0

        self.percentageHealth = self.health / self.maxHealth

        self.rect = pygame.Rect(self.x, self.y, int(self.percentageHealth * self.width), self.height)

    def render(self):
        pygame.draw.rect(surface, allColors['green'], self.rect)
        pygame.draw.rect(surface, allColors['white'], self.orgRect, 2)

class Sounds():
    def __init__(self):
        self.laserList = []
        self.explosionList = []
        for l in range(5):
            filename = os.path.join(sndFolder, 'laser{}.wav'.format(l))
            sound = pygame.mixer.Sound(filename)
            sound.set_volume(0.15)
            self.laserList.append(sound)

        for ex in range(3):
            filename = os.path.join(sndFolder, 'explosion{}.wav'.format(ex))
            sound = pygame.mixer.Sound(filename)
            sound.set_volume(0.3)
            self.explosionList.append(sound)

        self.bossIntro = os.path.join(sndFolder, 'BossIntro.mp3')
        self.menuMusic = os.path.join(sndFolder, 'RailJetSeamlessLoop.ogg')

def main():
    pygame.init()
    pygame.mixer.init()

    global allColors, surface, screenSize, clock, imgFolder, sndFolder, gameFolder, allSprites, bullets, meteor_imgs, score, sounds, explosionAnim

    allColors = {
    'black':   (   0,   0,   0),
    'white':   ( 255, 255, 255),
    'red':     ( 255,   0,   0),
    'lime':    (   0, 255,   0),
    'blue':    (   0,   0, 255),
    'yellow':  ( 255, 255,   0),
    'cyan':    (   0, 255, 255),
    'magenta': ( 255,   0, 255),
    'silver':  ( 192, 192, 192),
    'gray':    ( 128, 128, 128),
    'darkred': ( 128,   0,   0),
    'olive':   ( 128, 128,   0),
    'green':   (   0, 128,   0),
    'purple':  ( 128,   0, 128),
    'darkaqua':(   0, 128, 128),
    'navyblue':(   0,   0, 128)
    }

    screenSize = (480,640)
    FPS = 64

    surface = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('Shoot \'em up!')
    clock = pygame.time.Clock()

    imgFolder = os.path.join(os.path.dirname(__file__), 'img')
    sndFolder = os.path.join(os.path.dirname(__file__), 'snd')

    meteor_imgs = []
    meteor_list = ['meteor_big1.png', 'meteor_med1.png', 'meteor_small1.png']

    explosionAnim = {}
    explosionAnim['huge'] = []
    explosionAnim['large'] = []
    explosionAnim['small'] = []

    for meteor in meteor_list:
        meteor_imgs.append(pygame.image.load(os.path.join(imgFolder, meteor)))

    for ex in range(1,9):
        dirname = os.path.join(imgFolder, 'explosion_{}.png'.format(ex))
        img = pygame.image.load(dirname).convert()
        img.set_colorkey(allColors['white'])
        img_huge = pygame.transform.scale(img, (64, 64))
        img_large = pygame.transform.scale(img, (32, 32))
        img_small = pygame.transform.scale(img, (16, 16))
        explosionAnim['huge'].append(img_huge)
        explosionAnim['large'].append(img_large)
        explosionAnim['small'].append(img_small)

    sounds = Sounds()

    #start of the gameloop
    running = True
    isGameOver = True
    pausedGame = False
    while running:
        if isGameOver:
            gameOver()
            allSprites = pygame.sprite.LayeredUpdates()
            EnemyShips = pygame.sprite.Group()
            Meteors = pygame.sprite.Group()
            Backgrounds = pygame.sprite.Group()
            #-------------------------------------------------------------------------------
            #Creation of Instances and adding them to the groups
            score = Score()

            pygame.mixer.music.load(sounds.bossIntro)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(loops=-1)

            bg1 = Background(0, 8)
            bg2 = Background(bg1.rect.height, 8)
            allSprites.add(bg1,bg2)
            Backgrounds.add(bg1,bg2)

            for es in range(EnemyShip.amount):
                enemyShip = EnemyShip()
                EnemyShips.add(enemyShip)

            allSprites.add(EnemyShips)

            for m in range(Meteor.amount):
                meteor = Meteor()
                allSprites.add(meteor)
                Meteors.add(meteor)

            player = Player()
            allSprites.add(player.bullets)
            allSprites.add(player)
            healthBar = HealthBar(player.health)
            isGameOver = False
        #Declaring the Delay
        clock.tick(64)
        #Reacting on Player's input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.isShooting = True
                if event.key == pygame.K_p:
                    pausedGame = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_SPACE:
                    player.isShooting = False
        #Update Classes and Variables
        allSprites.update()
        healthBar.update(player.health)

        #Render Objects
        allSprites.draw(surface)
        score.render()
        healthBar.render()

        pygame.display.update()

        #Collisiondetection
        #player with enemyShips
        for es in EnemyShips:
            if pygame.sprite.collide_mask(player, es):
                random.choice(sounds.explosionList).play()
                expl = Explosion(midOfTwoRects(player, es),'huge')
                allSprites.add(expl)
                player.health -= 40
                es.kill()
        #player with meteors
        for m in Meteors:
            if pygame.sprite.collide_mask(player, m):
                random.choice(sounds.explosionList).play()
                expl = Explosion(midOfTwoRects(player, m),'large')
                allSprites.add(expl)
                player.health -= m.rect.width / 2
                m.kill()
        #bullets with bullets and enemyBullets with player
        for b in player.bullets:
            for es in EnemyShips:
                for eb in es.bullets:
                    if pygame.sprite.collide_mask(eb, b):
                        eb.kill()
                        b.kill()

                if pygame.sprite.collide_mask(b, es):
                    random.choice(sounds.explosionList).play()
                    expl = Explosion(es.rect.center,'large')
                    allSprites.add(expl)
                    es.kill()
                    b.kill()
                    score.score += 50

            for m in Meteors:
                if pygame.sprite.collide_mask(b, m):
                    random.choice(sounds.explosionList).play()
                    expl = Explosion(m.rect.center,'large')
                    allSprites.add(expl)
                    m.kill()
                    b.kill()
                    score.score += 50 - m.rect.width

        for es in EnemyShips:
            for eb in es.bullets:
                if pygame.sprite.collide_mask(player, eb):
                    random.choice(sounds.explosionList).play()
                    expl = Explosion(eb.rect.center,'small')
                    allSprites.add(expl)
                    player.health -= 5
                    eb.kill()

        Meteor.amount = 10 + int(score.score / 500)

        EnemyShip.amount = 1 + int(score.score / 2000)

        while len(Meteors) < Meteor.amount:
            meteor = Meteor()
            allSprites.add(meteor)
            Meteors.add(meteor)

        while len(EnemyShips) < EnemyShip.amount:
            eb = EnemyShip()
            allSprites.add(eb)
            EnemyShips.add(eb)

        if player.health <= 0:
            isGameOver = True

        if pausedGame == True:
            pauseGame()
            pausedGame = False

def midOfTwoRects(first, second):
    valX = int((first.rect.centerx + second.rect.centerx) / 2)
    valY = int((first.rect.centery + second.rect.centery) / 2)

    return (valX, valY)

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerInput():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

def pauseGame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_p:
                    return
        drawText('Game Paused!', allColors['white'], screenSize[0] / 2, screenSize[1] / 2, 'mid')
        pygame.display.update()

def gameOver():
    bg1 = Background(0, 2)
    bg2 = Background(bg1.rect.height, 2)

    pygame.mixer.music.load(sounds.menuMusic)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(loops=-1)

    background = pygame.sprite.Group()
    background.add(bg1, bg2)
    running = True

    counter = 200

    while running:
        clock.tick(64)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                else:
                    running = False
        background.update()

        background.draw(surface)

        drawText('SHMUP!', allColors['darkred'], screenSize[0] / 2, screenSize[1] / 4, 'mid')
        drawText('Move with your arrows!', allColors['white'], screenSize[0] / 2, screenSize[1] / 2, 'mid', 20)
        drawText('Shoot with space!', allColors['white'], screenSize[0] / 2, screenSize[1] / 4 * 3, 'mid', 20)
        pygame.display.update()

    pygame.mixer.music.fadeout(2000)

    while counter > 0:
        clock.tick(64)
        background.update()

        background.draw(surface)
        pygame.display.update()
        counter -= 1

def drawText(text, color, x, y, pos, size = 48):
    font = pygame.font.match_font('arial')
    font = pygame.font.Font(font, size)
    textobj = font.render(text, True, color)
    textRect = textobj.get_rect()

    if pos == 'mid':
        textRect.center = (x,y)
    elif pos == 'topleft':
        textRext.topleft = (x,y)
    elif pos == 'topright':
        textRect.topright = (x,y)
    elif pos == 'bottomleft':
        textRect.bottomleft = (x,y)
    elif pos == 'bottomright':
        textRext.bottomright = (x,y)
    else:
        print('something went wrong! your input was ' + pos)

    surface.blit(textobj, textRect)

main()
