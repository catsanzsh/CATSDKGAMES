import pygame
import tkinter as tk
from tkinter import messagebox
import random

# --- Pygame Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB) as you please
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PADDLE_COLOR = BLUE
BALL_COLOR = RED
BRICK_COLORS = [
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 255, 255),  # Cyan
    (255, 0, 255)   # Magenta
]

# Paddle properties
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 20
PADDLE_SPEED = 12  # Pixels per frame, to make it responsive

# Ball properties, this little ball
BALL_RADIUS = 10
INITIAL_BALL_SPEED_X = 5
INITIAL_BALL_SPEED_Y = -5

# Brick properties, stack them high!
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_HEIGHT = 25
BRICK_TOP_OFFSET = 50  # Space from top for bricks
BRICK_PADDING_HORIZONTAL = 5  # Horizontal padding between bricks and screen edge
BRICK_PADDING_VERTICAL = 5  # Vertical padding between bricks
BRICK_SPACING_HORIZONTAL = 5  # Horizontal space between bricks
BRICK_SPACING_VERTICAL = 5    # Vertical space between bricks

# Calculate actual brick width based on screen and columns
TOTAL_HORIZONTAL_SPACING = BRICK_PADDING_HORIZONTAL * 2 + BRICK_SPACING_HORIZONTAL * (BRICK_COLS - 1)
AVAILABLE_WIDTH_FOR_BRICKS = SCREEN_WIDTH - TOTAL_HORIZONTAL_SPACING
BRICK_WIDTH = AVAILABLE_WIDTH_FOR_BRICKS / BRICK_COLS


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 20  # A bit off the bottom

    def move(self, direction):
        self.rect.x += direction * PADDLE_SPEED
        # Keep the paddle on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.move(-1)
        if keys[pygame.K_RIGHT]:
            self.move(1)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2], pygame.SRCALPHA)  # SRCALPHA for transparency
        pygame.draw.circle(self.image, BALL_COLOR, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()  # Set initial position and speed

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_RADIUS
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_RADIUS  # Start the ball in the middle
        self.speed_x = INITIAL_BALL_SPEED_X * random.choice([-1, 1])  # Randomize initial horizontal direction for variety
        self.speed_y = INITIAL_BALL_SPEED_Y
        self.just_hit_paddle = False  # To prevent the paddle from sticking

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.just_hit_paddle = False  # Reset sticky prevention each frame

        # Wall collision
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
            # Nudge it back in if it's stuck
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.speed_y *= -1
            if self.rect.top < 0:
                self.rect.top = 0
        # Bottom wall is game over, not a bounce


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Add a little border to make the bricks stand out
        pygame.draw.rect(self.image, BLACK, self.image.get_rect(), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def create_bricks(all_sprites_group, bricks_group):
    """This function creates all the bricks."""
    for i in range(BRICK_ROWS):
        brick_color = BRICK_COLORS[i % len(BRICK_COLORS)]  # Cycle through colors
        for j in range(BRICK_COLS):
            x = BRICK_PADDING_HORIZONTAL + j * (BRICK_WIDTH + BRICK_SPACING_HORIZONTAL)
            y = BRICK_TOP_OFFSET + i * (BRICK_HEIGHT + BRICK_SPACING_VERTICAL)
            brick = Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, brick_color)
            all_sprites_group.add(brick)
            bricks_group.add(brick)
    return bricks_group


def run_pygame_breakout():
    """Runs the main Pygame Breakout loop."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout Game")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()

    paddle = Paddle()
    ball = Ball()

    all_sprites.add(paddle)
    all_sprites.add(ball)

    create_bricks(all_sprites, bricks)

    score = 0
    lives = 3  # You get three shots!

    font_style = pygame.font.match_font('arial')  # Find a basic font
    if not font_style:  # If Arial isn't there, use default
        font_style = None
    font = pygame.font.Font(font_style, 24)

    running = True
    game_over_flag = False
    game_won_flag = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over_flag or game_won_flag:  # Restart on any key if game ended
                    # Reset everything
                    game_over_flag = False
                    game_won_flag = False
                    score = 0
                    lives = 3
                    ball.reset()
                    # Recreate bricks since they are all gone
                    for brick_sprite in bricks:
                        brick_sprite.kill()
                    create_bricks(all_sprites, bricks)

        if not game_over_flag and not game_won_flag:
            keys = pygame.key.get_pressed()
            paddle.update(keys)
            ball.update()

            # Ball and Paddle collision
            if pygame.sprite.collide_rect(ball, paddle) and not ball.just_hit_paddle:
                # Make sure ball is above paddle and moving down
                if ball.rect.bottom >= paddle.rect.top and ball.speed_y > 0:
                    ball.speed_y *= -1
                    ball.rect.bottom = paddle.rect.top - 1  # Prevent sticking
                    # Change ball's horizontal speed based on where it hit the paddle
                    offset = (ball.rect.centerx - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
                    ball.speed_x += offset * 2
                    # Cap ball speed_x to prevent it from going too fast horizontally
                    ball.speed_x = max(-abs(INITIAL_BALL_SPEED_X * 1.5), min(abs(INITIAL_BALL_SPEED_X * 1.5), ball.speed_x))
                    ball.just_hit_paddle = True

            # Ball and Brick collision
            brick_hit_list = pygame.sprite.spritecollide(ball, bricks, True)  # True to kill the brick
            for brick_hit in brick_hit_list:
                ball.speed_y *= -1
                score += 10  # Earn some points!
                # Small nudge to prevent multi-hits on the same frame if ball is fast
                if ball.speed_y > 0:  # If moving down after bounce
                    ball.rect.top = brick_hit.rect.bottom
                elif ball.speed_y < 0:  # If moving up after bounce
                    ball.rect.bottom = brick_hit.rect.top

            # Ball goes off bottom screen - you lose a life
            if ball.rect.top > SCREEN_HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over_flag = True
                else:
                    ball.reset()

            # Win condition - no more bricks!
            if not bricks:
                game_won_flag = True

        # --- Drawing ---
        screen.fill(BLACK)  # Black background
        all_sprites.draw(screen)  # Draw all the sprites

        # Score and Lives display
        score_text = font.render(f"SCORE: {score}", True, WHITE)
        lives_text = font.render(f"LIVES: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        if game_over_flag:
            msg_text = font.render("Game Over! Press any key to restart.", True, RED)
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(msg_text, msg_rect)

        if game_won_flag:
            msg_text = font.render("Congratulations, you won! Press any key to play again.", True, GREEN)
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(msg_text, msg_rect)

        pygame.display.flip()  # Update the entire screen
        clock.tick(FPS)  # Maintain 60 FPS

    pygame.quit()


def start_game_from_tkinter():
    """This function starts the Pygame part."""
    root.destroy()  # Close the Tkinter window
    run_pygame_breakout()  # Run the actual game


if __name__ == '__main__':
    # This is the Tkinter part, a simple launcher
    root = tk.Tk()
    root.title("Breakout Game Launcher")
    root.geometry("300x150")  # A small window

    label = tk.Label(root, text="Ready to play Breakout?", font=("Arial", 12), pady=20)
    label.pack()

    start_button = tk.Button(root, text="Start Game", command=start_game_from_tkinter, font=("Arial", 14), bg="red", fg="white", pady=10)
    start_button.pack()

    # Center this window
    window_width = 300
    window_height = 150
    screen_width_tk = root.winfo_screenwidth()
    screen_height_tk = root.winfo_screenheight()
    center_x = int(screen_width_tk / 2 - window_width / 2)
    center_y = int(screen_height_tk / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.mainloop()
