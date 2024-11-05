# pygame template

import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
FPS = 60
Jamal_x = ()
Jamals_y =()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
BUSH_COLOUR = (16, 59, 29)

# ---------------------------
# Initialize global variables



# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # DRAWING
    screen.fill((46, 68, 140))  # always the first drawing command
    # the maze 
    pygame.draw.rect(screen,(BUSH_COLOUR),(400,0,2,4))
