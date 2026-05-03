import pygame

from common.xonix_events import XonixEvent

class OverlayGamePaused:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.pause_selected = 0


    def tick(self, clock):
        clock.tick(5)


    def handle_events(self, event):
        if event.key == pygame.K_UP:
            self.pause_selected = (self.pause_selected - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.pause_selected = (self.pause_selected + 1) % 2
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if self.pause_selected == 0:  # Resume
                self.event_bus.publish(XonixEvent.RESUME_GAME)
            elif self.pause_selected == 1:  # Main Menu
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

        title_surf = title_font.render("PAUSED", True, (0, 180, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(width // 2, height // 2 - 90)))

        options = ["Resume", "Main Menu"]
        for i, option in enumerate(options):
            color = (255, 220, 0) if i == self.pause_selected else (180, 180, 180)
            surf = menu_font.render(option, True, color)
            rect = surf.get_rect(center=(width // 2, height // 2 - 10 + i * 56))
            if i == self.pause_selected:
                pygame.draw.rect(screen, (30, 30, 80), rect.inflate(24, 10))
                pygame.draw.rect(screen, (0, 120, 200), rect.inflate(24, 10), 2)
            screen.blit(surf, rect)

        hint_surf = hint_font.render(
            "UP / DOWN to navigate      ENTER to select", True, (80, 80, 100)
        )
        screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 36)))
