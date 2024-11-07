import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

player_x = 339
player_y = 255

atm_width = 80
atm_height = 96

player = pygame.Rect(player_x,player_y,100,145)
ground = pygame.Rect(0, 400, 800, 200)

playing = False
moving = True


def draw_atm(x, y):
    global invis_rect
    
    #ATM body
    pygame.draw.rect(screen, (50, 50, 150), (x, y+44, atm_width, atm_height))
    
    #ATM head
    pygame.draw.polygon(screen, (50, 50, 150), [(x + 10, y - 4), (x + 70, y - 4), (x + 79, y + 43), (x, y + 43)])

    # Screen
    pygame.draw.rect(screen, (0, 100, 200), (x + 15, y + 5, atm_width - 31, 30))
    
    #Atm inner detail
    pygame.draw.polygon(screen, (20, 20, 90), [(x + 10, y +37), (x + 70, y +37), (x + 79, y + 43), (x, y + 43)])

    # Card slot
    pygame.draw.rect(screen, (10, 10, 10), (x + 25, y + 50, atm_width - 50, 10))
    
    #ATM Top piece
    pygame.draw.rect(screen, (20, 20, 90), (x+9, y -17, 62, 13))



    # Keypad
    keypad_x = x + 15
    keypad_y = y + 70
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(screen, (100, 100, 100), (keypad_x + col * 17, keypad_y + row * 20, 15, 15))

    invis_rect = (x-25,y+44,atm_width+50,30)

def GameBox():
        pygame.draw.rect(screen,(0,0,0),(148,160,500,300))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if player.colliderect(invis_rect):
                    playing = not playing


    keys_pressed = pygame.key.get_pressed()
    if moving == True:
        if keys_pressed[pygame.K_d]:
            player_x += 5

        if keys_pressed[pygame.K_a]:
            player_x += -5

    player.x = player_x


    screen.fill((255, 255, 255))  
    pygame.draw.rect(screen, (80,80,80), ground)
    draw_atm(220,260)
    pygame.draw.rect(screen,(0,0,0),player)
    
    if playing:
        GameBox()
        moving = False
    if not playing:
        moving = True

    pygame.display.flip()
    clock.tick(60)
    


pygame.quit()
