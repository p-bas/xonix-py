import pygame

from config import STATE_PLAYING, STATE_MENU


def handle_events(event, gs):
    """Handle keyboard events in the pause menu."""
    if event.type != pygame.KEYDOWN:
        return

    if event.key == pygame.K_UP:
        gs.pause_selected = (gs.pause_selected - 1) % 2
    elif event.key == pygame.K_DOWN:
        gs.pause_selected = (gs.pause_selected + 1) % 2
    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
        if gs.pause_selected == 0:  # Resume
            gs.state = STATE_PLAYING
        elif gs.pause_selected == 1:  # Main Menu
            gs.state = STATE_MENU
            gs.menu_selected = 0


def draw_overlay(screen, gs):
    """Draw the pause overlay on top of the already-rendered game field."""
    width, height = screen.get_size()

    overlay = pygame.Surface((width, height))
    overlay.set_alpha(190)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont(None, 72)
    menu_font = pygame.font.SysFont(None, 40)
    hint_font = pygame.font.SysFont(None, 28)

    title_surf = title_font.render("PAUSED", True, (0, 180, 255))
    title_rect = title_surf.get_rect(center=(width // 2, height // 2 - 90))
    screen.blit(title_surf, title_rect)

    options = ["Resume", "Main Menu"]
    for i, option in enumerate(options):
        color = (255, 220, 0) if i == gs.pause_selected else (180, 180, 180)
        surf = menu_font.render(option, True, color)
        rect = surf.get_rect(center=(width // 2, height // 2 - 10 + i * 56))
        if i == gs.pause_selected:
            pygame.draw.rect(screen, (30, 30, 80), rect.inflate(24, 10))
            pygame.draw.rect(screen, (0, 120, 200), rect.inflate(24, 10), 2)
        screen.blit(surf, rect)

    hint_surf = hint_font.render("UP / DOWN to navigate      ENTER to select", True, (80, 80, 100))
    hint_rect = hint_surf.get_rect(center=(width // 2, height - 36))
    screen.blit(hint_surf, hint_rect)
