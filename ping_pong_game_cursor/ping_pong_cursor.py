import sys
import pygame

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 560
FPS = 60

# Professional Palette
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
PADDLE_COLOR = (70, 130, 180)
BALL_COLOR = (255, 215, 0)
NET_COLOR = (100, 100, 100)
MENU_BG = (20, 25, 35)

# Physics Settings
PADDLE_WIDTH, PADDLE_HEIGHT = 12, 90
PADDLE_SPEED = 10
PADDLE_MARGIN = 30

BALL_SIZE = 12
BALL_SPEED_INITIAL = 5
BALL_SPEED_MAX = 12
ANGLE_MULTIPLIER = 0.12  # Lower intensity for smoother vertical bounce
BALL_DY_MAX = 7

SCORE_LIMIT = 11
BEST_OF = 5

TOP_BAR_H = 60
PLAY_Y = TOP_BAR_H
PLAY_H = WINDOW_HEIGHT - TOP_BAR_H
PLAY_BOTTOM = PLAY_Y + PLAY_H

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def clamp(value, low, high):
    return max(low, min(high, value))

def check_game_won(score_a, score_b):
    """Win by 2 rule implementation."""
    if (score_a >= SCORE_LIMIT or score_b >= SCORE_LIMIT) and abs(score_a - score_b) >= 2:
        return True
    return False

# -----------------------------------------------------------------------------
# MENU SYSTEM
# -----------------------------------------------------------------------------
def run_menu(screen, font, title_font, best_result):
    btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 110, WINDOW_HEIGHT - 120, 220, 50)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos):
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return True
                if event.key == pygame.K_ESCAPE: return False

        screen.fill(MENU_BG)
        title = title_font.render("PRO PING-PONG", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 80))

        ctrls = font.render("P1: W/S  |  P2: Up/Down", True, WHITE)
        screen.blit(ctrls, (WINDOW_WIDTH // 2 - ctrls.get_width() // 2, 200))

        rules = font.render(f"Best of {BEST_OF} | 11 pts (Win by 2)", True, (150, 150, 150))
        screen.blit(rules, (WINDOW_WIDTH // 2 - rules.get_width() // 2, 250))

        best = font.render(best_result, True, (255, 215, 0))
        screen.blit(best, (WINDOW_WIDTH // 2 - best.get_width() // 2, 320))

        # Start Button
        m_pos = pygame.mouse.get_pos()
        color = (90, 150, 220) if btn_rect.collidepoint(m_pos) else (60, 120, 180)
        pygame.draw.rect(screen, color, btn_rect, border_radius=5)
        txt = font.render("START GAME", True, WHITE)
        screen.blit(txt, (btn_rect.centerx - txt.get_width() // 2, btn_rect.centery - txt.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

# -----------------------------------------------------------------------------
# CORE GAME LOOP
# -----------------------------------------------------------------------------
def run_game(screen, font, clock):
    # Setup Positions
    p1_y = float(PLAY_Y + (PLAY_H - PADDLE_HEIGHT) // 2)
    p2_y = float(PLAY_Y + (PLAY_H - PADDLE_HEIGHT) // 2)
    ball_x, ball_y = float(WINDOW_WIDTH // 2), float(PLAY_Y + PLAY_H // 2)
    ball_dx, ball_dy = float(BALL_SPEED_INITIAL), 3.0

    score_a, score_b = 0, 0
    sets_a, sets_b = 0, 0
    serve_cooldown = 60
    paddle_hit_cooldown = 0

    while True:
        # 1. EVENT HANDLING (Optimized: No pump(), cleaner queue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 0, 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return 0, 0

        # 2. KEYBOARD POLLING (Placed before physics to avoid "sticking")
        keys = pygame.key.get_pressed()
        
        # Player 1 (Left)
        if keys[pygame.K_w] and p1_y > PLAY_Y: p1_y -= PADDLE_SPEED
        if keys[pygame.K_s] and p1_y < (PLAY_BOTTOM - PADDLE_HEIGHT): p1_y += PADDLE_SPEED
        # Player 2 (Right)
        if keys[pygame.K_UP] and p2_y > PLAY_Y: p2_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and p2_y < (PLAY_BOTTOM - PADDLE_HEIGHT): p2_y += PADDLE_SPEED

        # 3. BALL MOVEMENT & COLLISION
        if serve_cooldown > 0:
            serve_cooldown -= 1
        else:
            ball_x += ball_dx
            ball_y += ball_dy

        # Wall Collision
        if ball_y <= PLAY_Y:
            ball_y = float(PLAY_Y)
            ball_dy *= -1
        elif ball_y >= (PLAY_BOTTOM - BALL_SIZE):
            ball_y = float(PLAY_BOTTOM - BALL_SIZE)
            ball_dy *= -1

        # Rects for collision
        rect_p1 = pygame.Rect(PADDLE_MARGIN, int(p1_y), PADDLE_WIDTH, PADDLE_HEIGHT)
        rect_p2 = pygame.Rect(WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH, int(p2_y), PADDLE_WIDTH, PADDLE_HEIGHT)
        rect_ball = pygame.Rect(int(ball_x), int(ball_y), BALL_SIZE, BALL_SIZE)

        if paddle_hit_cooldown > 0: paddle_hit_cooldown -= 1

        # Paddle Collision Logic
        if paddle_hit_cooldown == 0:
            # Left Paddle
            if ball_dx < 0 and rect_ball.colliderect(rect_p1):
                diff = (ball_y + BALL_SIZE / 2.0) - (p1_y + PADDLE_HEIGHT / 2.0)
                target_dy = clamp(diff * ANGLE_MULTIPLIER * 2.0, -BALL_DY_MAX, BALL_DY_MAX)
                ball_dy = clamp(0.6 * ball_dy + 0.4 * target_dy, -BALL_DY_MAX, BALL_DY_MAX)
                ball_dx = clamp(abs(ball_dx) + 0.3, BALL_SPEED_INITIAL, BALL_SPEED_MAX)
                ball_x = float(rect_p1.right + 2)
                paddle_hit_cooldown = 4 # Anti-vibration cooldown

            # Right Paddle
            elif ball_dx > 0 and rect_ball.colliderect(rect_p2):
                diff = (ball_y + BALL_SIZE / 2.0) - (p2_y + PADDLE_HEIGHT / 2.0)
                target_dy = clamp(diff * ANGLE_MULTIPLIER * 2.0, -BALL_DY_MAX, BALL_DY_MAX)
                ball_dy = clamp(0.6 * ball_dy + 0.4 * target_dy, -BALL_DY_MAX, BALL_DY_MAX)
                ball_dx = -clamp(abs(ball_dx) + 0.3, BALL_SPEED_INITIAL, BALL_SPEED_MAX)
                ball_x = float(rect_p2.left - BALL_SIZE - 2)
                paddle_hit_cooldown = 4

        # 4. SCORING & SETS
        if ball_x < 0 or ball_x > WINDOW_WIDTH:
            scored_by_a = (ball_x > WINDOW_WIDTH)
            if scored_by_a: score_a += 1
            else: score_b += 1

            if check_game_won(score_a, score_b):
                if score_a > score_b: sets_a += 1
                else: sets_b += 1
                score_a, score_b = 0, 0
                if sets_a >= 3 or sets_b >= 3: return sets_a, sets_b

            # Reset Ball State
            ball_x, ball_y = float(WINDOW_WIDTH // 2), float(PLAY_Y + PLAY_H // 2)
            ball_dx = float(BALL_SPEED_INITIAL if scored_by_a else -BALL_SPEED_INITIAL)
            ball_dy = 3.0
            serve_cooldown, paddle_hit_cooldown = 60, 0

        # 5. RENDERING
        screen.fill(BLACK)
        pygame.draw.rect(screen, MENU_BG, (0, 0, WINDOW_WIDTH, TOP_BAR_H))
        
        # Text Rendering
        s_txt = font.render(f"{score_a} - {score_b}", True, WHITE)
        screen.blit(s_txt, (WINDOW_WIDTH // 2 - s_txt.get_width() // 2, 10))
        set_txt = font.render(f"Sets: {sets_a} - {sets_b}", True, (200, 200, 200))
        screen.blit(set_txt, (WINDOW_WIDTH // 2 - set_txt.get_width() // 2, 35))

        # Net & Objects
        for y in range(PLAY_Y, WINDOW_HEIGHT, 20):
            pygame.draw.rect(screen, NET_COLOR, (WINDOW_WIDTH // 2 - 1, y, 2, 10))
        pygame.draw.rect(screen, PADDLE_COLOR, rect_p1)
        pygame.draw.rect(screen, PADDLE_COLOR, rect_p2)
        pygame.draw.ellipse(screen, BALL_COLOR, rect_ball)

        pygame.display.flip()
        clock.tick(FPS)

# -----------------------------------------------------------------------------
# MAIN ENTRY
# -----------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ping-Pong Vibe Edition - Final")
    font, title_font = pygame.font.SysFont("Arial", 28), pygame.font.SysFont("Arial", 60, bold=True)
    clock, best_result = pygame.time.Clock(), "Last Match: No record"

    while True:
        if not run_menu(screen, font, title_font, best_result): break
        s1, s2 = run_game(screen, font, clock)
        if s1 == 0 and s2 == 0: break
        winner = "Player 1" if s1 > s2 else "Player 2"
        best_result = f"Last: {winner} won {max(s1, s2)}:{min(s1, s2)}"

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()