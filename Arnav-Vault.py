import pygame
import random

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

money = 0

gravity = 9.1

ground = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

hiding = False

guards = []
lockers = []
vaults = []

font = pygame.font.Font('freesansbold.ttf', 32)

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
            pygame.draw.line(screen, (255, 0, 0), (self.x + 50, self.y + 50), (self.x + 400, self.y + 50))
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
        self.percent = 0
        self.max_progress = 1000
        self.max_bar = self.x + 100
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)

    def open(self, player):
        if self.rect.colliderect(player):
            self.progress += 2

player = Player(0, 0)

guard1 = Guard(0, HEIGHT - 150, 2, "right")
guards.append(guard1)

locker1 = Locker(200, HEIGHT - 100, hiding)
lockers.append(locker1)

vault1 = Vault(WIDTH - 100, HEIGHT - 150)
vaults.append(vault1)
vault2 = Vault(WIDTH - 300, HEIGHT - 150)
vaults.append(vault2)

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

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    if player.y + 100 < HEIGHT - 50:
        player.y += gravity
        player.move()

    for guard in guards:
        if guard.x + 50 > 0:
            guard.move()
            guard.check_collision(player)

    if not hiding:
        for guard in guards:
            guard.see_player()
            if guard.rect.colliderect(player):
                running = False

    for guard in guards:
        if guard.aware:
            if guard.direction == "right":
                guard.x_vel = 5
            else:
                guard.x_vel = -5

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    pygame.draw.rect(screen, (102, 92, 91), ground)

    for locker in lockers:
        locker.draw()
    
    for vault in vaults:
        vault.draw()
        if vault.progress > 0 and vault.progress < vault.max_progress:
            vault.percent = (vault.progress / vault.max_progress) * 100
            pygame.draw.rect(screen, (0, 255, 0), (vault.x, vault.y - 20, vault.percent, 10))

        if vault.progress >= vault.max_progress:
            vaults.remove(vault)
            money += 100
    
    text = font.render('Money: ' + str(money), True, (0, 0, 0))

    for guard in guards:
        if guard.x + 50 > 0:
            guard.draw()
            guard.vision()
        else:
            guards.remove(guard)

    if random.randint(0, 500) == 1 and len(guards) < 1:
        guard2 = Guard(0, HEIGHT - 150, 2, "right")
        guards.append(guard2)

    if hiding == False:
        player.draw()

    screen.blit(text, (0, 0))



    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
