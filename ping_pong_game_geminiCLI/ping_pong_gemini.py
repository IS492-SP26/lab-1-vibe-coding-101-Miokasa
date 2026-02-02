
import pygame
import sys
import random

# --- Initialization ---
pygame.init()

# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 140
BALL_RADIUS = 7

# Speeds
PADDLE_SPEED = 7
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ping-Pong')

# Clock to control the frame rate
clock = pygame.time.Clock()

# --- Game Objects ---
# Paddles
player_paddle = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(20, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(SCREEN_WIDTH / 2 - BALL_RADIUS, SCREEN_HEIGHT / 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# --- Game Variables ---
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
player_speed = 0
opponent_speed = 0

# Score
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

def ball_reset():
    """Resets the ball to the center with a random direction."""
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

# --- Main Game Loop ---
while True:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Player paddle movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += PADDLE_SPEED
            if event.key == pygame.K_UP:
                player_speed -= PADDLE_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= PADDLE_SPEED
            if event.key == pygame.K_UP:
                player_speed += PADDLE_SPEED
                
        # Opponent paddle movement (simple AI)
        # For a two-player game, this would be replaced with key handling for a second player (e.g., W and S keys)
        # For simplicity, we'll make the opponent paddle track the ball
        # You could use the following for a 2-player setup:
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_s:
        #         opponent_speed += PADDLE_SPEED
        #     if event.key == pygame.K_w:
        #         opponent_speed -= PADDLE_SPEED
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_s:
        #         opponent_speed -= PADDLE_SPEED
        #     if event.key == pygame.K_w:
        #         opponent_speed += PADDLE_SPEED

    # --- Game Logic ---
    
    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision: Top and Bottom walls
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Ball collision: Left and Right walls (scoring)
    if ball.left <= 0:
        player_score += 1
        ball_reset()

    if ball.right >= SCREEN_WIDTH:
        opponent_score += 1
        ball_reset()

    # Ball collision: Paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1
        
    # Paddle movement and boundaries
    player_paddle.y += player_speed
    if player_paddle.top <= 0:
        player_paddle.top = 0
    if player_paddle.bottom >= SCREEN_HEIGHT:
        player_paddle.bottom = SCREEN_HEIGHT

    # Simple AI for opponent paddle
    if opponent_paddle.top < ball.y:
        opponent_paddle.top += PADDLE_SPEED
    if opponent_paddle.bottom > ball.y:
        opponent_paddle.bottom -= PADDLE_SPEED
    if opponent_paddle.top <= 0:
        opponent_paddle.top = 0
    if opponent_paddle.bottom >= SCREEN_HEIGHT:
        opponent_paddle.bottom = SCREEN_HEIGHT

    # --- Drawing ---
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, LIGHT_GREY, player_paddle)
    pygame.draw.rect(screen, LIGHT_GREY, opponent_paddle)
    pygame.draw.ellipse(screen, LIGHT_GREY, ball)
    pygame.draw.aaline(screen, LIGHT_GREY, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    # Display scores
    player_text = game_font.render(f"{player_score}", False, LIGHT_GREY)
    screen.blit(player_text, (SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2))

    opponent_text = game_font.render(f"{opponent_score}", False, LIGHT_GREY)
    screen.blit(opponent_text, (SCREEN_WIDTH / 2 - 45, SCREEN_HEIGHT / 2))

    # --- Update the Display ---
    pygame.display.flip()
    clock.tick(60)
