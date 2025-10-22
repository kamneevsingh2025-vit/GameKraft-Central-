import pygame
import numpy as np
import random
import sys

# --- Initialize pygame ---
pygame.init()

# --- Game Settings ---
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 10

# Colors
BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
GRAY = (80, 80, 100)
ORE_COLOR = (255, 223, 0)
ASTEROID_COLOR = (200, 60, 60)
PLAYER_COLOR = (0, 200, 255)
TEXT_COLOR = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
pygame.display.set_caption("🚀 SPACE MINER")

font = pygame.font.SysFont("consolas", 24)
clock = pygame.time.Clock()

# --- Load or create simple sounds ---
# (Short beep tones if no .wav file provided)
pygame.mixer.init()
ore_sound = pygame.mixer.Sound("collect.wav")
asteroid_sound = pygame.mixer.Sound("hit.wav")

# --- Game variables ---
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
player_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
grid[player_pos[0], player_pos[1]] = 9
score = 0
health = 100
running = True

# Randomly spawn ores and asteroids
for _ in range(8):
    grid[random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)] = 1
for _ in range(6):
    grid[random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)] = -1


# --- Helper functions ---
def draw_grid():
    """Draws the grid and all game objects."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell_value = grid[x, y]
            
            if cell_value == 9:
                color = PLAYER_COLOR
            elif cell_value == 1:
                color = ORE_COLOR
            elif cell_value == -1:
                color = ASTEROID_COLOR
            else:
                color = GRAY

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

def draw_ui():
    """Draw score and health."""
    ui_y = HEIGHT + 20
    text = font.render(f"Score: {score}   Health: {health}", True, TEXT_COLOR)
    screen.blit(text, (20, ui_y))

def move_player(dx, dy):
    """Move player and handle events."""
    global player_pos, score, health, running

    x, y = player_pos
    new_x, new_y = x + dx, y + dy

    # Stay in bounds
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        grid[x, y] = 0  # Clear old pos

        if grid[new_x, new_y] == 1:
            score += 10
            ore_sound.play()
        elif grid[new_x, new_y] == -1:
            health -= 10
            asteroid_sound.play()

        # Update position
        grid[new_x, new_y] = 9
        player_pos = [new_x, new_y]

        # Respawn new ore/asteroid
        if random.random() < 0.3:
            rx, ry = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            grid[rx, ry] = random.choice([1, -1])

        # Check health instantly
        if health <= 0:
            running = False


def show_game_over():
    """Display end screen."""
    screen.fill(BLACK)
    over_text = font.render("GAME OVER 💀", True, (255, 80, 80))
    score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    tip_text = font.render("Press any key to exit", True, TEXT_COLOR)
    
    screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(tip_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    pygame.display.flip()

    # Wait for keypress to close
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting = False
    pygame.quit()
    sys.exit()


# --- Main Game Loop ---
while running:
    screen.fill(BLACK)
    draw_grid()
    draw_ui()
    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: move_player(-1, 0)
            elif event.key == pygame.K_DOWN: move_player(1, 0)
            elif event.key == pygame.K_LEFT: move_player(0, -1)
            elif event.key == pygame.K_RIGHT: move_player(0, 1)

# --- Show Game Over Screen ---
show_game_over()

