import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Asteroids")
icon = pygame.image.load('assets/images/ghost.png')
pygame.display.set_icon(icon)

# Spaceship
spaceshipImg = pygame.image.load('assets/images/ghost.png')
spaceshipX = screen_width / 2
spaceshipY = screen_height / 2
spaceship_angle = 0
spaceship_speed = 0
spaceship_rot_speed = 0

# Bullet
bulletImg = pygame.image.load('assets/images/slime.png')
bullets = []

# Asteroids
asteroidImg = pygame.image.load('assets/images/sun.png')
asteroids = []

for _ in range(5):
    asteroids.append({
        "x": random.randint(0, screen_width),
        "y": random.randint(0, screen_height),
        "dx": random.choice([-1, 1]) * random.uniform(1, 3),
        "dy": random.choice([-1, 1]) * random.uniform(1, 3)
    })

# Function to draw spaceship
def draw_spaceship(x, y, angle):
    rotated_image = pygame.transform.rotate(spaceshipImg, angle)
    new_rect = rotated_image.get_rect(center=spaceshipImg.get_rect(topleft=(x, y)).center)
    screen.blit(rotated_image, new_rect.topleft)

# Function to draw asteroids
def draw_asteroid(x, y):
    screen.blit(asteroidImg, (x, y))

# Function to draw bullets
def draw_bullet(x, y):
    screen.blit(bulletImg, (x, y))

# Function to move spaceship
def move_spaceship(x, y, angle, speed):
    radian_angle = math.radians(angle)
    x += speed * math.cos(radian_angle)
    y -= speed * math.sin(radian_angle)
    return x % screen_width, y % screen_height

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_rot_speed = 5
            if event.key == pygame.K_RIGHT:
                spaceship_rot_speed = -5
            if event.key == pygame.K_UP:
                spaceship_speed = 5
            if event.key == pygame.K_SPACE:
                radian_angle = math.radians(spaceship_angle)
                bullets.append({
                    "x": spaceshipX + spaceshipImg.get_width() / 2,
                    "y": spaceshipY + spaceshipImg.get_height() / 2,
                    "dx": 10 * math.cos(radian_angle),
                    "dy": -10 * math.sin(radian_angle)
                })

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship_rot_speed = 0
            if event.key == pygame.K_UP:
                spaceship_speed = 0

    spaceship_angle += spaceship_rot_speed
    spaceshipX, spaceshipY = move_spaceship(spaceshipX, spaceshipY, spaceship_angle, spaceship_speed)

    for bullet in bullets:
        bullet["x"] += bullet["dx"]
        bullet["y"] += bullet["dy"]
        if 0 <= bullet["x"] <= screen_width and 0 <= bullet["y"] <= screen_height:
            draw_bullet(bullet["x"], bullet["y"])
        else:
            bullets.remove(bullet)

    for asteroid in asteroids:
        asteroid["x"] += asteroid["dx"]
        asteroid["y"] += asteroid["dy"]
        asteroid["x"] %= screen_width
        asteroid["y"] %= screen_height
        draw_asteroid(asteroid["x"], asteroid["y"])

    draw_spaceship(spaceshipX, spaceshipY, spaceship_angle)
    pygame.display.update()
