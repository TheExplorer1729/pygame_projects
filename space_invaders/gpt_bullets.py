import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
BULLET_SIZE = 10
BULLET_SPEED = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullets Shooting")

# Create the player
player = pygame.Rect((SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - PLAYER_SIZE), (PLAYER_SIZE, PLAYER_SIZE))

# Create a list to store the bullets
bullets = []

# Create a timer event to generate bullets
CREATE_BULLET_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_BULLET_EVENT, 1000)  # Generate bullets every 1 second (1000 milliseconds)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == CREATE_BULLET_EVENT:
            # Create a bullet at the player's position
            bullet = pygame.Rect(player.centerx - BULLET_SIZE // 2, player.top, BULLET_SIZE, BULLET_SIZE)
            bullets.append(bullet)

    keys = pygame.key.get_pressed()

    # Move the player left and right
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
        player.x += 5

    # Update bullet positions
    for bullet in bullets:
        bullet.y -= BULLET_SPEED

    # Remove bullets that go off-screen
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, RED, player)

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
