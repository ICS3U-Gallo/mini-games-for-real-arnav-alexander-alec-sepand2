import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

player_x = 339
player_y = 255

player = pygame.Rect(player_x,player_y,100,145)
ground = pygame.Rect(0, 400, 800, 200)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_d]:
        player_x += 5

    if keys_pressed[pygame.K_a]:
        player_x += -5

    player.x = player_x

    screen.fill((255, 255, 255))  
    pygame.draw.rect(screen, (80,80,80), ground)
    pygame.draw.rect(screen,(0,0,0),player)
    

    pygame.display.flip()
    clock.tick(60)
    


pygame.quit()
