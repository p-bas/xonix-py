import pygame

from config import LEVELS

class GameStatHud:
    def __init__(self):
        self.level = 0
        self.coverage = 0.0
        self.win_rate = 0
        self.lives_left = 0

    def update(self, field, level, lives_left):
        self.level = level
        self.coverage = field.calculate_coverage()
        self.win_rate = LEVELS[level]["win"] if level < len(LEVELS) else None
        self.lives_left = lives_left

    def draw(self, screen):
        font = pygame.font.SysFont(None, 24)
        lines = [
            f"Level: {self.level}",
            f"Lives: {self.lives_left}",
            f"Coverage: {self.coverage:.1f}%",
            f"Target: {self.win_rate}%",
        ]
        for i, line in enumerate(lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (10, 10 + i * 18))
