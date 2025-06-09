import pygame
import random
import sys

# ----- CONFIGURATION -----
CELL_SIZE = 32            # size of one grid cell (px)
GRID_WIDTH = 20           # number of cells horizontally
GRID_HEIGHT = 15          # number of cells vertically
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT + CELL_SIZE  # extra row for ground
FPS = 10                  # game speed (frames per second)

# ----- COLORS -----
SKY_BLUE = (135, 206, 235)
BRICK_RED = (178, 34, 34)
GROUND_BROWN = (139, 69, 19)

# ----- INITIALIZATION -----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Mario Snake")

# load sprites
try:
    mario_img    = pygame.image.load("mario.png").convert_alpha()
    mushroom_img = pygame.image.load("mushroom.png").convert_alpha()
    mario_img    = pygame.transform.scale(mario_img, (CELL_SIZE, CELL_SIZE))
    mushroom_img = pygame.transform.scale(mushroom_img, (CELL_SIZE, CELL_SIZE))
except (pygame.error, FileNotFoundError):
    # fallback if images missing
    mario_img    = pygame.Surface((CELL_SIZE, CELL_SIZE))
    mushroom_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
    mario_img.fill((255, 0, 0))
    mushroom_img.fill((255, 165, 0))

# ----- GAME STATE -----
def new_food(snake):
    """Spawn food in a random cell not occupied by the snake."""
    while True:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake:
            return pos

snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
direction = (1, 0)    # moving right
food = new_food(snake)
score = 0

# ----- MAIN LOOP -----
running = True
while running:
    clock.tick(FPS)
    # --- Event handling ---
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evt.type == pygame.KEYDOWN:
            # arrow keys or WASD
            if evt.key == pygame.K_LEFT  and direction != (1,0):  direction = (-1, 0)
            if evt.key == pygame.K_RIGHT and direction != (-1,0): direction = (1,  0)
            if evt.key == pygame.K_UP    and direction != (0,1):  direction = (0, -1)
            if evt.key == pygame.K_DOWN  and direction != (0,-1): direction = (0,  1)

    # --- Move snake ---
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # Check wall collisions
    if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
        running = False

    # Check self-collision
    if new_head in snake:
        running = False

    if not running:
        break

    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += 1
        food = new_food(snake)
    else:
        snake.pop()  # remove tail segment

    # --- Draw background ---
    screen.fill(SKY_BLUE)
    # draw brick "ground" at bottom row
    for x in range(GRID_WIDTH):
        rect = pygame.Rect(x*CELL_SIZE, GRID_HEIGHT*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BRICK_RED, rect)
        pygame.draw.rect(screen, GROUND_BROWN, rect.inflate(0, -CELL_SIZE//4))

    # --- Draw food ---
    fx, fy = food
    screen.blit(mushroom_img, (fx*CELL_SIZE, fy*CELL_SIZE))

    # --- Draw snake ---
    for i, (x, y) in enumerate(snake):
        pos_px = (x*CELL_SIZE, y*CELL_SIZE)
        if i == 0:
            # head as Mario
            screen.blit(mario_img, pos_px)
        else:
            # body segments
            pygame.draw.rect(screen, (0, 155, 0), (pos_px[0], pos_px[1], CELL_SIZE, CELL_SIZE))

    # --- Draw score ---
    font = pygame.font.SysFont(None, 24)
    score_surf = font.render(f"Score: {score}", True, (0,0,0))
    screen.blit(score_surf, (5, 5))

    # --- Update display ---
    pygame.display.flip()

# ----- GAME OVER -----
# simple Game Over screen
font_big = pygame.font.SysFont(None, 48)
go_surf = font_big.render("Game Over", True, (255,0,0))
screen.blit(go_surf, (SCREEN_WIDTH//2 - go_surf.get_width()//2, SCREEN_HEIGHT//2))
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()
