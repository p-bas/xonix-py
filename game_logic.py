from collections import deque

import pygame

from config import GRID_WIDTH, GRID_HEIGHT, EMPTY, FILLED, TRAIL, LEVELS, COLORS


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
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
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


def start_level(player, level):
    from enemy import Enemy
    field = create_field()
    player.reset()
    enemies = [Enemy() for _ in range(LEVELS[level]["enemies"])]
    return field, enemies


def consume_life(field, player):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if field[y][x] == TRAIL:
                field[y][x] = EMPTY
    player.reset()


def calculate_cell_size(screen_width, screen_height):
    cell_w = screen_width // GRID_WIDTH
    cell_h = screen_height // GRID_HEIGHT
    return max(1, min(cell_w, cell_h))


def draw_hud(screen, field, level, lives):
    font = pygame.font.SysFont(None, 24)
    percent = calculate_coverage(field)
    win = LEVELS[level]["win"] if level < len(LEVELS) else None
    lines = [
        f"Level: {level}",
        f"Lives: {lives}",
        f"Coverage: {percent:.1f}%",
        f"Target: {win}%",
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (10, 10 + i * 18))


def draw_field(screen, field, player, enemies):
    screen_width, screen_height = screen.get_size()
    cell_size = calculate_cell_size(screen_width, screen_height)
    screen.fill((0, 0, 0))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = COLORS[field[y][x]]
            pygame.draw.rect(
                screen, color,
                (x * cell_size, y * cell_size, cell_size, cell_size),
            )
    pygame.draw.rect(
        screen,
        COLORS["player"],
        (player.x * cell_size, player.y * cell_size, cell_size, cell_size),
    )
    for enemy in enemies:
        pygame.draw.circle(
            screen,
            COLORS["enemy"],
            (
                enemy.x * cell_size + cell_size // 2,
                enemy.y * cell_size + cell_size // 2,
            ),
            cell_size // 2,
        )
