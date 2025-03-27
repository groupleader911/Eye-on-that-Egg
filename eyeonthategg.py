import pygame
from pygame import mixer
from pygame.locals import *
import random
import asyncio

#making sound effects
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.font.init()

#first person shooter mode
clock = pygame.time.Clock()
fps = 60

#display scaling
screenwidth = 600
screenheight = 800


#loading sound effects
explosion_sound1 = pygame.mixer.Sound("./python/exps1.wav")
explosion_sound1.set_volume(0.25)

explosion_sound2 = pygame.mixer.Sound("./python/exps2.wav")
explosion_sound2.set_volume(0.25)

bulletsound = pygame.mixer.Sound("./python/lasersound.wav")
bulletsound.set_volume(0.25)



#global vars
rows = 5
cols = 5
husband_cooldown = 1000 #bullet cooldown (1 sec)
last_husband_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()

gameover = 0



#fonts
font3 = pygame.font.SysFont("Constantia", 30)
font4 = pygame.font.SysFont("Constantia", 40)

#setting up display
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Eye on that Egg")


#color
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

#setting images up for scaling
angrywife = pygame.image.load("./python/angrywife.PNG").convert_alpha()



#loaded images
background = pygame.image.load("./python/background.jpg")

colorblack = pygame.Surface(screen.get_size())
colorblack.fill((0, 0, 0))

def draw_background():
    #screen.blit(background, (0, -500))
    screen.blit(background, (0, 0))


#function for creating end-screen (creating text)
def text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))



# creating husband@wife
class Angrywife(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(angrywife, (75, 130))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.lastshot = pygame.time.get_ticks()
    
    def update(self):
        #movement speed
        speed = 8

        gameover = 0

        #setting bullet cooldown (ms)
        cooldown = 500

        #masking angrywife
        self.mask = pygame.mask.from_surface(self.image)


        #user input + movement
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_d] and self.rect.right < screenwidth:
            self.rect.x += speed
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screenwidth:
            self.rect.x += speed

        
        #recording time for limiting bullet shooting
        currenttime = pygame.time.get_ticks( )

        #user input for SHOOTING BULLET
        if key[pygame.K_SPACE] and currenttime - self.lastshot > cooldown:
            bullet = Egg(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.lastshot = currenttime
            bulletsound.play()
        
        #healthbar
        pygame.draw.rect(screen, red, ((self.rect.x + 5), (self.rect.bottom), self.rect.width, 12))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, ((self.rect.x + 5), (self.rect.bottom), int(self.rect.width * (self.health_remaining / self.health_start)), 12))
        elif self.health_remaining <= 0:
            explosion = Eggsplosion(self.rect.centerx, self.rect.centery, 5)
            explosion_group.add(explosion)
            self.kill()
            gameover = -1
        return gameover




#creating eggshell bullets
class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./python/goldenegg2.PNG")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        
        #deleting used bullets
        if self.rect.bottom < 0:
            self.kill()
        
        #collision checking
        if pygame.sprite.spritecollide(self, husband_group, True, pygame.sprite.collide_mask):
            self.kill()
            explosion_sound1.play()
            explosion = Eggsplosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)



#creating husbands
class Husband(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./python/husband2.PNG")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        #setting husband movement
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        
        self.mask = pygame.mask.from_surface(self.image)



#creating bullets for husbands
class Husband_bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./python/goldenegg2.PNG")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 3
        
        #deleting used bullets
        if self.rect.top > screenheight:
            self.kill()

        #angrywife collisions
        if pygame.sprite.spritecollide(self, sprite_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion_sound2.play()
            # reducing the ships health after bullet collision
            wife.health_remaining -= 1
            explosion = Eggsplosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)



class Eggsplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"./python/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (60, 60))
            if size == 4:
                img = pygame.transform.scale(img, (80, 80))
            if size == 5:
                img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    
    def update(self):
        explosion_speed = 5

        self.counter += 1
    
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #stoping animation after completion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


#create groups
sprite_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
husband_group = pygame.sprite.Group()
husband_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


#creating random husband positions
def create_husband():
    for row in range(rows):
        for item in range(cols):
            target = Husband(100 + item * 100, 100 + row * 85)
            husband_group.add(target)

create_husband()


#create player position and health
wife = Angrywife(int((screenwidth/2)), screenheight-100, 3)
sprite_group.add(wife)



run = True
while run:

    clock.tick(fps)

    #draw background
    draw_background()


    if countdown == 0:
        #drawing husband bullets (creating)
        # recording current time
        bullet_time = pygame.time.get_ticks()
        #shooting instance
        if bullet_time - last_husband_shot > husband_cooldown and len(husband_bullet_group) < 5 and len(husband_group) > 0:
            attacking_husband = random.choice(husband_group.sprites())
            husband_bullet = Husband_bullets(attacking_husband.rect.centerx, attacking_husband.rect.bottom)
            husband_bullet_group.add(husband_bullet)

            last_husband_shot = bullet_time

        
        if len(husband_group) == 0:
            gameover = 1
        
        if gameover == 0:
            #updating groups
            gameover= wife.update()


            bullet_group.update()
            husband_group.update()
            husband_bullet_group.update()
        elif gameover == -1:
            text('GAME OVER', font4, white, int(screenwidth/2 - 110), int(screenheight/2 + 200))
        elif gameover == 1:
            text('YOU WON', font4, white, int(screenwidth/2 - 110), int(screenheight/2 + 200))



    if countdown > 0:
        text('GET READY', font4, white, int(screenwidth/2 - 110), int(screenheight/2 + 150))
        text(str(countdown), font4, white, int(screenwidth/2 - 10), int(screenheight/2 + 200))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
    
    
    #updating explosion group 
    explosion_group.update()

    
    #drawing sprite groups
    explosion_group.draw(screen)
    sprite_group.draw(screen)
    bullet_group.draw(screen)
    husband_group.draw(screen)
    husband_bullet_group.draw(screen)


    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    pygame.display.update()


pygame.quit()