import tkinter as tk
import random
import time

# --- Constants ---
WIDTH = 600
HEIGHT = 400
FPS = 60
UPDATE_DELAY = 1000 // FPS

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 20
PLAYER_SPEED = 8
PLAYER_COLOR = "lime green"
PLAYER_Y_OFFSET = 30

BULLET_WIDTH = 4
BULLET_HEIGHT = 12
PLAYER_BULLET_SPEED = 10
PLAYER_BULLET_COLOR = "cyan"
MAX_PLAYER_BULLETS = 3

ENEMY_BULLET_SPEED = 7
ENEMY_BULLET_COLOR = "orange red"

ENEMY_ROWS = 5
ENEMY_COLS = 10
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 20
ENEMY_X_SPACING = 15
ENEMY_Y_SPACING = 10
ENEMY_TOP_MARGIN = 40
ENEMY_INITIAL_X_SPEED = 2
ENEMY_DROP_DISTANCE = 15
ENEMY_SHOOT_CHANCE_BASE = 0.002
ENEMY_COLORS = ["magenta", "yellow", "turquoise", "pink", "white"]

SCORE_FONT = ("Consolas", 16, "bold")
MESSAGE_FONT = ("Consolas", 30, "bold")

class SpaceInvadersGame:
    def __init__(self, master):
        self.master = master
        master.title("Space Invaders - Synthesized by CATSEEK R1")
        master.geometry(f"{WIDTH}x{HEIGHT}")
        master.resizable(False, False)
        master.configure(bg="black")

        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.game_running = False
        self.game_over_message_id = None
        self.enemy_x_speed = ENEMY_INITIAL_X_SPEED
        self.enemy_shoot_chance_multiplier = 1.0

        self.player = None
        self.player_bullets = []
        self.enemies = []
        self.enemy_bullets = []

        self.move_left_pressed = False
        self.move_right_pressed = False

        self.score_display = self.canvas.create_text(10, 10, anchor="nw", fill="white", font=SCORE_FONT)
        self.lives_display = self.canvas.create_text(WIDTH - 10, 10, anchor="ne", fill="white", font=SCORE_FONT)
        
        self.bind_keys()
        self.start_game()

    def bind_keys(self):
        self.master.bind("<KeyPress-Left>", lambda e: self.set_move_left(True))
        self.master.bind("<KeyRelease-Left>", lambda e: self.set_move_left(False))
        self.master.bind("<KeyPress-Right>", lambda e: self.set_move_right(True))
        self.master.bind("<KeyRelease-Right>", lambda e: self.set_move_right(False))
        self.master.bind("<KeyPress-a>", lambda e: self.set_move_left(True))
        self.master.bind("<KeyRelease-a>", lambda e: self.set_move_left(False))
        self.master.bind("<KeyPress-d>", lambda e: self.set_move_right(True))
        self.master.bind("<KeyRelease-d>", lambda e: self.set_move_right(False))
        self.master.bind("<KeyPress-space>", self.player_shoot)
        self.master.bind("<KeyPress-r>", self.restart_game_if_over)

    def set_move_left(self, state):
        self.move_left_pressed = state

    def set_move_right(self, state):
        self.move_right_pressed = state

    def start_game(self):
        self.canvas.delete("all")
        self.score_display = self.canvas.create_text(10, 10, anchor="nw", fill="white", font=SCORE_FONT, text=f"Score: {self.score}")
        self.lives_display = self.canvas.create_text(WIDTH - 10, 10, anchor="ne", fill="white", font=SCORE_FONT, text=f"Lives: {self.lives}")

        self.score = 0
        self.lives = 3
        self.player_bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.enemy_x_speed = ENEMY_INITIAL_X_SPEED
        self.enemy_shoot_chance_multiplier = 1.0
        
        if self.game_over_message_id:
            self.canvas.delete(self.game_over_message_id)
            self.game_over_message_id = None

        self.create_player()
        self.create_enemies()
        self.update_ui_displays()
        
        self.game_running = True
        self.game_loop()

    def restart_game_if_over(self, event=None):
        if not self.game_running:
            self.start_game()

    def create_player(self):
        x = (WIDTH - PLAYER_WIDTH) / 2
        y = HEIGHT - PLAYER_HEIGHT - PLAYER_Y_OFFSET
        self.player = {'id': self.canvas.create_rectangle(x, y, x + PLAYER_WIDTH, y + PLAYER_HEIGHT, fill=PLAYER_COLOR, outline=""),
                       'x': x, 'y': y}

    def create_enemies(self):
        total_grid_width = ENEMY_COLS * ENEMY_WIDTH + (ENEMY_COLS - 1) * ENEMY_X_SPACING
        start_x = (WIDTH - total_grid_width) / 2
        
        for r in range(ENEMY_ROWS):
            row_enemies = []
            for c in range(ENEMY_COLS):
                x = start_x + c * (ENEMY_WIDTH + ENEMY_X_SPACING)
                y = ENEMY_TOP_MARGIN + r * (ENEMY_HEIGHT + ENEMY_Y_SPACING)
                color = ENEMY_COLORS[r % len(ENEMY_COLORS)]
                enemy_id = self.canvas.create_rectangle(x, y, x + ENEMY_WIDTH, y + ENEMY_HEIGHT, fill=color, outline="")
                row_enemies.append({'id': enemy_id, 'x': x, 'y': y, 'w': ENEMY_WIDTH, 'h': ENEMY_HEIGHT, 'alive': True, 'row': r, 'col': c})
            self.enemies.append(row_enemies)

    def game_loop(self):
        if not self.game_running:
            return

        self.update_player()
        self.update_player_bullets()
        self.update_enemies()
        self.update_enemy_bullets()
        self.check_collisions()
        self.draw_elements()
        self.update_ui_displays()
        self.check_game_state()

        if self.game_running:
            self.master.after(UPDATE_DELAY, self.game_loop)

    def update_player(self):
        if self.move_left_pressed and self.player['x'] > 0:
            self.player['x'] -= PLAYER_SPEED
        if self.move_right_pressed and self.player['x'] + PLAYER_WIDTH < WIDTH:
            self.player['x'] += PLAYER_SPEED
        
        self.canvas.coords(self.player['id'], self.player['x'], self.player['y'], 
                           self.player['x'] + PLAYER_WIDTH, self.player['y'] + PLAYER_HEIGHT)

    def player_shoot(self, event=None):
        if self.game_running and len(self.player_bullets) < MAX_PLAYER_BULLETS:
            x = self.player['x'] + PLAYER_WIDTH / 2 - BULLET_WIDTH / 2
            y = self.player['y'] - BULLET_HEIGHT
            bullet_id = self.canvas.create_rectangle(x, y, x + BULLET_WIDTH, y + BULLET_HEIGHT, fill=PLAYER_BULLET_COLOR, outline="")
            self.player_bullets.append({'id': bullet_id, 'x': x, 'y': y})

    def update_player_bullets(self):
        for bullet in list(self.player_bullets):
            bullet['y'] -= PLAYER_BULLET_SPEED
            if bullet['y'] < 0:
                self.canvas.delete(bullet['id'])
                self.player_bullets.remove(bullet)
            else:
                self.canvas.coords(bullet['id'], bullet['x'], bullet['y'],
                                   bullet['x'] + BULLET_WIDTH, bullet['y'] + BULLET_HEIGHT)

    def update_enemies(self):
        if not any(enemy['alive'] for row in self.enemies for enemy in row):
            return

        move_down = False
        min_x = WIDTH
        max_x = 0
        lowest_y = 0

        for r_idx, row in enumerate(self.enemies):
            for c_idx, enemy in enumerate(row):
                if enemy['alive']:
                    min_x = min(min_x, enemy['x'])
                    max_x = max(max_x, enemy['x'] + ENEMY_WIDTH)
                    lowest_y = max(lowest_y, enemy['y'] + ENEMY_HEIGHT)

        if max_x + self.enemy_x_speed > WIDTH or min_x + self.enemy_x_speed < 0:
            self.enemy_x_speed *= -1
            move_down = True

        for r_idx, row in enumerate(self.enemies):
            for c_idx, enemy in enumerate(row):
                if enemy['alive']:
                    enemy['x'] += self.enemy_x_speed
                    if move_down:
                        enemy['y'] += ENEMY_DROP_DISTANCE
                    self.canvas.coords(enemy['id'], enemy['x'], enemy['y'],
                                       enemy['x'] + ENEMY_WIDTH, enemy['y'] + ENEMY_HEIGHT)
                    
                    is_bottom_most_in_col = True
                    for check_r_idx in range(r_idx + 1, ENEMY_ROWS):
                        if self.enemies[check_r_idx][c_idx]['alive']:
                            is_bottom_most_in_col = False
                            break
                    
                    if is_bottom_most_in_col and random.random() < (ENEMY_SHOOT_CHANCE_BASE * self.enemy_shoot_chance_multiplier):
                        self.enemy_shoot(enemy)
        
        if lowest_y >= self.player['y']:
            self.end_game(won=False, reason="Invaders reached base!")

    def enemy_shoot(self, enemy):
        x = enemy['x'] + ENEMY_WIDTH / 2 - BULLET_WIDTH / 2
        y = enemy['y'] + ENEMY_HEIGHT
        bullet_id = self.canvas.create_rectangle(x, y, x + BULLET_WIDTH, y + BULLET_HEIGHT, fill=ENEMY_BULLET_COLOR, outline="")
        self.enemy_bullets.append({'id': bullet_id, 'x': x, 'y': y})

    def update_enemy_bullets(self):
        for bullet in list(self.enemy_bullets):
            bullet['y'] += ENEMY_BULLET_SPEED
            if bullet['y'] + BULLET_HEIGHT > HEIGHT:
                self.canvas.delete(bullet['id'])
                self.enemy_bullets.remove(bullet)
            else:
                self.canvas.coords(bullet['id'], bullet['x'], bullet['y'],
                                   bullet['x'] + BULLET_WIDTH, bullet['y'] + BULLET_HEIGHT)

    def check_collisions(self):
        num_enemies_alive_start = sum(e['alive'] for r in self.enemies for e in r)

        for bullet in list(self.player_bullets):
            bullet_coords = (bullet['x'], bullet['y'], BULLET_WIDTH, BULLET_HEIGHT)
            for row in self.enemies:
                for enemy in row:
                    if enemy['alive']:
                        enemy_coords = (enemy['x'], enemy['y'], ENEMY_WIDTH, ENEMY_HEIGHT)
                        if self.is_overlapping(bullet_coords, enemy_coords):
                            self.canvas.delete(bullet['id'])
                            if bullet in self.player_bullets: self.player_bullets.remove(bullet)
                            self.canvas.delete(enemy['id'])
                            enemy['alive'] = False
                            self.score += (ENEMY_ROWS - enemy['row']) * 10
                            break
                else:
                    continue
                break

        num_enemies_alive_end = sum(e['alive'] for r in self.enemies for e in r)
        if num_enemies_alive_start > 0 and num_enemies_alive_end < num_enemies_alive_start:
            self.enemy_shoot_chance_multiplier = float(num_enemies_alive_start) / max(1, num_enemies_alive_end)
            if abs(self.enemy_x_speed) < 5:
                 self.enemy_x_speed *= 1.02

        player_coords = (self.player['x'], self.player['y'], PLAYER_WIDTH, PLAYER_HEIGHT)
        for bullet in list(self.enemy_bullets):
            bullet_coords = (bullet['x'], bullet['y'], BULLET_WIDTH, BULLET_HEIGHT)
            if self.is_overlapping(bullet_coords, player_coords):
                self.canvas.delete(bullet['id'])
                if bullet in self.enemy_bullets: self.enemy_bullets.remove(bullet)
                self.lives -= 1
                if self.lives <= 0:
                    self.end_game(won=False, reason="No lives left!")
                break 
        
        for row in self.enemies:
            for enemy in row:
                if enemy['alive']:
                    enemy_coords = (enemy['x'], enemy['y'], ENEMY_WIDTH, ENEMY_HEIGHT)
                    if self.is_overlapping(enemy_coords, player_coords):
                        self.end_game(won=False, reason="Invader touched you!")
                        return

    def is_overlapping(self, item1_coords, item2_coords):
        x1, y1, w1, h1 = item1_coords
        x2, y2, w2, h2 = item2_coords
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

    def draw_elements(self):
        pass

    def update_ui_displays(self):
        self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_display, text=f"Lives: {self.lives}")

    def check_game_state(self):
        if not any(enemy['alive'] for row in self.enemies for enemy in row) and self.game_running:
            self.end_game(won=True, reason="All invaders defeated!")

    def end_game(self, won, reason):
        self.game_running = False
        if won:
            message = "VICTORY!"
            color = "green"
        else:
            message = "GAME OVER!"
            color = "red"
        if self.game_over_message_id:
            self.canvas.delete(self.game_over_message_id)
        final_message = f"{message}\n{reason}\nScore: {self.score}\nPress 'R' to restart"
        self.game_over_message_id = self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text=final_message,
                                                            font=MESSAGE_FONT, fill=color, justify=tk.CENTER, anchor="center")

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceInvadersGame(root)
    root.mainloop()
