import pygame
import random
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
rightcarx_1 = 750
rightcarx_2 = 1000
rightcarx_3 = 1250
rightcary= 350
#left side
leftcarx_1 = 750
leftcarx_2 = 1000
leftcarx_3 = 1250
leftcary = 500
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

# Starting the game
start = False

# Check if path is clear
pathclear = True


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

    if start == False:
        get_font("You must click right click to jump down", 30, (0, 0, 0), 150, 50)
        get_font("and space bar to jump up to avoid the incoming cars", 30, (0, 0, 0), 150, 70)
        get_font("if you understand these instructions click 'TAB'", 30, (0, 0, 0), 150, 90)
        #if section doesnt start check for this
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                start = True
                # checking if it reads it
                print('it works')

    if start == True:    

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

        # draw the road delimiters
        number_of_delimiters= 16
        for i in range(number_of_delimiters):
            pygame.draw.rect(screen, (YELLOW), (i*50, 450, 30, 5))



        # Basic cars right side
        carup = pygame.draw.rect(screen, (RED), (rightcarx_1, rightcary, 100, 50))

        # second car
        carup_2 = pygame.draw.rect(screen, (DARK_BLUE), (rightcarx_2, rightcary, 100, 50))
        carup_3 = pygame.draw.rect(screen, (DARK_BLUE), (rightcarx_3, rightcary, 100, 50))
        # --left side
        cardown = pygame.draw.rect(screen, (ORANGE), (leftcarx_1, leftcary, 100, 50))

        # second and thirdcar
        cardown_2 = pygame.draw.rect(screen, (YELLOW), (leftcarx_2, leftcary, 100, 50))
        cardown_3 = pygame.draw.rect(screen, (YELLOW), (leftcarx_3, leftcary, 100, 50))
        #--------------------

        # Moving the cars
        leftcarx_1 -= 1
        rightcarx_1 -= 2

        leftcarx_2 -= 2
        rightcarx_2 -= 1
        
        leftcarx_3 -= 1
        rightcarx_2 -= 2 
        #Character
        character = pygame.draw.rect(screen, (BLACK), (character_x, character_y, 50, 50))

        # Dying in the game
        # saying how if your character touches a car the game will end
        if character_x >= (leftcarx_1 + 5) and character_x <= (leftcarx_1 + 10) and leftcary == character_y:
            break
        if character_x >= (leftcarx_2 + 5) and character_x <= (leftcarx_2 + 10) and leftcary == character_y:
            break
        if character_x >= (leftcarx_3 + 5) and character_x <= (leftcarx_3 + 10) and leftcary == character_y:
            break
        # giving the user a chance to jump away if only the front of the car hits them
        elif cardown.colliderect(character):
            get_font("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        elif cardown_2.colliderect(character):
            get_font("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        elif cardown_3.colliderect(character):
            get_font("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        #once the middle section of the car hits them they will die
        elif character_x >= (rightcarx_1 + 15) and character_x <= (rightcarx_1 + 25) and rightcary == character_y:
            break
        elif character_x >= (rightcarx_2 + 15) and character_x <= (rightcarx_2 + 25) and rightcary == character_y:
            break
        elif character_x >= (rightcarx_3 + 15) and character_x <= (rightcarx_3 + 25) and rightcary == character_y:
            break
        elif carup.colliderect(character):
            get_font("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        elif carup_2.colliderect(character):
            get_font("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        elif carup_3.colliderect(character):
            get_font("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)

        # Spawning new cars (keeping traffic coming)
        if rightcarx_1 <= (character_x - 350):
            rightcarx_1 = 900
        elif rightcarx_2 == (character_x - 350):
            rightcarx_2 = 1000
        elif rightcarx_3 == (character_x - 350):
            rightcarx_3 = 1100
        elif leftcarx_1 <= (character_x - 350):
            leftcarx_1 = 900
        elif leftcarx_2 == ((character_x - 350)):
            leftcarx_2 = 1000
        elif leftcarx_3 == ((character_x - 350)):
            leftcarx_3 = 1100


        # Fixing being unable to escape traffic
        if rightcarx_1 == leftcarx_1 or rightcarx_2 == leftcarx_2 or rightcarx_3 == leftcarx_3 and character_x != 450:
            pathclear = False
        elif pathclear == False:
            get_font("You can't escape quickly click 'm' to jump to the middle", 50, (0, 0, 0), 100, 80)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    character_y += 100
        

        count += 1

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(FPS)
    #---------------------------


pygame.quit()
