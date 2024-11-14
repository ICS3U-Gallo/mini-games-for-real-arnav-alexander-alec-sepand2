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

last_rect_time = pygame.time.get_ticks
rectx1 = 200
rect_moving = False
rect_positions = [] 

snake_pos = [400, 300]
snake_body = [[400, 300]]
snake_direction = ""
snake_speed = 10
food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]
food_spawned = True
score = 0
snake_game_active = False 

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

def get_font(text, size, color, x, y):
    font = pygame.font.Font(None, size)  
    img = font.render(text, True, color)    
    img = screen.blit(img, (x, y))

last_rect_time = 0

def GameBox():
    global snake_game_active, snake_pos, snake_body, food_pos, food_spawned, score, snake_direction
    
    pygame.draw.rect(screen, (0, 0, 30), (148, 80, 500, 430))
    pygame.draw.rect(screen, (10, 10, 50), (148, 80, 500, 50))
    get_font("Hacking...", 50, (100, 100, 250), 313, 90)

    if not snake_game_active:
        get_font("Press SPACE to start Snake", 26, (100, 100, 250), 212, 135)
        return
    
    # Update Snake
    keys = pygame.key.get_pressed()


    if keys[pygame.K_UP] or keys[pygame.K_w] and snake_direction != "DOWN":
        snake_direction = "UP"
    elif keys[pygame.K_DOWN] or keys[pygame.K_s] and snake_direction != "UP":
        snake_direction = "DOWN"
    elif keys[pygame.K_LEFT] or keys[pygame.K_a] and snake_direction != "RIGHT":
        snake_direction = "LEFT"
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and snake_direction != "LEFT":
        snake_direction = "RIGHT"

    if snake_direction == "UP":
        snake_pos[1] -= snake_speed
    elif snake_direction == "DOWN":
        snake_pos[1] += snake_speed
    elif snake_direction == "LEFT":
        snake_pos[0] -= snake_speed
    elif snake_direction == "RIGHT":
        snake_pos[0] += snake_speed

    # Snake growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawned = False
    else:
        snake_body.pop()

    # Spawning food
    if not food_spawned:
        food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]
        food_spawned = True

    # Game over conditions
    if (snake_pos[0] < 0 or snake_pos[0] > WIDTH or snake_pos[1] < 0 or snake_pos[1] > HEIGHT or
            snake_pos in snake_body[1:]):
        snake_game_active = False
        snake_pos = [400, 300]
        snake_body = [[400, 300]]
        snake_direction = "UP"
        score = 0

    # Draw snake and food
    for pos in snake_body:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    
    get_font(f"Score: {score}", 26, (255, 255, 255), 350, 110)


    


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and player.colliderect(invis_rect):
                playing = not playing
            if event.key == pygame.K_SPACE and not snake_game_active:  # Start snake game when not active
                snake_game_active = True
            elif event.key == pygame.K_SPACE and snake_game_active:  # Stop snake game when active
                snake_game_active = False

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
    # pygame.draw.rect(screen, (0, 0, 0), invis_rect)
    
    if playing:
        GameBox()
        moving = False
    else:
        moving = True

    pygame.display.flip()
    clock.tick(20 if snake_game_active else 60)

pygame.quit()
