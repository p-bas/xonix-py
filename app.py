import pygame
import random
from collections import deque

# ---------------- CONFIG ----------------
STATE_PLAYING = 0
STATE_DEAD = 1
STATE_WIN = 2

WIN_PERCENT = 80

CELL_SIZE = 10
GRID_WIDTH = 150
GRID_HEIGHT = 80

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS = 50

EMPTY = 0
FILLED = 1
TRAIL = 2

# Colors
COLORS = {
    EMPTY: (0, 0, 0),
    FILLED: (0, 120, 255),
    TRAIL: (255, 255, 0),
    "player": (0, 255, 0),
    "enemy": (255, 0, 0),
}

LEVELS = [
    {"fps": 40, "enemies": 2, "win": 65},
    {"fps": 41, "enemies": 2, "win": 70},
    {"fps": 41, "enemies": 2, "win": 70},
    {"fps": 42, "enemies": 3, "win": 65},
    {"fps": 42, "enemies": 3, "win": 70},
    {"fps": 43, "enemies": 3, "win": 75},
    {"fps": 43, "enemies": 4, "win": 70},
    {"fps": 44, "enemies": 4, "win": 75},
    {"fps": 44, "enemies": 4, "win": 80},
    {"fps": 46, "enemies": 5, "win": 75},
    {"fps": 48, "enemies": 5, "win": 80},
]

# ----------------------------------------

class Enemy:
    def __init__(self):
        self.x = random.randint(2, GRID_WIDTH - 3)
        self.y = random.randint(2, GRID_HEIGHT - 3)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def move(self, field, tick_sound=None):
        reflected = False
        hit_x = field[self.y][self.x + self.dx] == FILLED
        hit_y = field[self.y + self.dy][self.x] == FILLED

        # Corner collision: reflect both directions
        if hit_x and hit_y:
            self.dx *= -1
            self.dy *= -1
            reflected = True
        else:
            # Reflect only the blocked axis
            if hit_x:
                self.dx *= -1
                reflected = True
            if hit_y:
                self.dy *= -1
                reflected = True

        if reflected and tick_sound:
            tick_sound.play()

        self.x += self.dx
        self.y += self.dy

class Player:
    def __init__(self):
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT - 2
        self.dx = 0
        self.dy = 0
        self.drawing = False

    def update(self, field, sound=None):
        if self.dx == 0 and self.dy == 0:
            return None

        nx = self.x + self.dx
        ny = self.y + self.dy

        # Prevent leaving field
        if nx < 0 or nx >= GRID_WIDTH or ny < 0 or ny >= GRID_HEIGHT:
            return None

        next_cell = field[ny][nx]

        # 🚫 Prevent moving back onto own trail (NO DEATH)
        if next_cell == TRAIL:
            return None

        # 🧱 Reached filled area
        if next_cell == FILLED:
            if self.drawing:
                # CLOSE THE CONTOUR:
                # convert last trail cell to filled
                field[self.y][self.x] = FILLED
                self.x = nx
                self.y = ny
                self.drawing = False
                return "closed"
            else:
                self.x = nx
                self.y = ny
                return None

        # 🟨 Move into empty area → draw trail
        if next_cell == EMPTY:
            is_filled = field[self.y][self.x] == FILLED
            field[self.y][self.x] = TRAIL if not is_filled else FILLED
            self.x = nx
            self.y = ny
            self.drawing = True
            # sound.play()
            return None


def draw_overlay(screen, text):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 64)
    small_font = pygame.font.SysFont(None, 32)

    text_surf = font.render(text, True, (255, 0, 0))
    hint_surf = small_font.render("Press R to Restart or ESC to Exit", True, (255, 255, 255))

    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    hint_rect = hint_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

    screen.blit(text_surf, text_rect)
    screen.blit(hint_surf, hint_rect)

def create_field():
    field = [[EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for x in range(GRID_WIDTH):
        field[0][x] = FILLED
        field[GRID_HEIGHT - 1][x] = FILLED
    for y in range(GRID_HEIGHT):
        field[y][0] = FILLED
        field[y][GRID_WIDTH - 1] = FILLED
    return field


def flood_fill(field, enemies):
    visited = [[False] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    queue = deque()

    for enemy in enemies:
        queue.append((enemy.y, enemy.x))
        visited[enemy.y][enemy.x] = True

    while queue:
        y, x = queue.popleft()
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                if not visited[ny][nx] and field[ny][nx] == EMPTY:
                    visited[ny][nx] = True
                    queue.append((ny, nx))

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if field[y][x] == EMPTY and not visited[y][x]:
                field[y][x] = FILLED
            if field[y][x] == TRAIL:
                field[y][x] = FILLED

def calculate_coverage(field):
    filled = 0
    total = (GRID_WIDTH - 2) * (GRID_HEIGHT - 2)

    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            if field[y][x] == FILLED:
                filled += 1

    return (filled * 100) / total

def draw_hud(screen, field, level):
    font = pygame.font.SysFont(None, 24)
    percent = calculate_coverage(field)
    win = LEVELS[level]["win"]

    lines = [
        f"Level: {level + 1}",
        f"Coverage: {percent:.1f}%",
        f"Target: {win}%",
    ]

    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (10, 10 + i * 18))


def start_level(level):
    field = create_field()
    player = Player()
    enemies = [Enemy() for _ in range(LEVELS[level]["enemies"])]
    return field, player, enemies

def main():
    state = STATE_PLAYING
    level = 0
    pygame.init()
    pygame.mixer.init()
    tick_sound = pygame.mixer.Sound("sounds/ball.wav")
    tick_sound.set_volume(0.25)

    win_sound = pygame.mixer.Sound("sounds/win.wav")
    win_sound.set_volume(0.7)

    fail_sound = pygame.mixer.Sound("sounds/fail.wav")
    fail_sound.set_volume(0.5)

    rub_sound = pygame.mixer.Sound("sounds/scratch.wav")
    rub_sound.set_volume(0.3)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Xonix (pygame)")
    clock = pygame.time.Clock()

    field, player, enemies = start_level(level)

    running = True
    while running:
        clock.tick(LEVELS[level]["fps"])

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False

          if state == STATE_WIN and event.type == pygame.KEYDOWN:
              if event.key == pygame.K_r:
                  level += 1
                  if level >= len(LEVELS):
                      state = STATE_WIN  # final win
                  else:
                      field, player, enemies = start_level(level)
                      state = STATE_PLAYING
              elif event.key == pygame.K_ESCAPE:
                  running = False
          
          if state == STATE_DEAD and event.type == pygame.KEYDOWN:
              if event.key == pygame.K_r:
                  level = 0
                  field, player, enemies = start_level(level)
                  state = STATE_PLAYING
              elif event.key == pygame.K_ESCAPE:
                  running = False

        if state == STATE_PLAYING:
          keys = pygame.key.get_pressed()
          player.dx = player.dy = 0
          if keys[pygame.K_LEFT]:
              player.dx = -1
          elif keys[pygame.K_RIGHT]:
              player.dx = 1
          elif keys[pygame.K_UP]:
              player.dy = -1
          elif keys[pygame.K_DOWN]:
              player.dy = 1

          result = player.update(field, rub_sound)

          if result == "closed":
              flood_fill(field, enemies)
              coverage = calculate_coverage(field)
              if coverage >= LEVELS[level]["win"]:
                state = STATE_WIN
                win_sound.play()

        # elif result == "dead":
        #    field = create_field()
        #    player = Player()
        #    continue


        if state == STATE_PLAYING:
          for enemy in enemies:
              enemy.move(field, tick_sound)

              if enemy.x == player.x and enemy.y == player.y:
                  state = STATE_DEAD
                  fail_sound.play()
                  break

              if player.drawing and field[enemy.y][enemy.x] == TRAIL:
                  state = STATE_DEAD
                  fail_sound.play()
                  break

        screen.fill((0, 0, 0))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = COLORS[field[y][x]]
                pygame.draw.rect(
                    screen,
                    color,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

        pygame.draw.rect(
            screen,
            COLORS["player"],
            (player.x * CELL_SIZE, player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

        for enemy in enemies:
            pygame.draw.circle(
                screen,
                COLORS["enemy"],
                (
                    enemy.x * CELL_SIZE + CELL_SIZE // 2,
                    enemy.y * CELL_SIZE + CELL_SIZE // 2,
                ),
                CELL_SIZE // 2,
            )

        draw_hud(screen, field, level)

        if state == STATE_DEAD:
            draw_overlay(screen, "YOU ARE DEAD")

        if state == STATE_WIN:
            if level < len(LEVELS):
                draw_overlay(screen, f"LEVEL {level + 1} COMPLETE")
            else:
                draw_overlay(screen, "YOU COMPLETED ALL LEVELS!")

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
