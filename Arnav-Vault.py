import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Vault Crack")

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
vaults = []

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


class Guard():
    def __init__(self, x, y, x_vel, direction):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.direction = direction
        self.vision_hitbox = pygame.Rect(0, 0, 0, 0)
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
            pass

    def vision(self):
        if self.direction == "right":
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y + 50), (self.x + 400, self.y + 50))
            self.vision_hitbox = pygame.Rect(self.x, self.y, 400, 100)
        else:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y + 50), (self.x - 400, self.y + 50))
            self.vision_hitbox = pygame.Rect(self.x - 400, self.y, 400, 100)

    def see_player(self):
        if self.vision_hitbox.colliderect(player):
            self.aware = True
            print("Guard sees player")

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
            pass

class Vault():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.progress = 0
        self.max_progress = 1000
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

    def open(self, player):
        if self.rect.colliderect(player):
            self.progress += 2
            if self.progress >= self.max_progress:
                print("Vault opened")
                self.progress = 0

player = Player(0, 0)

guard1 = Guard(0, HEIGHT - 150, 2, "right")

locker1 = Locker(200, HEIGHT - 100, hiding)
lockers.append(locker1)

vault1 = Vault(WIDTH - 100, HEIGHT - 100)
vaults.append(vault1)

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if not hiding:
                    for locker in lockers:
                        if locker.rect.colliderect(player):
                            hiding = True
                else:
                    hiding = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        if not hiding:
            player.x += player_x_vel
            player.move()

    if keys[pygame.K_a]:
        if not hiding:
            player.x -= player_x_vel
            player.move()

    if keys[pygame.K_SPACE]:
        for vault in vaults:
            vault.open(player)
            print(vault.progress)

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    if player.y + 100 < HEIGHT - 50:
        player.y += gravity
        player.move()

    if guard1.x + 50 > 0:
        guard1.move()
        guard1.check_collision(player)

    if not hiding:
        guard1.see_player()

    if guard1.aware:
        if guard1.direction == "right":
            guard1.x_vel = 5
        else:
            guard1.x_vel = -5

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    pygame.draw.rect(screen, (102, 92, 91), ground)

    if hiding == False:
        player.draw()

    for locker in lockers:
        locker.draw()
    
    for vault in vaults:
        vault.draw()

    if guard1.x + 50 > 0:
        guard1.draw()
        guard1.vision()



    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
