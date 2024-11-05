import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
FPS = 60
# Colours
WHITE = (255, 255, 255)
RED = (250, 0, 0)
NIGHT_SKY = (46, 68, 130)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
DARK_ORANGE = (255, 140, 0)
DARK_BLUE = (25, 25, 112)
GREY = (169, 169, 169)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 102)
BLUE_HUE = 112
PAVEMENT_GREY = (145, 145, 145)
GREEN = (6, 64, 43)
# ---------------------------
# Initialize global variables

circle_x = 200
circle_y = 200

# ---------------------------

# Car's coordinates
car_x = 750
car_y= 400

# Road coordinates
road_x = 0
road_y = 300

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # DRAWING
    screen.fill(NIGHT_SKY)  # always the first drawing command

    # Road
    pygame.draw.rect(screen, PAVEMENT_GREY, (road_x, road_y, 800, 400)) # pavement
    # road yellow lines
    pygame.draw.rect(screen, (YELLOW), (0, 450, 30, 5))
    pygame.draw.rect(screen, (YELLOW), (50, 450, 30, 5))
    pygame.draw.rect(screen, (YELLOW), (100, 450, 30, 5))
    pygame.draw.rect(screen, (YELLOW), (150, 450, 30, 5))
    pygame.draw.rect(screen, (YELLOW), (200, 450, 30, 5))

    # Basic cars
    pygame.draw.rect(screen, (RED), (car_x, car_y, 100, 50))


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(FPS)
    #---------------------------


pygame.quit()
