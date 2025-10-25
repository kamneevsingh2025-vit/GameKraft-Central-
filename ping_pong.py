import pygame
import sys

# --- Initialization ---
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
CAPTION = "Simple Pong"
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle properties
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Ball properties
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# --- Setup Screen and Clock ---
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

# --- Game Objects (Rectangles) ---

# Paddles
player1_paddle = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Initial ball direction/velocity
ball_speed_x = BALL_SPEED_X * (1 if pygame.time.get_ticks() % 2 == 0 else -1) # Start in a random horizontal direction
ball_speed_y = BALL_SPEED_Y * (1 if pygame.time.get_ticks() % 3 != 0 else -1) # Start in a random vertical direction

# Score (Not fully implemented for display, just variables)
score1 = 0
score2 = 0

# --- Functions ---

def move_paddles():
    """Handles keyboard input for moving paddles."""
    keys = pygame.key.get_pressed()
    
    # Player 1 controls (W/S)
    if keys[pygame.K_w] and player1_paddle.top > 0:
        player1_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_paddle.bottom < SCREEN_HEIGHT:
        player1_paddle.y += PADDLE_SPEED

    # Player 2 controls (Up/Down Arrows)
    if keys[pygame.K_UP] and player2_paddle.top > 0:
        player2_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2_paddle.bottom < SCREEN_HEIGHT:
        player2_paddle.y += PADDLE_SPEED

def move_ball():
    """Updates the ball's position and handles wall collisions."""
    global ball_speed_x, ball_speed_y
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1  # Reverse vertical direction

    # Collision with left/right boundaries (Scoring)
    if ball.left <= 0:
        # Player 2 scores
        global score2
        score2 += 1
        reset_ball()
    
    if ball.right >= SCREEN_WIDTH:
        # Player 1 scores
        global score1
        score1 += 1
        reset_ball()

def check_paddle_collision():
    """Handles ball collision with paddles and reverses horizontal direction."""
    global ball_speed_x
    
    if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
        # Only reverse if the ball is moving towards the paddle it hit
        if ball_speed_x < 0 and ball.colliderect(player1_paddle):
            ball_speed_x *= -1
        elif ball_speed_x > 0 and ball.colliderect(player2_paddle):
            ball_speed_x *= -1

def reset_ball():
    """Resets the ball to the center after a score."""
    global ball_speed_x, ball_speed_y
    ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
    ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
    
    # Optional: Slightly increase speed or change direction after reset
    ball_speed_x *= (1 if pygame.time.get_ticks() % 2 == 0 else -1) * 1.05 # Increase speed slightly
    ball_speed_y *= (1 if pygame.time.get_ticks() % 3 != 0 else -1) * 1.05


# --- Main Game Loop ---
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Game Logic Updates
    move_paddles()
    move_ball()
    check_paddle_collision()
    
    # 3. Drawing/Rendering
    screen.fill(BLACK) # Clear screen

    # Draw Paddles and Ball
    pygame.draw.rect(screen, WHITE, player1_paddle)
    pygame.draw.rect(screen, WHITE, player2_paddle)
    pygame.draw.ellipse(screen, WHITE, ball) # Draw ball as a circle/ellipse

    # Optional: Draw center line
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# --- Cleanup ---
pygame.quit()
sys.exit()
