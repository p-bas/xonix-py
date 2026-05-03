from collections import deque

import pygame

from config import GRID_WIDTH, GRID_HEIGHT, EMPTY, FILLED, TRAIL, COLORS


def _calculate_cell_size(screen_width, screen_height):
    cell_w = screen_width // GRID_WIDTH
    cell_h = screen_height // GRID_HEIGHT
    return max(1, min(cell_w, cell_h))


class BattleField:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for x in range(GRID_WIDTH):
            self.grid[0][x] = FILLED
            self.grid[GRID_HEIGHT - 1][x] = FILLED
        for y in range(GRID_HEIGHT):
            self.grid[y][0] = FILLED
            self.grid[y][GRID_WIDTH - 1] = FILLED

    def __getitem__(self, index):
        return self.grid[index]

    def flood_fill(self, enemies):
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
                    if not visited[ny][nx] and self.grid[ny][nx] == EMPTY:
                        visited[ny][nx] = True
                        queue.append((ny, nx))

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == EMPTY and not visited[y][x]:
                    self.grid[y][x] = FILLED
                if self.grid[y][x] == TRAIL:
                    self.grid[y][x] = FILLED

    def calculate_coverage(self):
        filled = 0
        total = (GRID_WIDTH - 2) * (GRID_HEIGHT - 2)
        for y in range(1, GRID_HEIGHT - 1):
            for x in range(1, GRID_WIDTH - 1):
                if self.grid[y][x] == FILLED:
                    filled += 1
        return (filled * 100) / total

    def consume_life(self, player):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == TRAIL:
                    self.grid[y][x] = EMPTY
        player.reset()

    def draw(self, screen, player, enemies):
        screen_width, screen_height = screen.get_size()
        cell_size = _calculate_cell_size(screen_width, screen_height)
        screen.fill((0, 0, 0))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = COLORS[self.grid[y][x]]
                pygame.draw.rect(
                    screen, color,
                    (x * cell_size, y * cell_size, cell_size, cell_size),
                )

        player.draw(screen, cell_size)
        for enemy in enemies:
            enemy.draw(screen, cell_size)
