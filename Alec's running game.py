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

#
# Car's coordinates
#
# right side
rightcarx_1 = 900
rightcarx_2 = 1400
rightcary= 350
# left side
leftcarx_1 = 1200
leftcarx_2 = 1700
leftcary = 500

# Road coordinates
road_x = 0
road_y = 300

# Character details
character_x = 300
character_y = 350

# adding a game clock
count = 0


# draw text function 
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)  
    img = font.render(text, True, color)    
    img = screen.blit(img, (x, y))

# Starting the game
start = False

# Winning the game
win = False

# Check if path is clear
pathclear = True

# Star properties
num_stars = 50

star_x = []
star_y = []

# generate x and y coordinates for each star
for i in range (0, num_stars):
    star_x.append(random.randint(0, WIDTH))
    star_y.append(random.randint(0, HEIGHT // 2))

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

    # Drawing the stars

    for i in range (0, num_stars):
        pygame.draw.circle(screen, YELLOW, (star_x[i], star_y[i]), 2)


    if start == False:
        draw_text("You must click right click to jump down", 30, (0, 0, 0), 50, 50)
        draw_text("and space bar to jump up to avoid the incoming cars", 30, (0, 0, 0), 50, 70)
        draw_text("You only die if the middle of the car hits you, use this knowledge to win.", 30, (0, 0, 0), 50, 90)
        draw_text("if you understand these instructions click 'TAB'", 30, (0, 0, 0), 50, 110)
        # if section doesn't start check for this
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                start = True

        
               
    if start == True:    

        # Road
        pygame.draw.rect(screen, PAVEMENT_GREY, (road_x, road_y, 800, 400)) # pavement
        
        # Lamp lights
        pygame.draw.ellipse(screen, YELLOW, (220, 210, 20, 20))
        pygame.draw.ellipse(screen, YELLOW, (420, 210, 20, 20))
        pygame.draw.ellipse(screen, YELLOW, (620, 210, 20, 20))

        # Lamp heads
        pygame.draw.rect(screen, PAVEMENT_GREY, (220, 200, 20, 20))
        pygame.draw.rect(screen, PAVEMENT_GREY, (420, 200, 20, 20))
        pygame.draw.rect(screen, PAVEMENT_GREY, (620, 200, 20, 20))
        
        # Lamps
        pygame.draw.rect(screen, PAVEMENT_GREY, (200, 210, 20, 100))
        pygame.draw.rect(screen, PAVEMENT_GREY, (400, 210, 20, 100))
        pygame.draw.rect(screen, PAVEMENT_GREY, (600, 210, 20, 100))

        # draw the road delimiters
        number_of_delimiters= 16
        for i in range(number_of_delimiters):
            pygame.draw.rect(screen, (YELLOW), (i*50, 450, 30, 5))


        # Basic cars right side
        carup = pygame.draw.rect(screen, (RED), (rightcarx_1, rightcary, 100, 50))

        # second car
        carup_2 = pygame.draw.rect(screen, (DARK_BLUE), (rightcarx_2, rightcary, 100, 50))
        
        # --left side
        cardown = pygame.draw.rect(screen, (ORANGE), (leftcarx_1, leftcary, 100, 50))

        # second and thirdcar
        cardown_2 = pygame.draw.rect(screen, (YELLOW), (leftcarx_2, leftcary, 100, 50))
        
        
        #Character
        character = pygame.draw.rect(screen, (BLACK), (character_x, character_y, 50, 50))

        # Dying in the game
        # if your character touches a car the game will end
        if character_x >= (leftcarx_1 + 5) and character_x <= (leftcarx_1 + 10) and leftcary == character_y:
            break
        if character_x >= (leftcarx_2 + 5) and character_x <= (leftcarx_2 + 10) and leftcary == character_y:
            break
        
        # giving the user a chance to jump away if only part of the car hits them
        if cardown.colliderect(character):
            draw_text("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        elif cardown_2.colliderect(character):
            draw_text("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        
        #once the middle section of the car hits them they will die
        elif character_x >= (rightcarx_1 + 15) and character_x <= (rightcarx_1 + 25) and rightcary == character_y:
            break
        elif character_x >= (rightcarx_2 + 15) and character_x <= (rightcarx_2 + 25) and rightcary == character_y:
            break
        
        elif carup.colliderect(character):
            draw_text("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        elif carup_2.colliderect(character):
            draw_text("You got hit! Jump away quickly!", 50, (0, 0, 0), 170, 50)
        
        # Minimum gap between cars
        # Minimum gap between left and right lanes to avoid overlap
        LANE_GAP = 300

        # Moving the cars
        if count < (60 * 30):
            leftcarx_1 -= 2
            rightcarx_1 -= 2
            leftcarx_2 -= 2
            rightcarx_2 -= 2

        # Reset and reposition the right cars if they move off-screen
        if rightcarx_1 <= -100:
            rightcarx_1 = 900 + random.randint(0, 200)
            # Ensure the car is at least 300 away from the nearest left car
            if abs(rightcarx_1 - leftcarx_1) < LANE_GAP:
                rightcarx_1 += LANE_GAP
            if abs(rightcarx_1 - leftcarx_2) < LANE_GAP:
                rightcarx_1 += LANE_GAP

        if rightcarx_2 <= -100:
            rightcarx_2 = 1400 + random.randint(0, 200)
            
            if abs(rightcarx_2 - leftcarx_1) < LANE_GAP:
                rightcarx_2 += LANE_GAP
            if abs(rightcarx_2 - leftcarx_2) < LANE_GAP:
                rightcarx_2 += LANE_GAP

        # Reset and reposition the left cars if they move off-screen
        if leftcarx_1 <= -100:
            leftcarx_1 = 1200 + random.randint(0, 200)
            
            if abs(leftcarx_1 - rightcarx_1) < LANE_GAP:
                leftcarx_1 += LANE_GAP
            if abs(leftcarx_1 - rightcarx_2) < LANE_GAP:
                leftcarx_1 += LANE_GAP

        if leftcarx_2 <= -100:
            leftcarx_2 = 1700 + random.randint(0, 200)
            
            if abs(leftcarx_2 - rightcarx_1) < LANE_GAP:
                leftcarx_2 += LANE_GAP
            if abs(leftcarx_2 - rightcarx_2) < LANE_GAP:
                leftcarx_2 += LANE_GAP

        MIN_CAR_GAP = 150
                # Reset and reposition the right cars if they move off-screen
        if rightcarx_1 <= -100:
            rightcarx_1 = 900 + random.randint(0, 200)
            # Ensure there's enough space between rightcarx_1 and rightcarx_2
            if abs(rightcarx_1 - rightcarx_2) < MIN_CAR_GAP:
                rightcarx_1 += MIN_CAR_GAP

        if rightcarx_2 <= -100:
            rightcarx_2 = 1400 + random.randint(0, 200)
    
            if abs(rightcarx_2 - rightcarx_1) < MIN_CAR_GAP:
                rightcarx_2 += MIN_CAR_GAP

        # Reset and reposition the left cars if they move off-screen
        if leftcarx_1 <= -100:
            leftcarx_1 = 1200 + random.randint(0, 200)
            # Ensure there's enough space between leftcarx_1 and leftcarx_2
            if abs(leftcarx_1 - leftcarx_2) < MIN_CAR_GAP:
                leftcarx_1 += MIN_CAR_GAP

        if leftcarx_2 <= -100:
            leftcarx_2 = 1700 + random.randint(0, 200)
            
            if abs(leftcarx_2 - leftcarx_1) < MIN_CAR_GAP:
                leftcarx_2 += MIN_CAR_GAP
        

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(FPS)
    #---------------------------


pygame.quit()


pygame.quit()
