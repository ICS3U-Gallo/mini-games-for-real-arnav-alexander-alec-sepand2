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
hiding = False

lockers = []

# ---------------------------

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hiding = False
        self.rect = pygame.Rect(self.x, self.y, 50, 100)

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def move(self):
        self.rect = pygame.Rect(self.x, self.y, 50, 100)

    def hide(self):
        if self.hiding == False:
            self.hiding = True
        else:
            self.hiding = False

class Gaurd():
    def __init__(self, x, y, x_vel, direction):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.direction = direction
        self.aware = False
        self.rect = pygame.Rect(self.x, self.y, 50, 100)

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)

    def move(self):
        self.x += self.x_vel
        self.rect = pygame.Rect(self.x, self.y, 50, 100)

        if self.x + 50 > WIDTH:
            self.x_vel *= -1
            self.direction = "left"

    def check_collision(self, player):
        if self.rect.colliderect(player):
            print("Game Over")

    def vision(self):
        if self.direction == "right":
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y + 50), (self.x + 400, self.y + 50))
        else:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y + 50), (self.x - 400, self.y + 50))

    def see_player(self):
        self.x *= 5
        self.aware = True

class Locker():
    def __init__(self, x, y, hiding):
        self.x = x
        self.y = y
        self.hiding = hiding
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

    def hide(self, player):
        if self.rect.colliderect(player):
            print("You Win")

player = Player(0, 0)

gaurd1 = Gaurd(0, HEIGHT - 150, 2, "right")
locker1 = Locker(200, HEIGHT - 100, hiding)
lockers.append(locker1)

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        player.x += player_x_vel
        player.move()
    if keys[pygame.K_a]:
        player.x -= player_x_vel
        player.move()
    if keys[pygame.K_e]:
        if hiding == False:
            for locker in lockers:
                if locker.rect.colliderect(player):
                    locker.hide(player)

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    if player.y + 100 < HEIGHT - 50:
        player.y += gravity
        player.move()

    if gaurd1.x + 50 > 0:
        gaurd1.move()
        gaurd1.check_collision(player)

    locker1.hide(player)

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    pygame.draw.rect(screen, (102, 92, 91), ground)

    player.draw()

    locker1.draw()

    if gaurd1.x + 50 > 0:
        gaurd1.draw()
        gaurd1.vision()




    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
