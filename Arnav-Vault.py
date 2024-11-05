import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

player_x = 0
player_y = 0
player_width = 50
player_height = 100
player_x_vel = 3

gravity = 9.1

ground = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        player_x += player_x_vel
    if keys[pygame.K_a]:
        player_x -= player_x_vel
    # GAME STATE UPDATES
    # All game math and comparisons happen here
    player = pygame.Rect(player_x, player_y, player_width, player_height)
    if player_y + 100 < HEIGHT - 50:
        player_y += gravity

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    pygame.draw.rect(screen, (102, 92, 91), ground)

    pygame.draw.rect(screen, (255, 0, 0), player)



    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
