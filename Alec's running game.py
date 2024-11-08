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
car_y= 350
#left side
carx = 750
cary = 500
# Road coordinates
road_x = 0
road_y = 300

# Character details
character_x = 299
character_y = 350

# adding a in game clock
count = 0

#text function:

def get_font(text, size, color, x, y):
    font = pygame.font.Font(None, size)  
    img = font.render(text, True, color)    
    img = screen.blit(img, (x, y))


running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if character_y == 350:
                character_y += 150
        elif event.type == pygame.KEYDOWN:
            if character_y > 350:
                character_y -= 150





    # DRAWING
    screen.fill(NIGHT_SKY)  # always the first drawing command

    # Road
    pygame.draw.rect(screen, PAVEMENT_GREY, (road_x, road_y, 800, 400)) # pavement
    
    # Lamp light
    pygame.draw.ellipse(screen, YELLOW, (220, 210, 20, 20))

    # Lamp head
    pygame.draw.rect(screen, PAVEMENT_GREY, (220, 200, 20, 20))
    
    # Lamp
    pygame.draw.rect(screen, PAVEMENT_GREY, (200, 210, 20, 100))
    
    # road yellow lines
    number_of_delimiters= 16
    for i in range(number_of_delimiters):
        pygame.draw.rect(screen, (YELLOW), (i*50, 450, 30, 5))

    # Basic cars right side
    pygame.draw.rect(screen, (RED), (car_x, car_y, 100, 50))

    # --left side
    pygame.draw.rect(screen, (ORANGE), (carx, cary, 100, 50))

    # Moving the cars
    carx -= 1
    car_x -= 2
    
    #Character
    pygame.draw.rect(screen, (BLACK), (character_x, character_y, 50, 50))

    # Dying in the game
    # saying how if your character touches a car the game will end
    if carx == (character_x + 35) and cary == character_y:
        get_font("You got hit!", 100, (0, 0, 0), 170, 50)
        break
    elif car_x == (character_x + 35) and car_y == character_y:
        get_font("You got hit!", 100, (0, 0, 0), 170, 50)
        break
    
    count += 1

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(FPS)
    #---------------------------


pygame.quit()
