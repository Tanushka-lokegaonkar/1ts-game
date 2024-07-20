import pygame
import random
import sys

pygame.init()

screen_width=1000
screen_height=600

score = 0
player_lives = 3
font = pygame.font.Font(None,36)
game_over_font = pygame.font.Font(None,64)

background_image = pygame.image.load("plane/BG.png")
background_image = pygame.transform.scale(background_image,(screen_width,screen_height))
bg_x = 0
speed_increase_rate = 0
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Fighter Plane")

enemies=[]
player_bullets = []

class Character:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("assets/player1.png")
        self.img = pygame.transform.scale(self.img,(100,100))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.run_animation_count = 0
        self.img_list= ["plane/Fly (1).png","plane/Fly (2).png",
                        "plane/Fly (1).png",
                        "plane/Fly (2).png"]
        self.is_jump = False
        self.jump_count = 15
        self.is_duck = False
        self.duck_count = 15
        self.bullet_img = 'plane/Bullet (1).png'
        #self.plane_fire = 'plane/Shoot (2).png'

    def draw(self):
        self.rect.center = (self.x,self.y)
        screen.blit(self.img,self.rect)
    def run_animation_player(self):
        if(not self.is_jump):
            self.img = pygame.image.load(self.img_list[int(self.run_animation_count)])
            self.img = pygame.transform.scale(self.img,(100,100))
            self.run_animation_count+=0.5
            self.run_animation_count = self.run_animation_count%4
        if(not self.is_duck):
            self.img = pygame.image.load(self.img_list[int(self.run_animation_count)])
            self.img = pygame.transform.scale(self.img,(100,100))
            self.run_animation_count+=0.5
            self.run_animation_count = self.run_animation_count%4
    def jump(self):
        if (self.jump_count>-15):
            n=1
            if (self.jump_count<0):
                n=-1
            self.y -= ((self.jump_count**2)/10)*n
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.jump_count = 15
            self.y =300
    def duck(self):
        if (self.duck_count>-15):
            n=1
            if (self.duck_count<0):
                n=-1
            self.y += ((self.duck_count**2)/10)*n
            self.duck_count -= 1
        else:
            self.is_duck = False
            self.duck_count = 15
            self.y =300

    def shoot(self):
        bullet = Bullet(self.x+5,self.y-18,self.bullet_img)
        player_bullets.append(bullet)

class Enemy:
    def __init__(self,x,y):            #__init__ fixed function
        self.x = x
        self.y = y
        self.img = pygame.image.load("plane/enemy1.png")
        self.img = pygame.transform.scale(self.img,(75,75))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.run_animation_count = 0
        self.img_list= ["plane/enemy1.png","plane/enemy2.png",
                        "plane/enemy3.png"]

    def draw(self):
        self.rect.center = (self.x,self.y)
        screen.blit(self.img,self.rect)

    def run_animation_enemy(self):
        self.img = pygame.image.load(self.img_list[int(self.run_animation_count)])
        self.img = pygame.transform.scale(self.img,(100,100))
        self.run_animation_count+=0.5
        self.run_animation_count = self.run_animation_count%3

class Bullet:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img,(15,15))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
    
    def draw(self):
        self.rect.center = (self.x,self.y)
        screen.blit(self.img,self.rect)

    def move(self,vel):
        self.x +=vel

    def off_screen(self):
        return(self.x<=0 or self.x>=screen_width)

player = Character(100,386)
running=True
clock=pygame.time.Clock()

last_enemy_spawn_time = pygame.time.get_ticks()

while running:
    score+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.is_jump = True
            if event.key == pygame.K_RIGHT:
                player.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.is_duck = True
            if event.key == pygame.K_RIGHT:
                player.shoot()

    bg_x-=(10+speed_increase_rate)
    speed_increase_rate+=0.006
    if bg_x < -screen_width:
        bg_x = 0
    screen.blit(background_image,(bg_x,0))
    screen.blit(background_image,(screen_width+bg_x,0))

    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time >= 3000:
        if random.randint(0,100)<3:
            enemy_x1 = screen_width + 900
            enemy_y1 = random.randint(200,400)
            enemy1 = Enemy(enemy_x1,enemy_y1)
            enemy_x2 = enemy_x1 + 800
            enemy_y2 = random.randint(200,400)
            enemy2 = Enemy(enemy_x2,enemy_y2)
            enemies.append(enemy2)
            enemies.append(enemy1)
            last_enemy_spawn_time = current_time

    for enemy in enemies:
        enemy.x -= (15 + speed_increase_rate)
        enemy.draw()
        enemy.run_animation_enemy()

        if enemy.rect.colliderect(player.rect):  #collision1
            speed_increasing_rate = 0
            player_lives-=1
            enemies.remove(enemy)
        
        for bullet in player_bullets:              #collision2
            if pygame.Rect.colliderect(enemy.rect,bullet.rect):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                score+=10

    for bullet in player_bullets:
        if(bullet.off_screen()):
            player_bullets.remove(bullet)
        else:
            bullet.draw()
            bullet.move(10)

    if player_lives <= 0:
        game_over_text = game_over_font.render("Game over",True,(255,255,255))
        screen.blit(game_over_text,(screen_width//2 -120,screen_height//2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    live_text = font.render(f"Lives:{player_lives}",True,(0,0,0))
    screen.blit(live_text,(screen_width-120,10))
    score_text = font.render(f"Score:{score}",True,(0,0,0))
    screen.blit(score_text,(20,10))

    if player.is_jump:
        player.jump()
    if player.is_duck:
        player.duck()
    player.draw()
    player.run_animation_player()
    pygame.display.update()               
    clock.tick(30)                        

pygame.quit()