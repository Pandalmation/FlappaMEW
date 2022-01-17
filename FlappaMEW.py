import pygame
import math
import random
import sys
from pygame.locals import *
from pygame import mixer
 
#initialize the pygame and mixer
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
 
#create screen
screen_width = 512
screen_height = 384
screen = pygame.display.set_mode((screen_width, screen_height))
 
#load sounds
music = pygame.mixer.music.load(r'C:\Users\tiffa\Downloads\BINUS stuff\CS stuff\First year\Assignments-Repository\final/rick.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

ping_fx = pygame.mixer.Sound(r'C:\Users\tiffa\Downloads\BINUS stuff\CS stuff\First year\Assignments-Repository\final/ping.wav')
ping_fx.set_volume(0.05)
 
oof_fx = pygame.mixer.Sound(r'C:\Users\tiffa\Downloads\BINUS stuff\CS stuff\First year\Assignments-Repository\final/oof.wav')
oof_fx.set_volume(0.15)
 
bonk_fx = pygame.mixer.Sound(r'C:\Users\tiffa\Downloads\BINUS stuff\CS stuff\First year\Assignments-Repository\final/bonk.wav')
bonk_fx.set_volume(0.05)
 
 
#keeps track of time + frames per second
clock = pygame.time.Clock()
fps = 60
 
#Title of the game
pygame.display.set_caption('FlappaMEW')
 
#game vars
bgscroll = 0
scrollspeed = 2
flying = False
gameover = False
shoot = False
rows = 3
columns = 5
enemyCD = 400 #bullet cooldown in milliseconds
lastenemyshot = pygame.time.get_ticks()
 
 
#colors
red = (255, 0, 0)
green = (0, 255, 0)
 
 
#load images
background_img= pygame.image.load(r'C:\Users\tiffa\Downloads\BINUS stuff\CS stuff\First year\Assignments-Repository\final/noon.png')
button_img= pygame.image.load(r'C:\Users\tiffa\Downloads\BINUS stuff\CS stuff\First year\Assignments-Repository\final/retry.png')
button_img= pygame.transform.scale(button_img, (70, 35))
heartprojectile_img= pygame.image.load(r'C:\Users\tiffa\Downloads\BINUS stuff\CS stuff\First year\Assignments-Repository\final/heart.png')
heartprojectile_img= pygame.transform.scale(heartprojectile_img, (15,15))
shurikenprojectile_img= pygame.image.load(r'C:\Users\tiffa\Downloads\BINUS stuff\CS stuff\First year\Assignments-Repository\final/shuriken.png')
shurikenprojectile_img= pygame.transform.scale(shurikenprojectile_img, (15,15))
 
#class for Mew Sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, shootCD, ammo, health):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] #create an empty list
        self.index = 0  #tells which picture from the list would be showed 
        self.counter = 0 #controls the speed of which the animation runs
        for num in range(1,109):
            img = pygame.image.load(f'C:\\Users\\tiffa\\Downloads\\BINUS stuff\\CS stuff\\First year\\Assignments-Repository\\final\\mew/mew-{num}.png') #loada the images from 1 - 108
            self.images.append(img) #images gets appended into the empty list
        self.image = self.images[self.index] #image contains the list of images appended with the index
        self.rect = self.image.get_rect() #gets the rectangle of the image
        self.rect.center = [x,y] #intialize the center of the rectangle
        self.vel = 0 #starts with 0 velocity
        self.shootCD = 0 #starts with 0 shoot cooldown
        self.ammo = ammo #the ammo MEW contains
        self.healthstart = health #how much health it starts with
        self.healthremaining = health #how much health remians
        self.clicked = False #registers click as false first
    
    def update(self):
        global gameover
        if self.shootCD > 0:
            self.shootCD -= 1
 
        if flying == True:
            #gravity
            self.vel += 0.25
            if self.vel > 4:
                self.vel = 4
            if self.rect.bottom < 375:
                self.rect.y += int(self.vel)
       
        if gameover == False:
 
            #draw health bar
            pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 7), self.rect.width, 8))
            if self.healthremaining > 0:
                pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 7), int(self.rect.width * (self.healthremaining / self.healthstart)), 8))
            elif self.healthremaining <= 0:
                explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
                explosiongroup.add(explosion)
                self.kill()
                gameover = True

 
            #if mouse clicked, fly will occur
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked== False:
                self.clicked = True
                self.vel = -5
            #if no mouse clicks then it will continue to drop
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
           
            #update mask
            self.mask = pygame.mask.from_surface(self.image)
           
            #animation
            self.counter += 1
            flyCD = 3
 
            if self.counter > flyCD:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
 
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90) #rotates the image


    def shoot(self):
        if self.shootCD == 0 and self.ammo > 0:
            self.shootCD = 50  #shootcooldown
            projectile = Projectile(self.rect.centerx + (0.6 * self.rect.size[0]), self.rect.centery) #position of where the projectile starts to come from
            projectilegroup.add(projectile)
 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range (1,12):
            img= pygame.image.load(f'C:\\Users\\tiffa\\Downloads\\BINUS stuff\\CS stuff\\First year\\Assignments-Repository\\final\\explode/explosion-{num}.png')
            if size == 1:
                img= pygame.transform.scale(img, (20,20))
            if size == 2:
                img= pygame.transform.scale(img, (40,40))
            if size == 3:
                img= pygame.transform.scale(img, (80,80))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
   
    def update(self):
        explosion_speed = 3
        self.counter+= 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        #if animation is complete, explosion will be deleted
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill() 
 
 
class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"C:\\Users\\tiffa\\Downloads\\BINUS stuff\\CS stuff\\First year\\Assignments-Repository\\final\\enemy/enem-" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_counter = 0
        self.move_direction = 1
 
     
    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.image = heartprojectile_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        #move bullet
        self.x = 2
        self.rect.x += (self.x * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        if pygame.sprite.spritecollide(self, enemygroup, True):
            self.kill()
            ping_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosiongroup.add(explosion)
 
class EnemyProjectiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = shurikenprojectile_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
    def update(self):
        #move bullet
        self.rect.x -= 5
        #check if bullet has gone off screen
        if self.rect.right > screen_width:
            self.kill()
        if pygame.sprite.spritecollide(self, mew_group, False, pygame.sprite.collide_mask):
            self.kill()
            oof_fx.play()
            #reduce mew health
            Mew.healthremaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosiongroup.add(explosion)
 
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
 
    def draw(self):
 
        action = False
 
        #get mouse position
        position = pygame.mouse.get_pos()
        #check if mouse over button
        if gameover == True:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            if self.rect.collidepoint(position):
                if pygame.mouse.get_pressed()[0] == 1:
                    action = True
        return action
 
   
button = Button(screen_width // 2 - 40, screen_height // 2 - 20, button_img)
 
#sprite groups
mew_group = pygame.sprite.Group()
Mew = Sprite(50, int(screen_height/2), 0, math.inf, 5)
mew_group.add(Mew)
enemygroup = pygame.sprite.Group()
enemyprojectilesgroup = pygame.sprite.Group()
projectilegroup = pygame.sprite.Group()
explosiongroup = pygame.sprite.Group()
 
def createEnemies():
    for column in range(columns):
        for item in range(rows):
            enemy = Enemies(300 + item * 80, 65 + column * 70) #position of enemy sprites
            enemygroup.add(enemy)
 
createEnemies()

     
def resetgame():
    Mew.rect.x = 20
    Mew.rect.y = int(screen_height/2 - 20)
    Mew.healthremaining = Mew.healthstart
    

    action = False
    while gameover == True:
        if pygame.mouse.get_pressed()[0] == 1:
            action = True
            
    return action
     
 
run = True
while run:
 
    clock.tick(fps)
   
    #draw background
    screen.blit(background_img, (bgscroll, 0))
 
    time_now = pygame.time.get_ticks()
    #create random bullets
    if time_now - lastenemyshot > enemyCD:
        attackingenemy = random.choice(enemygroup.sprites())
        shuriken_projectile = EnemyProjectiles(attackingenemy.rect.centerx, attackingenemy.rect.top)
        enemyprojectilesgroup.add(shuriken_projectile)
        lastenemyshot = time_now
 
    mew_group.update()
    mew_group.draw(screen)
 
    projectilegroup.update()
    projectilegroup.draw(screen)
   
    enemygroup.update()
    enemygroup.draw(screen)
 
    enemyprojectilesgroup.update()
    enemyprojectilesgroup.draw(screen)
 
    explosiongroup.update()
    explosiongroup.draw(screen)
 
    if Mew.rect.top < -40:
        gameover = True
        flying = False
 
    #check if mew hit ground
    if Mew.rect.bottom > 375:
        gameover = True
        flying = False
    else:
        if shoot:
            Mew.shoot()
 
    if gameover == False:
        bgscroll -= scrollspeed
        if abs(bgscroll) > 512:
            bgscroll = 0
 
    #check for gameover and reset
    if gameover == True:
        if button.draw() == True:
            gameover = False
            resetgame()
            
    #controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True
        #key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot = True 
                bonk_fx.play()
            if event.key == pygame.K_r:
                resetgame()
        #key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shoot = False
 
       
    pygame.display.update()
 
pygame.quit()
