# pygame template   



import pygame
import random

# Initialize Pygame
pygame.init()


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


GREEN = (16, 59, 29)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)
WHITE = (255, 255, 255)

# block size
BLOCK_SIZE = 40

#  police positions blocking some of the enteries 
police_positions = [(1, 1), (8, 5), (6, 8)]

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

# Exit position 
exit_position = (8, 8)

# Get a random valid position for the thief
valid_positions = []
for y in range(len(maze_layout)):
    for x in range(len(maze_layout[y])):
        if maze_layout[y][x] == 1:  # It's a valid path
            valid_positions.append((x, y))

# Randomly choose the thief's starting position
thief_position = random.choice(valid_positions)

# Game loop
running = True
captured = False  # To track if the thief has been captured
while running:
    screen.fill(GREEN)  # Background color

    # Draw the maze
    for y in range(len(maze_layout)):
        for x in range(len(maze_layout[y])):
            wall = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if maze_layout[y][x] == 1:
                pygame.draw.rect(screen, BLACK, wall)  # Path (black)
            else:
                pygame.draw.rect(screen, GREEN, wall)  # Wall (green)

    # thief (grey square)
    thief_rect = pygame.Rect(thief_position[0] * BLOCK_SIZE, thief_position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, GREY, thief_rect)

    #  police (blue and red squares)
    for pos in police_positions:
        police_block = pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, BLUE, police_block)  # Blue square
        pygame.draw.rect(screen, RED, police_block.inflate(-10, -10))  # Red inside blue square
        if police_block.colliderect(thief_rect):  # checks to see if the grey block and the police block collides or not 
            print("YOU GOT CAPTURED!")
            captured = True

    #  the exit
    exit_block = pygame.Rect(exit_position[0] * BLOCK_SIZE, exit_position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, WHITE, exit_block)  # Exit (white square)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not captured:
            
            x, y = thief_position
            if event.key == pygame.K_LEFT and x > 0 and maze_layout[y][x - 1] == 1:
                thief_position = (x - 1, y)
            elif event.key == pygame.K_RIGHT and x < len(maze_layout[0]) - 1 and maze_layout[y][x + 1] == 1:
                thief_position = (x + 1, y)
            elif event.key == pygame.K_UP and y > 0 and maze_layout[y - 1][x] == 1:
                thief_position = (x, y - 1)
            elif event.key == pygame.K_DOWN and y < len(maze_layout) - 1 and maze_layout[y + 1][x] == 1:
                thief_position = (x, y + 1)

    

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    pygame.time.Clock().tick(10)  # 10 frames per second

pygame.quit()
