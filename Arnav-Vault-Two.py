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

f1_guard_chance_range = 1000
f2_guard_chance_range = 1000

spawning_f1_guard = False
spawning_f2_guard = False
spawning_f1_guard_counter = 0
spawning_f2_guard_counter = 0

money = 0

ground = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
floor2 = pygame.Rect(0, HEIGHT - 375, WIDTH, 50)

current_floor = "f1"

hiding = False
can_hide = True

guards = []
lockers = []
vaults = []

stairway_down = pygame.Rect(0, HEIGHT - 175, 75, 125)
stairway_up = pygame.Rect(0, HEIGHT - 500, 75, 125)

font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 64)

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
    
    def stair_down(self):
        if self.rect.colliderect(stairway_down):
            self.y -= 325
    
    def stair_up(self):
        if self.rect.colliderect(stairway_up):
            self.y += 325


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

class Locker():
    def __init__(self, x, y, hiding):
        self.x = x
        self.y = y
        self.hiding = hiding
        self.rect = pygame.Rect(self.x, self.y, 50, 100)

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        for i in range(4):
            pygame.draw.line(screen, (0, 0, 0), (self.x + 10, self.y + 10 + (i * 5)), (self.x + 40, self.y + 10 + (i * 5)), 2)

class Vault():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.progress = 0
        self.percent = 0
        self.max_progress = 1000
        self.max_bar = self.x + 100
        self.opening = False
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pygame.draw.circle(screen, (150, 150, 150), (self.x + 50, self.y + 50), 25)
        
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 50, self.y + 45), 5)
        pygame.draw.rect(screen, (0, 0, 0), (self.x + 48, self.y + 48, 5, 10))

    def open(self, player):
        if self.rect.colliderect(player):
            self.opening = True
        if self.opening == True and hiding == False:
            self.progress += 1
        

player = Player(0, HEIGHT - 150)

f1_guard = Guard(0, HEIGHT - 150, 2, "right")
f2_guard = Guard(0, HEIGHT - 475, 2, "right")

locker1 = Locker(200, HEIGHT - 150, hiding)
lockers.append(locker1)
locker2 = Locker(625, HEIGHT - 150, hiding)
lockers.append(locker2)
locker3 = Locker(325, HEIGHT - 475, hiding)
lockers.append(locker3)
locker4 = Locker(725, HEIGHT - 475, hiding)
lockers.append(locker4)

vault1 = Vault(WIDTH - 500, HEIGHT - 150)
vaults.append(vault1)
vault2 = Vault(WIDTH - 300, HEIGHT - 150)
vaults.append(vault2)
vault3 = Vault(WIDTH - 100, HEIGHT - 150)
vaults.append(vault3)
vault4 = Vault(WIDTH - 600, HEIGHT - 475)
vaults.append(vault4)
vault5 = Vault(WIDTH - 400, HEIGHT - 475)
vaults.append(vault5)
vault6 = Vault(WIDTH - 200, HEIGHT - 475)
vaults.append(vault6)

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if can_hide:
                    if not hiding:
                        for locker in lockers:
                            if locker.rect.colliderect(player):
                                hiding = True
                    else:
                        hiding = False
            
            if event.key == pygame.K_w:
                if player.rect.colliderect(stairway_up):
                    player.stair_up()
                    player.move()
                elif player.rect.colliderect(stairway_down):
                    player.stair_down()
                    player.move()

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
            can_hide = False
            if guard.direction == "right":
                guard.x_vel = 5
            else:
                guard.x_vel = -5
        else:
            can_hide = True

        if guard.aware == True and player.y != guard.y:
            if guard.y == HEIGHT - 150:
                if guard.rect.colliderect(stairway_down):
                    guard.y -= 325
                    guard.direction = "right"
                    guard.x_vel *= -1
                    guard.aware = False
            else:
                if guard.rect.colliderect(stairway_up):
                    guard.y += 325
                    guard.direction = "right"
                    guard.x_vel *= -1
                    guard.aware = False
    
    for vault in vaults:
        if vault.rect.colliderect(player) != True:
            vault.opening = False
                

    if player.y == HEIGHT - 475:
        current_floor = "f2"
    else:
        current_floor = "f1"

    # DRAWING
    for guard in guards:
        if guard.x + 50 > 0:
            guard.vision()

    screen.fill((50, 50, 50))  # always the first drawing command

    pygame.draw.rect(screen, (102, 92, 91), ground)
    pygame.draw.rect(screen, (102, 92, 91), floor2)

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

    pygame.draw.rect(screen, (0, 0, 0), stairway_down)
    pygame.draw.rect(screen, (0, 0, 0), stairway_up)
    
    text = font.render('Money: ' + str(money), True, (255, 255, 255))

    for guard in guards:
        if guard.x + 50 > 0:
            guard.draw()
        else:
            guards.remove(guard)

    # Spawn Guards with random chance on both floors, increase chance of spawning every tick the guard is not spawned

    if spawning_f1_guard:
        spawning_f1_guard_counter += 1
        f1_warning = font2.render('!', True, (255, 0, 0))
        screen.blit(f1_warning, (25, HEIGHT - 150))

        if spawning_f1_guard_counter >= 75:
            f1_guard = Guard(0, HEIGHT - 150, 2, "right")
            guards.append(f1_guard)
            spawning_f1_guard = False
            spawning_f1_guard_counter = 0
    else:

        if random.randrange(1, f1_guard_chance_range) == 1 and f1_guard not in guards:
            spawning_f1_guard = True

            f1_guard_chance_range = 1000

        elif f1_guard not in guards:
            f1_guard_chance_range -= 2

    if spawning_f2_guard:
        spawning_f2_guard_counter += 1
        f2_warning = font2.render('!', True, (255, 0, 0))
        screen.blit(f2_warning, (25, HEIGHT - 475))

        if spawning_f2_guard_counter >= 75:
            f2_guard = Guard(0, HEIGHT - 475, 2, "right")
            guards.append(f2_guard)
            spawning_f2_guard = False
            spawning_f2_guard_counter = 0

    else:

        if random.randrange(1, f2_guard_chance_range) == 1 and f2_guard not in guards:
            
            spawning_f2_guard = True

            f2_guard_chance_range = 1000
        elif f2_guard not in guards:
            f2_guard_chance_range -= 2


    if hiding == False:
        player.draw()

    # GUI
    if player.rect.colliderect(stairway_down) or player.rect.colliderect(stairway_up):
        w_text = font.render('W', True, (255, 255, 255))
        screen.blit(w_text, (player.x + 10, player.y - 50))
    
    for locker in lockers:
        if locker.rect.colliderect(player) and not hiding:
            if can_hide:
                e_text = font.render('E', True, (255, 255, 255))
                screen.blit(e_text, (player.x + 10, player.y - 50))

    for vault in vaults:
        if vault.rect.colliderect(player) and not hiding:
            space_text = font.render('SPACE', True, (255, 255, 255))
            screen.blit(space_text, (player.x - 25, player.y - 50))

    screen.blit(text, (0, 0))



    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()