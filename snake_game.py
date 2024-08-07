import pygame
import random

pygame.mixer.init()

pygame.init()

white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width,screen_height))

bgimg1 = pygame.image.load("snake/image1.png")
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()
bgimg2 = pygame.image.load("snake/image2.png")
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()
bgimg3 = pygame.image.load("snake/image3.png")
bgimg3 = pygame.transform.scale(bgimg3, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.Font(None,36)

def text_screen(text, color, x, y):
    screen_text = font.render(text,True, color)
    gameWindow.blit(screen_text, (x,y))

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, red, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        # gameWindow.fill((233,210,229))
        # text_screen("Welcome to Snakes", black, 260, 250)
        # text_screen("Press Space Bar To Play", black, 232, 290)
        gameWindow.blit(bgimg1, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()
        pygame.display.update()
        clock.tick(60)

#game loop
def gameloop():
    #game variable
    exit_game = False
    game_over = False 
    snake_x = 45
    snake_y = 55
    init_velocity = 5
    velocity_x = 0
    velocity_y = 0
    snake_size = 10
    snk_list = []
    snk_len = 1
    with open("highscore.txt","r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    score = 0
    fps = 60

    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            # gameWindow.fill(white)
            # text_screen("Game over! Press Enter To Continue", red, 100, 250)
            gameWindow.blit(bgimg3, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x += init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x -= init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y -= init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y += init_velocity
                        velocity_x = 0
                    
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x)<8 and abs(snake_y-food_y)<8:
                score += 10
                food_x = random.randint(20,screen_width/2)
                food_y = random.randint(20,screen_height/2)
                pygame.mixer.music.load('snake/bonus.wav')
                pygame.mixer.music.play()
                snk_len += 10
                if score > int(highscore):
                    highscore = score

            #gameWindow.fill(black)
            gameWindow.blit(bgimg2, (0,0))
            text_screen(f"High Score:{highscore}   Score:{score} ", white, 5, 5)
            #text_screen("Score: " + str(score * 10), red, 5, 5)
            pygame.draw.circle(gameWindow, white, (food_x, food_y), 7.0)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
        
            if len(snk_list)>snk_len:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('snake/hit.wav')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('snake/hit.wav')
                pygame.mixer.music.play()
            plot_snake(gameWindow, red, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()