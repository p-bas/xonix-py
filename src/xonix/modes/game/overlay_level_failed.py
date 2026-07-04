import pygame
from pathlib import Path

from common.xonix_events import XonixEvent

_IMAGES_DIR = Path(__file__).parent.parent.parent / "assets" / "images"

class OverlayLevelFailed:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.selected_option = 0
        self._fail_image = pygame.image.load(str(_IMAGES_DIR / "fail.png")).convert_alpha()

    def tick(self, clock):
        clock.tick(5)

    def handle_events(self, event):
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % 3
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % 3
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if self.selected_option == 0:
                self.event_bus.publish(XonixEvent.RETRY_LEVEL)
            elif self.selected_option == 1:
                self.event_bus.publish(XonixEvent.SHOW_MENU)
            elif self.selected_option == 2:
                self.event_bus.publish(XonixEvent.EXIT_GAME)
        elif event.key == pygame.K_ESCAPE:
            self.event_bus.publish(XonixEvent.SHOW_MENU)

    def draw(self, screen):
        width, height = screen.get_size()

        overlay = pygame.Surface((width, height))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        menu_font = pygame.font.SysFont(None, 40)
        hint_font = pygame.font.SysFont(None, 28)

        img_size = 144
        fail_img = pygame.transform.smoothscale(self._fail_image, (img_size, img_size))
        screen.blit(fail_img, fail_img.get_rect(center=(width // 2, height // 2 - 140)))

        options = ["Retry", "Main Menu", "Exit Game"]
        for i, option in enumerate(options):
            color = (255, 220, 0) if i == self.selected_option else (180, 180, 180)
            surf = menu_font.render(option, True, color)
            rect = surf.get_rect(center=(width // 2, height // 2 - 10 + i * 56))
            if i == self.selected_option:
                pygame.draw.rect(screen, (80, 30, 30), rect.inflate(24, 10))
                pygame.draw.rect(screen, (200, 0, 0), rect.inflate(24, 10), 2)
            screen.blit(surf, rect)