import pygame
import random

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

# Clock
clock = pygame.time.Clock()

# Title and icon
pygame.display.set_caption("Moja gra")
icon = pygame.image.load("ikona.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("kosmos.png")

# Player
playerImg = pygame.image.load("statek4.png")
playerX = 370
playerX_change = 0
playerX_speed = 2
playerY = 480

# Enemy
enemyImg = pygame.image.load("ufo2.png")
enemyX = []
enemyX_change = []
enemyX_speed = 2
enemyY = []
enemyY_change = 40
number_of_enemies = 5
dead_enemies = 0

for _ in range(number_of_enemies):
    enemyX.append(random.randint(50,750))
    enemyY.append(random.randint(50,100))
    enemyX_change.append(enemyX_speed)

# Bullet
bulletImg = pygame.image.load("pocisk.png")
bulletX = 0
bulletY = 480
bulletY_change = 0
bulletY_speed = 20 # 5
bulletY_change = bulletY_speed
bullet_state = "ready"

# Score
font = pygame.font.Font("freesansbold.ttf", 32)
font_game_over = pygame.font.Font("freesansbold.ttf", 100)
points = 0

def show_score(sc, en):
    score = font.render("Score: " + str(sc), True, (255, 255, 255))
    enemies = font.render("Aliens: " + str(en), True, (255, 255, 255))
    screen.blit(score, (20, 20))
    screen.blit(enemies, (600, 20))

def game_over():
    over = font_game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (80, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def bullet(x, y, s):
    if s == "fire":
        screen.blit(bulletImg, (x, y))

def isCollision(x1, y1, x2, y2):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    if distance < 32: # 40?
        return True
    else:
        return False

# Main game loop
running = True
game_on = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
# Shot
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready" and game_on:
                    bullet_state = "fire"
                    bulletX = playerX + 16
                    bulletY = playerY - 30
                # print("ciu ciu ciu")
# Close
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                running = False
# Movement
    keys=pygame.key.get_pressed()
    playerX_change = 0
    if keys[pygame.K_LEFT]:
        playerX_change -= playerX_speed
    if keys[pygame.K_RIGHT]:
        playerX_change += playerX_speed
# Player movement
    playerX += playerX_change
# Checking if the player is at the screen boundary
    if playerX > 736: playerX = 736;
    if playerX < 0: playerX = 0;
# Bullet movement
    bulletY -= bulletY_change
# Checking if the bullet is at the screen boundary
    if bulletY < 0:
        bullet_state = "ready"
# Checking if the bullet hit the enemy
    for i in range(number_of_enemies):
        if isCollision(bulletX, bulletY, enemyX[i]+16, enemyY[i]+16) and bullet_state == "fire":
            bullet_state = "ready"
            enemyX[i] = random.randint(50,750)
            enemyY[i] = random.randint(50,100)
            points += 1
            dead_enemies += 1
            # print(points)
# Player movement
# Checking if the enemy is at the screen boundary
    for i in range(number_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 736:
            enemyX[i] = 736;
            enemyX_change[i] = -enemyX_speed
            enemyY[i] += enemyY_change
        if enemyX[i] < 0:
            enemyX[i] = 0;
            enemyX_change[i] = enemyX_speed
            enemyY[i] += enemyY_change
# Checking if GAME is OVER
        if enemyY[i] > 440:
            game_on = False
            enemyX_speed = 0
            break


# New enemy
    if dead_enemies >= 10:
        dead_enemies = 0
        enemyX.append(random.randint(50,750))
        enemyY.append(random.randint(50,100))
        enemyX_change.append(enemyX_speed)
        number_of_enemies += 1
        enemyY_change += 5

    # RGB - Red, Green, Blue
    # screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    if game_on:
        player(playerX, playerY)
        for i in range(number_of_enemies): enemy(enemyX[i], enemyY[i])
        bullet(bulletX, bulletY, bullet_state)
    else:
        game_over()
    show_score(points, number_of_enemies)
    pygame.display.update()
