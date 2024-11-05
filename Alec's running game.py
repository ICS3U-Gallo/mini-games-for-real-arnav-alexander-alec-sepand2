import pygame


pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)
FPS = 60
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock(FPS)
# Colours
WHITE = (255, 255, 255)
# ---------------------------
# Initialize global variables

circle_x = 200
circle_y = 200

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


  
    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # DRAWING
    screen.fill((WHITE))  # always the first drawing command

    pygame.draw.circle(screen, (0, 0, 255), (circle_x, circle_y), 30)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(FPS)
    #---------------------------


pygame.quit()
