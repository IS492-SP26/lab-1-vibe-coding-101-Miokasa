import pygame
import sys
import random
import numpy as np

# --- Initialization ---
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

# --- Game Constants ---
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
BG_COLOR_TOP = pygame.Color('#2c3e50')
BG_COLOR_BOTTOM = pygame.Color('#34495e')
UI_COLOR = pygame.Color('#ecf0f1')
PADDLE_COLOR = pygame.Color('#1abc9c')
BALL_COLOR = pygame.Color('#f1c40f')
ACCENT_COLOR = pygame.Color('#e74c3c')

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 160
BALL_RADIUS = 10

# Speeds
PADDLE_SPEED = 8
BALL_SPEED_X_START = 8
BALL_SPEED_Y_START = 8

# Game Logic Rules
WINNING_SCORE = 11
SETS_TO_WIN_MATCH = 2 # Best of 3

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hyper-Pong')
clock = pygame.time.Clock()

# --- Fonts ---
title_font = pygame.font.Font(pygame.font.get_default_font(), 80)
score_font = pygame.font.Font(pygame.font.get_default_font(), 50)
ui_font = pygame.font.Font(pygame.font.get_default_font(), 30)
instructions_font = pygame.font.Font(pygame.font.get_default_font(), 20)

# --- Sound Generation ---
def generate_sound(frequency, duration, volume=0.1):
    """Generates a pygame Sound object for a sine wave."""
    sample_rate = pygame.mixer.get_init()[0]
    n_samples = int(round(duration * sample_rate))
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    max_sample = 2**(pygame.mixer.get_init()[1] - 1) - 1

    t = np.linspace(0., duration, n_samples, endpoint=False)
    
    # Simple sine wave
    wave = np.sin(2 * np.pi * frequency * t)
    
    # Simple decay envelope
    envelope = np.exp(-t * 5)
    
    wave *= envelope
    
    buf[:, 0] = (wave * max_sample * volume).astype(np.int16)
    buf[:, 1] = (wave * max_sample * volume).astype(np.int16)
    
    return pygame.mixer.Sound(buf)

# Create sound effects
hit_sound = generate_sound(440, 0.1) # A4 note
score_sound = generate_sound(880, 0.2) # A5 note
wall_bounce_sound = generate_sound(220, 0.08) # A3 note

# --- Game State ---
class GameState:
    START_MENU = 0
    PLAYING = 1
    GAME_OVER = 2

# --- Helper Functions ---
def draw_gradient_background():
    """Draws a vertical gradient background."""
    for y in range(SCREEN_HEIGHT):
        color_ratio = y / SCREEN_HEIGHT
        # Interpolate between top and bottom colors
        r = int(BG_COLOR_TOP.r * (1 - color_ratio) + BG_COLOR_BOTTOM.r * color_ratio)
        g = int(BG_COLOR_TOP.g * (1 - color_ratio) + BG_COLOR_BOTTOM.g * color_ratio)
        b = int(BG_COLOR_TOP.b * (1 - color_ratio) + BG_COLOR_BOTTOM.b * color_ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

def draw_text(text, font, color, center_pos):
    """Renders and centers text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_pos)
    screen.blit(text_surface, text_rect)

# --- Game Variables ---
game_state = GameState.START_MENU
match_winner = ""

# Game Objects
player_paddle = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(30, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH / 2 - BALL_RADIUS, SCREEN_HEIGHT / 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

ball_speed_x = 0
ball_speed_y = 0
player_speed = 0
opponent_speed = 0

player_score = 0
opponent_score = 0
player_sets = 0
opponent_sets = 0

start_button = pygame.Rect(SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT - 200, 250, 60)

# --- Game Functions ---
def ball_reset():
    """Resets the ball to the center with a random direction."""
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ball_speed_y = BALL_SPEED_Y_START * random.choice((1, -1))
    ball_speed_x = BALL_SPEED_X_START * random.choice((1, -1))

def reset_game():
    """Resets scores and sets for a new match."""
    global player_score, opponent_score, player_sets, opponent_sets
    player_score = 0
    opponent_score = 0
    player_sets = 0
    opponent_sets = 0
    ball_reset()

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == GameState.START_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    reset_game()
                    game_state = GameState.PLAYING
                    
        elif game_state == GameState.PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player_speed -= PADDLE_SPEED
                if event.key == pygame.K_s:
                    opponent_speed += PADDLE_SPEED
                if event.key == pygame.K_w:
                    opponent_speed -= PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player_speed += PADDLE_SPEED
                if event.key == pygame.K_s:
                    opponent_speed -= PADDLE_SPEED
                if event.key == pygame.K_w:
                    opponent_speed += PADDLE_SPEED

        elif game_state == GameState.GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_state = GameState.START_MENU

    # --- Game Logic & Drawing ---
    draw_gradient_background()

    if game_state == GameState.START_MENU:
        # Title
        draw_text("Hyper-Pong", title_font, UI_COLOR, (SCREEN_WIDTH / 2, 150))
        
        # Instructions
        draw_text("Player 1: UP/DOWN Arrows", instructions_font, UI_COLOR, (SCREEN_WIDTH / 2, 300))
        draw_text("Player 2: W/S Keys", instructions_font, UI_COLOR, (SCREEN_WIDTH / 2, 340))
        
        # Rules
        draw_text("First to 11 points wins a set.", instructions_font, UI_COLOR, (SCREEN_WIDTH / 2, 420))
        draw_text("You must win by 2 points.", instructions_font, UI_COLOR, (SCREEN_WIDTH / 2, 450))
        draw_text(f"Best of {SETS_TO_WIN_MATCH * 2 - 1} sets wins the match.", instructions_font, UI_COLOR, (SCREEN_WIDTH / 2, 480))
        
        # Start Button
        pygame.draw.rect(screen, ACCENT_COLOR, start_button, border_radius=15)
        draw_text("Start Game", ui_font, UI_COLOR, start_button.center)

    elif game_state == GameState.PLAYING:
        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision: Top and Bottom walls
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            wall_bounce_sound.play()
            ball_speed_y *= -1

        # Ball collision: Paddles
        if ball.colliderect(player_paddle):
            if abs(ball.right - player_paddle.left) < 10:
                ball_speed_x *= -1
            elif abs(ball.bottom - player_paddle.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
            elif abs(ball.top - player_paddle.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1
            hit_sound.play()
            
        if ball.colliderect(opponent_paddle):
            if abs(ball.left - opponent_paddle.right) < 10:
                ball_speed_x *= -1
            elif abs(ball.bottom - opponent_paddle.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
            elif abs(ball.top - opponent_paddle.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1
            hit_sound.play()

        # Score checking
        if ball.left <= 0:
            player_score += 1
            score_sound.play()
            ball_reset()
        if ball.right >= SCREEN_WIDTH:
            opponent_score += 1
            score_sound.play()
            ball_reset()

        # Check for set win
        if player_score >= WINNING_SCORE and player_score >= opponent_score + 2:
            player_sets += 1
            player_score, opponent_score = 0, 0
        if opponent_score >= WINNING_SCORE and opponent_score >= player_score + 2:
            opponent_sets += 1
            player_score, opponent_score = 0, 0
            
        # Check for match win
        if player_sets >= SETS_TO_WIN_MATCH:
            match_winner = "Player 1"
            game_state = GameState.GAME_OVER
        if opponent_sets >= SETS_TO_WIN_MATCH:
            match_winner = "Player 2"
            game_state = GameState.GAME_OVER

        # Paddle movement and boundaries
        player_paddle.y += player_speed
        if player_paddle.top <= 0: player_paddle.top = 0
        if player_paddle.bottom >= SCREEN_HEIGHT: player_paddle.bottom = SCREEN_HEIGHT

        opponent_paddle.y += opponent_speed
        if opponent_paddle.top <= 0: opponent_paddle.top = 0
        if opponent_paddle.bottom >= SCREEN_HEIGHT: opponent_paddle.bottom = SCREEN_HEIGHT

        # --- Drawing game elements ---
        pygame.draw.aaline(screen, UI_COLOR, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
        pygame.draw.rect(screen, PADDLE_COLOR, player_paddle, border_radius=10)
        pygame.draw.rect(screen, PADDLE_COLOR, opponent_paddle, border_radius=10)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)

        # Scores
        draw_text(f"{opponent_score}", score_font, UI_COLOR, (SCREEN_WIDTH / 4, 50))
        draw_text(f"{player_score}", score_font, UI_COLOR, (SCREEN_WIDTH * 3 / 4, 50))
        
        # Sets
        draw_text(f"Sets: {opponent_sets}", ui_font, UI_COLOR, (SCREEN_WIDTH / 4, 100))
        draw_text(f"Sets: {player_sets}", ui_font, UI_COLOR, (SCREEN_WIDTH * 3 / 4, 100))

    elif game_state == GameState.GAME_OVER:
        draw_text("Match Over", title_font, UI_COLOR, (SCREEN_WIDTH / 2, 200))
        draw_text(f"{match_winner} Wins!", score_font, ACCENT_COLOR, (SCREEN_WIDTH / 2, 350))
        draw_text("Click anywhere to return to the main menu", ui_font, UI_COLOR, (SCREEN_WIDTH / 2, 500))

    # --- Update Display ---
    pygame.display.flip()
    clock.tick(60)