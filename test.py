import logging
from pathlib import Path
import pygame
from collections import deque

from config import WIDTH, HEIGHT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, COLORS, LEVELS, STATE_PLAYING, STATE_WIN, STATE_DEAD, EMPTY, FILLED, TRAIL
from resources import ResourceLoader, Sound, AudioManager

logging.basicConfig(level=logging.INFO)

from enemy import Enemy
from player import Player
from display_utils import DisplayManager



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


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    dm = DisplayManager(screen, GRID_WIDTH, GRID_HEIGHT)

    pygame.display.set_caption("Xonix (pygame)")
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(20)

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False

        
        screen.fill((0, 0, 0))


        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
