import pygame

from common.xonix_events import XonixEvent

class OverlayLevelFailed:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.selected_option = 0

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

        title_font = pygame.font.SysFont(None, 72)
        menu_font = pygame.font.SysFont(None, 40)
        hint_font = pygame.font.SysFont(None, 28)

        title_surf = title_font.render("LEVEL FAILED", True, (255, 50, 50))
        screen.blit(title_surf, title_surf.get_rect(center=(width // 2, height // 2 - 90)))

        options = ["Retry", "Main Menu", "Exit Game"]
        for i, option in enumerate(options):
            color = (255, 220, 0) if i == self.selected_option else (180, 180, 180)
            surf = menu_font.render(option, True, color)
            rect = surf.get_rect(center=(width // 2, height // 2 - 10 + i * 56))
            if i == self.selected_option:
                pygame.draw.rect(screen, (80, 30, 30), rect.inflate(24, 10))
                pygame.draw.rect(screen, (200, 0, 0), rect.inflate(24, 10), 2)
            screen.blit(surf, rect)