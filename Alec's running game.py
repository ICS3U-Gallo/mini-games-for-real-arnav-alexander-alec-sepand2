import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
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

# Game duration in seconds
GAME_DURATION = 30

# Car's coordinates
NUMBER_OF_CARS = 4

cars_x_start_coordinates = [900, 1400, 1200, 1700]
cars_x = []
# copy the start coordinates
for x in cars_x_start_coordinates:
    cars_x.append(x)

cars_y = [350, 350, 500, 500]

# Car's colours
cars_colour = [RED, DARK_BLUE, ORANGE, YELLOW]

# Road coordinates
road_x = 0
road_y = 300

# Star properties
num_stars = 50

star_x = []
star_y = []

# generate x and y coordinates for each star
for i in range (0, num_stars):
    star_x.append(random.randint(0, WIDTH))
    star_y.append(random.randint(0, HEIGHT // 2))


# Character details
character_x = 300
character_y = 350

# adding a game clock
count = 0

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# draw text function
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Starting the game
start = False

# Winning the game
win = False

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
        # Show the instructions
        draw_text("You must click right click to jump down", 30, (0, 0, 0), 50, 50)
        draw_text("and space bar to jump up to avoid the incoming cars", 30, (0, 0, 0), 50, 70)
        draw_text("You only die if the middle of the car hits you, use this knowledge to win.", 30, (0, 0, 0), 50, 90)
        draw_text("if you understand these instructions click 'TAB'", 30, (0, 0, 0), 50, 110)
        # wait for the user to press 'TAB' key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            start = True

    if win == True:
        draw_text("You won!", 60, BLACK, 150, 50)
        # Once you win, after 2 seconds the game ends
        if count >= (FPS * (GAME_DURATION + 2)):
            break

    if start == True:
        
        # Road
        pygame.draw.rect(screen, PAVEMENT_GREY, (road_x, road_y, 800, 400)) # pavement

        # Road delimiters
        number_of_delimiters = 16
        for i in range(number_of_delimiters):
            pygame.draw.rect(screen, YELLOW, (i*50, 450, 30, 5))

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

        # List of cars
        cars = []
        for i in range(0, NUMBER_OF_CARS):
            # draw each car and add them to the car's list
            car = pygame.draw.rect(screen, (cars_colour[i]), (cars_x[i], cars_y[i], 100, 50))
            cars.append(car)

        # Character
        character = pygame.draw.rect(screen, BLACK, (character_x, character_y, 50, 50))

        # Check if the character is hit by a car
        # The game ends if the character touches a car
        for i in range(0, NUMBER_OF_CARS):
            car = cars[i]
            if car.colliderect(character):
                # Give the user a chance to jump away if only part of the car hits them
                draw_text("You got hit! Jump away quickly!", 50, BLACK, 170, 50)

            if (cars_x[i] + 5) <= character_x <= (cars_x[i] + 10) and cars_y[i] == character_y:
                # If the user didn't jump the user dies and end the game
                running = False
                break
            
            if count < (FPS * GAME_DURATION):
            # Move the cars
                cars_x[i] -= 2

            # Reset and reposition the car if it moves off-screen
            if cars_x[i] <= -100:
                # use the original start coordinates + a random distance
                cars_x[i] = cars_x_start_coordinates[i] + random.randint(0, 200)

        if running == False:
            break  # no need to continue

        # Check if we reach the end of the game
        if count >= (FPS * GAME_DURATION):
            # User wins if he was not hit by a car
            win = True

        count += 1

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(FPS)
    #---------------------------


pygame.quit()


pygame.quit()
