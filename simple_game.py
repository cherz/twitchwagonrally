import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Game")

# Player properties
player_width = 50
player_height = 50
player_x = 0
player_y = SCREEN_HEIGHT // 2 - player_height // 2
player_speed = 5

# Finish line
finish_line_x = SCREEN_WIDTH - 20

# Clock for frame rate control
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Clear the screen with a white background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls (Arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    # Keep player within screen bounds
    player_x = max(0, min(player_x, SCREEN_WIDTH - player_width))

    # Check for win condition
    if player_x + player_width >= finish_line_x:
        screen.fill(GREEN)  # Fill the screen with green
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # Draw the player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # Draw the finish line
    pygame.draw.line(screen, BLACK, (finish_line_x, 0), (finish_line_x, SCREEN_HEIGHT), 5)

    # Update the screen
    pygame.display.flip()

    # Frame rate control
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()

