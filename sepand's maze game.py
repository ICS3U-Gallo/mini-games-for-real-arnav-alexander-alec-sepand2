# pygame template   



import pygame
import random

# Initialize Pygame
pygame.init()


WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
police_positions = [(0, 4), (8, 5), (6, 7)]

# Maze layout (1 = path, 0 = wall)idea came from  "Coding Games With Pygame Zero & Python"
maze_layout = [
    [1, 0, 0, 1, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1],
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
        if maze_layout[y][x] == 1 and maze_layout != exit_position:  # It's a valid path
            valid_positions.append((x, y))


thief_position = random.choice(valid_positions)

#text function:

def get_font(text, size, color, x, y):
    font = pygame.font.Font(None, size)  
    img = font.render(text, True, color)    
    img = screen.blit(img, (x, y))

count = 0 


# Game loop
running = True
captured = False  
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


    # game statemnt box 
    pygame.draw.rect(screen,BLACK,(363,0,300,400))


    #  police (blue and red squares)
    for pos in police_positions:
        police_block = pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, BLUE, police_block)  # Blue square
        pygame.draw.rect(screen, RED, police_block.inflate(-15, -15))  # Red inside blue square
        if police_block.colliderect(thief_rect):  # checks to see if the grey block and the police block collides or not 
            get_font("You got Captured!", 35, (255,255, 255), 370, 60)
            escaped = True
            running = False
            break  
        

    #  the exit
    exit_block = pygame.Rect(exit_position[0] * BLOCK_SIZE, exit_position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, WHITE, exit_block)  # drawing Exit (white square)



    # adding police after a certin time 
    # count += 1 
    # if count >= 100 and count < 120:
    #     get_font("you took to long ", 25, (255,255, 255), 370, 60)
    #     get_font("the police raided the maze !", 25, (255,255, 255), 370, 80)
    # if count >= 120:
    #     captured = True
    #     break  
        




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

    # Check if the thief has escaped 
    if thief_position == exit_position:
        # print("The thief has escaped!")
        # running = False
        get_font("You have escaped !", 35, (255,255, 255), 364, 100)
        
        running = False
        break
             


        

    pygame.display.flip()

    # Limit to 10 frames per second
    clock.tick(10)

pygame.quit()

