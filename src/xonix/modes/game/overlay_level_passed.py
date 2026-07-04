import pygame

from common.xonix_events import XonixEvent

class OverlayLevelPassed:
    def __init__(self, event_bus, level):
        self.event_bus = event_bus
        self.level = level
        self.selected_option = 0

    def tick(self, clock):
        clock.tick(5)

    def handle_events(self, event):
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.event_bus.publish(XonixEvent.NEXT_LEVEL)
        elif event.key == pygame.K_ESCAPE:
            self.event_bus.publish(XonixEvent.SHOW_MENU)

    def draw(self, screen):
        width, height = screen.get_size()

        text = f"LEVEL {self.level} COMPLETE"

        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont(None, 64)
        small_font = pygame.font.SysFont(None, 32)

        text_surf = font.render(text, True, (255, 0, 0))
        hint_surf = small_font.render(
            "Press ENTER or SPACE to continue, ESC to Exit", True, (255, 255, 255)
        )

        screen.blit(text_surf, text_surf.get_rect(center=(width // 2, height // 2 - 20)))
        screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height // 2 + 30)))
