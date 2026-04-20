import pygame

from config import STATE_PLAYING
from game_logic import start_level


def handle_events(event, gs, screen, player):
    """Handle keyboard events in the main menu. Returns the (possibly updated) screen surface."""
    if event.type != pygame.KEYDOWN:
        return screen

    if event.key == pygame.K_UP:
        gs.menu_selected = (gs.menu_selected - 1) % 3
    elif event.key == pygame.K_DOWN:
        gs.menu_selected = (gs.menu_selected + 1) % 3
    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
        if gs.menu_selected == 0:  # Start Game
            gs.level = 1
            gs.lives = gs.max_lives
            gs.field, gs.enemies = start_level(player, gs.level)
            gs.state = STATE_PLAYING
        elif gs.menu_selected == 1:  # Toggle Fullscreen
            gs.is_fullscreen = not gs.is_fullscreen
            if gs.is_fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                from config import WIDTH, HEIGHT
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
        elif gs.menu_selected == 2:  # Exit
            gs.running = False
    elif event.key == pygame.K_ESCAPE:
        gs.running = False

    return screen


def draw(screen, gs):
    w, h = screen.get_size()
    screen.fill((0, 0, 20))

    title_font = pygame.font.SysFont(None, min(w // 5, 300))
    menu_font = pygame.font.SysFont(None, min(w // 18, 56))
    hint_font = pygame.font.SysFont(None, min(w // 38, 28))

    title_surf = title_font.render("XONIX", True, (0, 200, 255))
    title_rect = title_surf.get_rect(center=(w // 2, h // 3))
    screen.blit(title_surf, title_rect)

    fullscreen_label = "Fullscreen: ON" if gs.is_fullscreen else "Fullscreen: OFF"
    options = ["Start Game", fullscreen_label, "Exit"]

    for i, option in enumerate(options):
        color = (255, 220, 0) if i == gs.menu_selected else (180, 180, 180)
        surf = menu_font.render(option, True, color)
        rect = surf.get_rect(center=(w // 2, h // 2 + i * 68))
        if i == gs.menu_selected:
            pygame.draw.rect(screen, (30, 30, 80), rect.inflate(24, 12))
            pygame.draw.rect(screen, (0, 120, 200), rect.inflate(24, 12), 2)
        screen.blit(surf, rect)

    hint_surf = hint_font.render(
        "UP / DOWN to navigate      ENTER to select", True, (80, 80, 100)
    )
    hint_rect = hint_surf.get_rect(center=(w // 2, h - 36))
    screen.blit(hint_surf, hint_rect)
