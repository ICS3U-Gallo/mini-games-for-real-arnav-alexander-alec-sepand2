import pygame
import random

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

player = pygame.Rect(player_x, player_y, 100, 145)
ground = pygame.Rect(0, 400, 1200, 200)

playing = False
moving = True

edge = False
edge_right = False

camera_x = 0
camera_y = 0

star_positions = [(random.randint(0, 200), random.randint(0, 150)) for _ in range(50)]

def draw_night_sky():
    pygame.draw.rect(screen, (10, 10, 30), (100 - camera_x, 100, 200, 150))
    pygame.draw.rect(screen, (10, 10, 30), (400 - camera_x, 100, 200, 150))
    
    for (star_x, star_y) in star_positions:
        pygame.draw.circle(screen, (255, 255, 255), (100 - camera_x + star_x, 100 + star_y), 2)  
        pygame.draw.circle(screen, (255, 255, 255), (400 - camera_x + star_x, 100 + star_y), 2)  

def draw_win_frame():
    window_color = (100, 100, 100)
    pygame.draw.rect(screen, window_color, (95 - camera_x, 95, 210, 160), 5)
    pygame.draw.rect(screen, window_color, (395 - camera_x, 95, 210, 160), 5)

def draw_bank_background():
    wall_color = (200, 200, 200) 
    pygame.draw.rect(screen, wall_color, (0, 0, 1200, 400))
    

    #Clock
    clock_center = (350 - camera_x, 60)
    clock_radius = 40
    pygame.draw.circle(screen, (255, 255, 255), clock_center, clock_radius)
    pygame.draw.circle(screen, (0, 0, 0), clock_center, clock_radius, 2)
    pygame.draw.line(screen, (0, 0, 0), clock_center, 
                     (clock_center[0] + 20, clock_center[1]), 4)  
    pygame.draw.line(screen, (255, 0, 0), clock_center, 
                     (clock_center[0], clock_center[1] - 30), 2)  

    #Chandelier 
    chandelier_center = (700 - camera_x, 30)
    chandelier_color = (255, 215, 0)  
    pygame.draw.rect(screen, (100, 100, 100), (chandelier_center[0] - 50, chandelier_center[1], 100, 10))
    pygame.draw.rect(screen,(100,100,100),(chandelier_center[0]-2,chandelier_center[1]-100,6,100))
    for i in range(-40, 50, 40):
        chain_start = (chandelier_center[0] + i, chandelier_center[1] + 10)
        chain_end = (chandelier_center[0] + i, chandelier_center[1] + 60)
        pygame.draw.line(screen, (150, 150, 150), chain_start, chain_end, 2)
        pygame.draw.circle(screen, chandelier_color, (chandelier_center[0] + i, chandelier_center[1] + 60), 10)

def draw_atm(x, y):
    global invis_rect
    
    x -= camera_x
    y -= camera_y
    
    pygame.draw.rect(screen, (50, 50, 150), (x, y + 44, atm_width, atm_height))
    pygame.draw.polygon(screen, (50, 50, 150), [(x + 10, y - 4), (x + 70, y - 4), (x + 79, y + 43), (x, y + 43)])
    pygame.draw.rect(screen, (0, 100, 200), (x + 15, y + 5, atm_width - 31, 30))
    pygame.draw.polygon(screen, (20, 20, 90), [(x + 10, y + 37), (x + 70, y + 37), (x + 79, y + 43), (x, y + 43)])
    pygame.draw.rect(screen, (10, 10, 10), (x + 25, y + 50, atm_width - 50, 10))
    pygame.draw.rect(screen, (20, 20, 90), (x + 9, y - 17, 62, 13))

    keypad_x = x + 15
    keypad_y = y + 70
    for row in range(3):
        for col in range(3):
            pygame.draw.rect(screen, (100, 100, 100), (keypad_x + col * 17, keypad_y + row * 20, 15, 15))

    invis_rect = (x - 25, y + 44, atm_width + 50, 30)

def GameBox():
    pygame.draw.rect(screen, (0, 0, 0), (148, 160, 500, 300))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and player.colliderect(invis_rect):
                playing = not playing

    keys_pressed = pygame.key.get_pressed()
    if moving:
        if player_x <= 0:
            edge = True
        if player_x >= 1095:
            edge_right = True
        if keys_pressed[pygame.K_a] and not edge:
            player_x -= 5
        if keys_pressed[pygame.K_d] and not edge_right:
            player_x += 5
        else:
            edge = False
            edge_right = False

    player.x = player_x
    camera_x = player_x - WIDTH // 2 + player.width // 2
    camera_x = max(0, min(camera_x, ground.width - WIDTH))

    screen.fill((0, 0, 0))
    draw_bank_background()
    draw_night_sky()  
    draw_win_frame()
    pygame.draw.rect(screen, (80, 80, 80), (ground.x - camera_x, ground.y, ground.width, ground.height))
    draw_atm(310, 260)
    pygame.draw.rect(screen, (0, 0, 0), (player.x - camera_x, player.y, player.width, player.height))
    pygame.draw.rect(screen, (0, 0, 0), invis_rect)
    
    if playing:
        GameBox()
        moving = False
    else:
        moving = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
