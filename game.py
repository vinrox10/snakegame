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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# ----- INITIALIZATION -----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Mario Snake")

# Initialize font with fallback
try:
    font = pygame.font.SysFont('Arial', 24)
    font_big = pygame.font.SysFont('Arial', 48)
    font_medium = pygame.font.SysFont('Arial', 32)
except:
    # Fallback to default font if Arial not available
    font = pygame.font.Font(None, 24)
    font_big = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 32)

# Load sprites with better error handling
def load_sprites():
    """Load game sprites with fallback options."""
    mario_img = None
    mushroom_img = None
    
    try:
        mario_img = pygame.image.load("mario.png").convert_alpha()
        mario_img = pygame.transform.scale(mario_img, (CELL_SIZE, CELL_SIZE))
        print("✓ Mario sprite loaded successfully")
    except (pygame.error, FileNotFoundError):
        print("⚠ Mario sprite not found, using fallback")
        mario_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
        mario_img.fill(RED)
        # Draw a simple Mario-like shape
        pygame.draw.circle(mario_img, (255, 200, 150), (CELL_SIZE//2, CELL_SIZE//3), CELL_SIZE//4)
    
    try:
        mushroom_img = pygame.image.load("mushroom.png").convert_alpha()
        mushroom_img = pygame.transform.scale(mushroom_img, (CELL_SIZE, CELL_SIZE))
        print("✓ Mushroom sprite loaded successfully")
    except (pygame.error, FileNotFoundError):
        print("⚠ Mushroom sprite not found, using fallback")
        mushroom_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
        mushroom_img.fill((255, 165, 0))
        # Draw a simple mushroom shape
        pygame.draw.circle(mushroom_img, RED, (CELL_SIZE//2, CELL_SIZE//3), CELL_SIZE//3)
        pygame.draw.rect(mushroom_img, WHITE, (CELL_SIZE//2-3, CELL_SIZE//3, 6, CELL_SIZE//2))
    
    return mario_img, mushroom_img

mario_img, mushroom_img = load_sprites()

# ----- GAME FUNCTIONS -----
def new_food(snake):
    """Spawn food in a random cell not occupied by the snake."""
    while True:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake:
            return pos

def reset_game():
    """Reset game state for a new game."""
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = (1, 0)    # moving right
    food = new_food(snake)
    score = 0
    return snake, direction, food, score

def handle_input(event, current_direction):
    """Handle keyboard input with WASD and arrow key support."""
    if event.type == pygame.KEYDOWN:
        # Arrow keys
        if event.key == pygame.K_LEFT and current_direction != (1, 0):
            return (-1, 0)
        elif event.key == pygame.K_RIGHT and current_direction != (-1, 0):
            return (1, 0)
        elif event.key == pygame.K_UP and current_direction != (0, 1):
            return (0, -1)
        elif event.key == pygame.K_DOWN and current_direction != (0, -1):
            return (0, 1)
        # WASD keys
        elif event.key == pygame.K_a and current_direction != (1, 0):
            return (-1, 0)
        elif event.key == pygame.K_d and current_direction != (-1, 0):
            return (1, 0)
        elif event.key == pygame.K_w and current_direction != (0, 1):
            return (0, -1)
        elif event.key == pygame.K_s and current_direction != (0, -1):
            return (0, 1)
    
    return current_direction

def draw_background():
    """Draw the game background."""
    screen.fill(SKY_BLUE)
    # Draw brick "ground" at bottom row
    for x in range(GRID_WIDTH):
        rect = pygame.Rect(x*CELL_SIZE, GRID_HEIGHT*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BRICK_RED, rect)
        pygame.draw.rect(screen, GROUND_BROWN, rect.inflate(0, -CELL_SIZE//4))

def draw_game(snake, food, score):
    """Draw all game elements."""
    draw_background()
    
    # Draw food
    fx, fy = food
    screen.blit(mushroom_img, (fx*CELL_SIZE, fy*CELL_SIZE))
    
    # Draw snake
    for i, (x, y) in enumerate(snake):
        pos_px = (x*CELL_SIZE, y*CELL_SIZE)
        if i == 0:
            # Head as Mario
            screen.blit(mario_img, pos_px)
        else:
            # Body segments with slight variation
            body_color = (0, 155 - i*2, 0) if i*2 < 155 else (0, 100, 0)
            pygame.draw.rect(screen, body_color, (pos_px[0], pos_px[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 100, 0), (pos_px[0]+2, pos_px[1]+2, CELL_SIZE-4, CELL_SIZE-4))
    
    # Draw score
    score_surf = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surf, (5, 5))
    
    # Draw controls hint
    controls_surf = font.render("WASD or Arrow Keys to move", True, BLACK)
    screen.blit(controls_surf, (5, SCREEN_HEIGHT - 25))

def show_game_over_screen(score):
    """Show game over screen with restart option."""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    go_surf = font_big.render("Game Over", True, RED)
    go_rect = go_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
    screen.blit(go_surf, go_rect)
    
    # Final score
    score_surf = font_medium.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
    screen.blit(score_surf, score_rect)
    
    # Restart instructions
    restart_surf = font.render("Press SPACE to play again or ESC to quit", True, WHITE)
    restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
    screen.blit(restart_surf, restart_rect)
    
    pygame.display.flip()

# ----- MAIN GAME LOOP -----
def main():
    """Main game function."""
    snake, direction, food, score = reset_game()
    game_state = "playing"  # "playing" or "game_over"
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif game_state == "playing":
                direction = handle_input(event, direction)
            elif game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        snake, direction, food, score = reset_game()
                        game_state = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        if game_state == "playing":
            # Move snake
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)
            
            # Check collisions
            game_over = False
            
            # Wall collision
            if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                game_over = True
            
            # Self-collision
            if new_head in snake:
                game_over = True
            
            if game_over:
                game_state = "game_over"
                continue
            
            snake.insert(0, new_head)
            
            # Check food collision
            if new_head == food:
                score += 1
                food = new_food(snake)
            else:
                snake.pop()  # Remove tail segment
            
            # Draw everything
            draw_game(snake, food, score)
            pygame.display.flip()
        
        elif game_state == "game_over":
            show_game_over_screen(score)
    
    pygame.quit()
    sys.exit()

# ----- RUN GAME -----
if __name__ == "__main__":
    print("Starting Mario Snake Game...")
    print("Controls: WASD or Arrow Keys to move")
    print("Goal: Collect mushrooms to grow your snake!")
    main()
