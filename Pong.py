import tkinter as tk
import random

# Game constants - Essential for defining the game's dimensions and properties
WIDTH = 600  # Width of the game window
HEIGHT = 400  # Height of the game window
PAD_WIDTH = 10  # Width of the paddles
PAD_HEIGHT = 100  # Height of the paddles
BALL_RADIUS = 8  # Radius of the ball
PADDLE_SPEED = 30  # Speed at which paddles move
BALL_INITIAL_SPEED_X = 3  # Initial horizontal speed of the ball
BALL_INITIAL_SPEED_Y = 3  # Initial vertical speed of the ball

# Scores for both players
player1_score = 0
player2_score = 0

# Global variables for ball's horizontal and vertical speed
ball_dx = BALL_INITIAL_SPEED_X
ball_dy = BALL_INITIAL_SPEED_Y

def init_ball():
    """Resets the ball to the center with a random direction."""
    global ball_dx, ball_dy
    canvas.coords(ball, WIDTH/2 - BALL_RADIUS, HEIGHT/2 - BALL_RADIUS, WIDTH/2 + BALL_RADIUS, HEIGHT/2 + BALL_RADIUS)
    # Set random initial direction for the ball
    ball_dx = random.choice([BALL_INITIAL_SPEED_X, -BALL_INITIAL_SPEED_X])
    ball_dy = random.choice([BALL_INITIAL_SPEED_Y, -BALL_INITIAL_SPEED_Y])

def move_paddles(event):
    """Moves the paddles based on key presses."""
    key = event.keysym
    # Player 1 (Left Paddle) - W for up, S for down
    p1_coords = canvas.coords(paddle1)
    if key == "w":
        if p1_coords[1] > 0:  # Prevent paddle from going off the top
            canvas.move(paddle1, 0, -PADDLE_SPEED)
    elif key == "s":
        if p1_coords[3] < HEIGHT:  # Prevent paddle from going off the bottom
            canvas.move(paddle1, 0, PADDLE_SPEED)

    # Player 2 (Right Paddle) - Up arrow for up, Down arrow for down
    p2_coords = canvas.coords(paddle2)
    if key == "Up":
        if p2_coords[1] > 0:  # Prevent paddle from going off the top
            canvas.move(paddle2, 0, -PADDLE_SPEED)
    elif key == "Down":
        if p2_coords[3] < HEIGHT:  # Prevent paddle from going off the bottom
            canvas.move(paddle2, 0, PADDLE_SPEED)

def update_score_display():
    """Updates the score display on the screen."""
    canvas.itemconfig(score_text, text=f"{player1_score}  |  {player2_score}")

def game_loop():
    """The main game loop that updates the game state."""
    global ball_dx, ball_dy, player1_score, player2_score

    # Move the ball
    canvas.move(ball, ball_dx, ball_dy)
    ball_pos = canvas.coords(ball)  # Get current ball position [x1, y1, x2, y2]

    # Check for collision with top and bottom walls
    if ball_pos[1] <= 0 or ball_pos[3] >= HEIGHT:
        ball_dy *= -1  # Reverse vertical direction

    # Get paddle positions
    p1_pos = canvas.coords(paddle1)
    p2_pos = canvas.coords(paddle2)

    # Check for collision with left paddle
    if ball_dx < 0 and \
       ball_pos[0] <= p1_pos[2] and \
       ball_pos[2] >= p1_pos[0] and \
       ball_pos[3] >= p1_pos[1] and \
       ball_pos[1] <= p1_pos[3]:
        ball_dx *= -1  # Reverse horizontal direction
        # Adjust ball's vertical speed based on where it hits the paddle
        paddle_center_y = (p1_pos[1] + p1_pos[3]) / 2
        ball_center_y = (ball_pos[1] + ball_pos[3]) / 2
        relative_intersect_y = (paddle_center_y - ball_center_y) / (PAD_HEIGHT / 2)
        ball_dy = -relative_intersect_y * abs(ball_dx)

    # Check for collision with right paddle
    if ball_dx > 0 and \
       ball_pos[2] >= p2_pos[0] and \
       ball_pos[0] <= p2_pos[2] and \
       ball_pos[3] >= p2_pos[1] and \
       ball_pos[1] <= p2_pos[3]:
        ball_dx *= -1  # Reverse horizontal direction
        # Adjust ball's vertical speed based on where it hits the paddle
        paddle_center_y = (p2_pos[1] + p2_pos[3]) / 2
        ball_center_y = (ball_pos[1] + ball_pos[3]) / 2
        relative_intersect_y = (paddle_center_y - ball_center_y) / (PAD_HEIGHT / 2)
        ball_dy = -relative_intersect_y * abs(ball_dx)

    # Check if ball goes out of bounds
    if ball_pos[0] <= 0:  # Ball goes past left side, Player 2 scores
        player2_score += 1
        update_score_display()
        init_ball()
    elif ball_pos[2] >= WIDTH:  # Ball goes past right side, Player 1 scores
        player1_score += 1
        update_score_display()
        init_ball()

    # Schedule the next update
    root.after(16, game_loop)  # Approximately 60 FPS

# --- Setup the window and canvas ---
root = tk.Tk()
root.title("Pong Game")
root.resizable(False, False)  # Prevent resizing the window

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")  # Create canvas with black background
canvas.pack()

# Create paddles
# Left paddle (Player 1)
paddle1 = canvas.create_rectangle(20, HEIGHT/2 - PAD_HEIGHT/2, 20 + PAD_WIDTH, HEIGHT/2 + PAD_HEIGHT/2, fill="white")
# Right paddle (Player 2)
paddle2 = canvas.create_rectangle(WIDTH - 20 - PAD_WIDTH, HEIGHT/2 - PAD_HEIGHT/2, WIDTH - 20, HEIGHT/2 + PAD_HEIGHT/2, fill="white")

# Create the ball
ball = canvas.create_oval(WIDTH/2 - BALL_RADIUS, HEIGHT/2 - BALL_RADIUS, WIDTH/2 + BALL_RADIUS, HEIGHT/2 + BALL_RADIUS, fill="cyan")

# Create the score display
score_text = canvas.create_text(WIDTH/2, 30, text="0  |  0", fill="white", font=("Consolas", 24, "bold"))

# Initialize ball position and speed
init_ball()

# Bind key presses to paddle movement
root.bind("<KeyPress>", move_paddles)
canvas.focus_set()  # Ensure canvas receives key events

# Start the game loop
game_loop()

# Run the tkinter main loop
root.mainloop()
