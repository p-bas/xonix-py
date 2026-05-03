import pygame

from common.xonix_events import XonixEvent


class LandingMode:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self._item_rects: list[pygame.Rect] = []
        self._activeIndex = 0


    def __activate(self):
        if self._activeIndex == 0:  # Start Game
            self.event_bus.publish(XonixEvent.START_GAME)
        elif self._activeIndex == 1:  # Toggle Fullscreen
            self.event_bus.publish(XonixEvent.TOGGLE_FULLSCREEN)
        elif self._activeIndex == 2:  # Exit
            self.event_bus.publish(XonixEvent.EXIT_GAME)


    def handle_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self._item_rects):
                if rect.collidepoint(event.pos):
                    self._activeIndex = i

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._item_rects):
                if rect.collidepoint(event.pos):
                    self._activeIndex = i
                    self.__activate()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self._activeIndex = (self._activeIndex - 1) % 3
            elif event.key == pygame.K_DOWN:
                self._activeIndex = (self._activeIndex + 1) % 3
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.__activate()


    def tick(self, clock):
        clock.tick(5)


    def update(self):
        pass


    def draw(self, screen):
        w, h = screen.get_size()
        screen.fill((0, 0, 20))

        title_font = pygame.font.SysFont(None, min(w // 5, 300))
        menu_font = pygame.font.SysFont(None, min(w // 18, 56))
        hint_font = pygame.font.SysFont(None, min(w // 38, 28))

        title_surf = title_font.render("XONIX", True, (0, 200, 255))
        title_rect = title_surf.get_rect(center=(w // 2, h // 3))
        screen.blit(title_surf, title_rect)

        is_fullscreen = bool(screen.get_flags() & pygame.FULLSCREEN)
        fullscreen_label = "Fullscreen: ON" if is_fullscreen else "Fullscreen: OFF"
        options = ["Start Game", fullscreen_label, "Exit"]

        self._item_rects.clear()
        for i, option in enumerate(options):
            color = (255, 220, 0) if i == self._activeIndex else (180, 180, 180)
            surf = menu_font.render(option, True, color)
            rect = surf.get_rect(center=(w // 2, h // 2 + i * 68))
            hit_rect = rect.inflate(24, 12)
            self._item_rects.append(hit_rect)
            if i == self._activeIndex:
                pygame.draw.rect(screen, (30, 30, 80), hit_rect)
                pygame.draw.rect(screen, (0, 120, 200), hit_rect, 2)
            screen.blit(surf, rect)

        hint_surf = hint_font.render(
            "UP / DOWN to navigate      ENTER to select", True, (80, 80, 100)
        )
        hint_rect = hint_surf.get_rect(center=(w // 2, h - 36))
        screen.blit(hint_surf, hint_rect)
