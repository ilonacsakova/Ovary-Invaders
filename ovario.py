import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()
pygame.mixer.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

#set timer
pygame.time.set_timer ( pygame.USEREVENT , 1000 )

# Background sound
pygame.mixer.music.load('green techno.mp3')

# Create title and icon
pygame.display.set_caption("Ovary Invaders 2.0")
icon = pygame.image.load('reproductive-system.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('ovaries.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('anna.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# bullets
bulletImg = pygame.image.load('heart.png')
bulletX = 0
bulletY = 480
bulletY_change = -0.9
bullet_state = "ready"

# cross
crossImg = []
crossX = []
crossY = []
crossY_change = []
cross_state = "chill"
num_of_crosses = 6

for i in range(num_of_crosses):
    crossImg.append(pygame.image.load('cross.png'))
    crossX.append(random.randint(0, 735))
    crossY.append(random.randint(50, 150))
    crossY_change.append(0.8)
    # cross_state.append("chill")

# time count
seconds = 0

# score
score_value = 0
font = pygame.font.Font('The Macabre.otf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('Another Danger - Demo.otf', 64)
win_font = pygame.font.Font('Another Danger - Demo.otf', 32)


def show_score(x, y):
    score = font.render("Score : " + str(score_value) + "         Get 10 points and don´t let Anka get you!             Use arrows and space.", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("RIGHTS LOST :(", True, (105, 0, 0))
    screen.blit(over_text, (300, 400))


def winner_text():
    win_text = win_font.render("YOU WON! NOW GO MASTURBATE!", True, (255, 100, 100))
    screen.blit(win_text, (120, 270))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


#def cross(x, y, i):
 #   screen.blit(crossImg[i], (x, y))


def show_fire_cross(x, y):
    global cross_state
    cross_state = "fire"
    screen.blit(crossImg[i], (crossX[i], crossY[i]))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def isDamage(playerX, playerY, crossX, crossY):
    distance = math.sqrt((math.pow(playerX - crossX, 2)) + (math.pow(playerY - crossY, 2)))
    if distance < 27:
        return True
    else:
        return False

pygame.mixer.music.play(-1)

# Game loop
running = True
while running:

    # colour RGB
    screen.fill((50, 50, 50))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if R or L
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_state = "fire"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
        if event.type == pygame.USEREVENT:
            seconds += 1
            if cross_state is "chill":
                crossX[i] = enemyX[i]
                show_fire_cross(crossX[i], crossY[i])
                cross_state = "fire"

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change


    for i in range(num_of_enemies):

        #cross(enemyX[i], enemyY[i], i)
        # win
        if score_value == 10:
            winner_text()
            break

        # Game over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]



        # Collison
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # damage
        damage = isDamage(playerX, playerY, crossX[i], crossY[i])
        if damage:
            crossY[i] = enemyY[i]
            cross_state = "chill"
            score_value -= 1
            playerX = 370
            playerY = 480

        # cross movement
        if seconds % 2 == 0:
            crossY[i] = enemyY[i]
            crossX[i] = enemyX[i]
            cross_state = "chill"
        if cross_state is "fire":
            show_fire_cross(crossX[i], crossY[i])
            crossY[i] += crossY_change[i]

        enemy(enemyX[i], enemyY[i], i)







    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
