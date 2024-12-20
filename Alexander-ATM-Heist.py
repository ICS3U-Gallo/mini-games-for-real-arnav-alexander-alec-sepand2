import pygame
import random


pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

player_x = 109
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

star_positions = [(random.randint(0, 200), random.randint(0, 150)) for _ in range(50)]

player_sprite_sheet = pygame.image.load('newsprt.png').convert_alpha()

last_rect_time = pygame.time.get_ticks
rectx1 = 200
rect_moving = False
rect_positions = [] 

snake_pos = [400, 300]
snake_body = [[400, 300]]
snake_direction = ""
snake_speed = 6
food_pos = [random.randrange(148, 500), random.randrange(132, 430)]
food_spawned = True
score = 0
snake_game_active = False 
over = False
win = False
no_pla = False
money = 0

player_anim = 0

player_anim_frame = 0  
player_anim_timer = 0  
ANIM_SPEED = 150 

invis_rect1 = pygame.Rect(310 - 25 + camera_x, 260 + 44, atm_width + 50, 30)

final_rect = (950,300,250,100)
running = True

def get_sprites(sheet, x, y, width, height):
    
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))

    return image

player_walk_right_anim_1 = get_sprites(player_sprite_sheet, 30, 0, 330, 800)
player_walk_right_anim_1 = pygame.transform.scale(player_walk_right_anim_1, (80, 180))
player_walk_right_anim_1.set_colorkey((255,0,0))

player_walk_left_anim_1 = pygame.transform.flip(player_walk_right_anim_1, True, False)
player_walk_left_anim_1.set_colorkey((255,0,0))

player_walk_right_anim_2 = get_sprites(player_sprite_sheet, 500, 0, 600, 800)
player_walk_right_anim_2 = pygame.transform.scale(player_walk_right_anim_2, (130, 180))
player_walk_right_anim_2.set_colorkey((255,0,0))

player_walk_left_anim_2 = pygame.transform.flip(player_walk_right_anim_2, True, False)
player_walk_left_anim_2.set_colorkey((255,0,0))

current_player_animation = player_walk_right_anim_1

def col_boundry():
    global running
    if player.colliderect(final_rect) and money == 0:
        get_font("Need Money To Proceed",30,(0,0,0),950-camera_x,200)
    if player.colliderect(final_rect) and money == 5:
        running = False


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
    global invis_rect1
    
    x -= camera_x
    
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

    invis_rect1 = pygame.Rect(310 - 25 - camera_x, 260 + 44, atm_width + 50, 30)

    

def get_font(text, size, color, x, y):
    font = pygame.font.Font(None, size)  
    img = font.render(text, True, color)    
    img = screen.blit(img, (x, y))

last_rect_time = 0

h_text = "Hacking..."
h_x = 313

def GameBox():
    global snake_game_active, snake_pos, snake_body, food_pos, food_spawned, score, snake_direction, over, win, no_pla, h_text, money, h_x
    
    pygame.draw.rect(screen, (0, 0, 30), (148, 80, 500, 430))
    pygame.draw.rect(screen, (10, 10, 50), (148, 80, 500, 50))
    get_font(h_text, 50, (100, 100, 250), h_x, 90)


    border_rect_1 = (145,130,3,381)
    border_rect_2 = (648,130,3,381)
    border_rect_3 = (148,130,510,3)
    border_rect_4 = (148,508,510,3)


    if not snake_game_active:
        get_font("Press SPACE to start Snake", 28, (100, 100, 250), 262, 135)
        get_font("Use WASD to move", 28, (100, 100, 250), 300, 165)
        get_font("Collect 10 red blocks", 28, (100, 100, 250), 293, 195)
        get_font("Avoid hitting youself and the border", 28, (100, 100, 250), 220, 225)
        return
    
    if over == True:
        get_font("You failed, Press SPACE to try again", 26, (100, 100, 250), 212, 135)
        return

    if win == True:
        h_text = "Hacking Complete!"
        no_pla = True
        h_x = 236
        return


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

    snake_body.insert(0, list(snake_pos))

    snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], 10, 10)
    food_rect = pygame.Rect(food_pos[0], food_pos[1], 10, 10)
    if snake_rect.colliderect(food_rect):  
        score += 1
        food_spawned = False  
    else:
        snake_body.pop()  


    if not food_spawned:
        food_pos = [random.randrange(148, 500), random.randrange(132, 430)]
        food_spawned = True

    if (snake_pos in snake_body[1:] or snake_rect.colliderect(border_rect_1) or snake_rect.colliderect(border_rect_2)
            or snake_rect.colliderect(border_rect_3) or snake_rect.colliderect(border_rect_4)):
        over = True
        snake_pos = [400, 300]
        snake_body = [[400, 300]]
        snake_direction = ""
        score = 0

    if score == 10:
        win = True
        money+=5


    for pos in snake_body:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    
    get_font(f"Score: {score}", 36, (100, 100, 250), 170, 95)


def reset_game():
    global snake_pos, snake_body, snake_direction, score, food_pos, food_spawned, snake_game_active
    global over, win, no_pla, h_text, h_x, money, playing, player_x, player_y, camera_x


    snake_pos = [400, 300]
    snake_body = [[400, 300]]
    snake_direction = ""
    score = 0
    food_pos = [random.randrange(148, 500), random.randrange(132, 430)]
    food_spawned = True
    over = False
    no_pla = False
    h_text = "Hacking..."
    h_x = 313
    
    player_x = 339
    player_y = 255
    camera_x = 0
    playing = False
    moving = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and player.colliderect(invis_rect1):
                playing = not playing
                if not playing:
                    reset_game()

            if event.key == pygame.K_SPACE and not snake_game_active and no_pla == False:  
                snake_game_active = True
            elif event.key == pygame.K_SPACE and over == True:  
                over = False

    keys_pressed = pygame.key.get_pressed()
    
    
    if moving:
        if player_x <= 0:
            edge = True
        if player_x >= 1095:
            edge_right = True
        if keys_pressed[pygame.K_a] and not edge:  
            player_x -= 5
            player_anim_timer += clock.get_time()
            if player_anim_timer >= ANIM_SPEED:
                player_anim_timer = 0
                player_anim_frame = (player_anim_frame + 1) % 2 
            current_player_animation = player_walk_left_anim_1 if player_anim_frame == 0 else player_walk_left_anim_2
    
        elif keys_pressed[pygame.K_d] and not edge_right:  
            player_x += 5
            player_anim_timer += clock.get_time()
            if player_anim_timer >= ANIM_SPEED:
                player_anim_timer = 0
                player_anim_frame = (player_anim_frame + 1) % 2  
            current_player_animation = player_walk_right_anim_1 if player_anim_frame == 0 else player_walk_right_anim_2
        
        else: 
            player_anim_timer = 0
            player_anim_frame = 0
    
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
    col_boundry()
    # pygame.draw.rect(screen, (0, 0, 0), (player.x - camera_x, player.y, player.width, player.height))
    pygame.draw.polygon(screen,(0,0,0),((870-camera_x,130),(870-camera_x,180),(910-camera_x,157)))
    pygame.draw.rect(screen,(0,0,0),(840-camera_x,146,30,20))
    get_font("VAULTS",43,(0,0,0),818-camera_x,100)
    screen.blit(current_player_animation,(player.x - camera_x, 228))
    # pygame.draw.rect(screen, (50, 50, 250), (final_rect[0] - camera_x, final_rect[1], final_rect[2], final_rect[3]))

    # pygame.draw.rect(screen, (0, 0, 0), invis_rect1)
    get_font(f"Money Collected: {money}",30,(0,0,0),20,20)
    
    if playing:
        GameBox()
        moving = False
    else:
        moving = True

    pygame.display.flip()
    clock.tick(20 if snake_game_active and win == False and playing else 60)

pygame.quit()
