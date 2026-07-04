from pathlib import Path
import pygame

from common.xonix_events import XonixEvent

_TROPHY_IMAGE = Path(__file__).parent.parent.parent / "assets" / "images" / "trophy.png"


class OverlayYouWon:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.selected_option = 0

    def tick(self, clock):
        clock.tick(5)

    def handle_events(self, event):
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % 2
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if self.selected_option == 0:
                self.event_bus.publish(XonixEvent.START_GAME)
            else:
                self.event_bus.publish(XonixEvent.EXIT_GAME)

    def draw(self, screen):
        width, height = screen.get_size()
        cx = width // 2

        overlay = pygame.Surface((width, height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        trophy_img = pygame.image.load(str(_TROPHY_IMAGE)).convert_alpha()
        trophy_img = pygame.transform.smoothscale(trophy_img, (320, 320))
        screen.blit(trophy_img, trophy_img.get_rect(center=(cx, height // 2 - 220)))

        congrats_font = pygame.font.SysFont(None, 60)
        congrats_surf = congrats_font.render("Congratulations", True, (255, 200, 0))
        screen.blit(congrats_surf, congrats_surf.get_rect(center=(cx, height // 2 - 55)))

        won_font = pygame.font.SysFont(None, 96)
        won_surf = won_font.render("You won!", True, (255, 255, 255))
        screen.blit(won_surf, won_surf.get_rect(center=(cx, height // 2 + 30)))

        menu_font = pygame.font.SysFont(None, 42)
        options = ["Start New Game", "Exit"]
        for i, option in enumerate(options):
            color = (255, 220, 0) if i == self.selected_option else (180, 180, 180)
            surf = menu_font.render(option, True, color)
            rect = surf.get_rect(center=(cx, height // 2 + 130 + i * 56))
            if i == self.selected_option:
                pygame.draw.rect(screen, (30, 30, 80), rect.inflate(24, 10))
                pygame.draw.rect(screen, (0, 120, 200), rect.inflate(24, 10), 2)
            screen.blit(surf, rect)

        hint_font = pygame.font.SysFont(None, 28)
        hint_surf = hint_font.render(
            "UP / DOWN to navigate      ENTER to select", True, (80, 80, 100)
        )
        screen.blit(hint_surf, hint_surf.get_rect(center=(cx, height - 36)))


