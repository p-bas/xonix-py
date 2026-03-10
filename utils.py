import pygame
from collections import deque
from config import EMPTY, FILLED, TRAIL, GRID_WIDTH, GRID_HEIGHT, WIDTH, HEIGHT, LEVELS

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