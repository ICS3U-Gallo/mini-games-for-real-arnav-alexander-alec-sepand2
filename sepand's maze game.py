# pygame template   
import pygame

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock =pygame.display.clock()

# Define colors
GREEN = (16, 59, 29)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)
WHITE = (255, 255, 255)

# Define block size
BLOCK_SIZE = 40

# Define police and thief positions (just an example, can be changed)
police_positions = [(1, 1), (8, 5), (6, 8)]
thief_position = (4, 7)

# Maze layout (1 = path, 0 = wall)
maze_layout = [
    [1, 0, 0, 1, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 0, 1, 1]
]

# Exit position (bottom-right corner)
exit_position = (8, 8)

# Game loop
running = True
captured = False  # To track if the thief has been captured
while running:
    screen.fill(GREEN)  # Background color

    # Draw the maze
    for y in range(len(maze_layout)):
        for x in range(len(maze_layout[y])):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if maze_layout[y][x] == 1:
                pygame.draw.rect(screen, BLACK, rect)  # Wall
            else:
                pygame.draw.rect(screen, GREEN, rect)  # Path

    

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    pygame.time.Clock().tick(10)  # 10 frames per second

pygame.quit()
