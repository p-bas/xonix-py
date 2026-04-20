import pygame

from config import STATE_PLAYING, STATE_MENU
from game_logic import consume_life, start_level


def handle_events(event, gs, player):
    """Handle keyboard events in the life-lost / game-over screen."""
    if event.type != pygame.KEYDOWN:
        return

    if event.key == pygame.K_UP:
        gs.life_lost_selected = (gs.life_lost_selected - 1) % 3
    elif event.key == pygame.K_DOWN:
        gs.life_lost_selected = (gs.life_lost_selected + 1) % 3
    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
        if gs.life_lost_selected == 0:
            if gs.lives > 0:
                consume_life(gs.field, player)
            else:
                gs.lives = gs.max_lives
                gs.field, gs.enemies = start_level(player, gs.level)
            gs.state = STATE_PLAYING
        elif gs.life_lost_selected == 1:
            gs.level = 1
            gs.lives = gs.max_lives
            gs.field, gs.enemies = start_level(player, gs.level)
            gs.state = STATE_PLAYING
        elif gs.life_lost_selected == 2:
            gs.state = STATE_MENU
            gs.menu_selected = 0
    elif event.key == pygame.K_ESCAPE:
        gs.state = STATE_MENU
        gs.menu_selected = 0


def draw_overlay(screen, gs):
    """Draw the life-lost / game-over overlay on top of the already-rendered game field."""
    width, height = screen.get_size()

    overlay = pygame.Surface((width, height))
    overlay.set_alpha(190)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont(None, 72)
    menu_font = pygame.font.SysFont(None, 40)
    hint_font = pygame.font.SysFont(None, 28)

    if gs.lives <= 0:
        title_text = "GAME OVER"
        title_color = (220, 0, 0)
        options = [
            f"Restart Level {gs.level}",
            "Restart from Level 1",
            "Exit to Menu",
        ]
    else:
        lives_word = "life" if gs.lives == 1 else "lives"
        title_text = "YOU DIED!"
        title_color = (255, 120, 0)
        options = [
            f"Continue Level {gs.level}  ({gs.lives} {lives_word} left)",
            "Restart from Level 1",
            "Exit to Menu",
        ]

    title_surf = title_font.render(title_text, True, title_color)
    title_rect = title_surf.get_rect(center=(width // 2, height // 2 - 110))
    screen.blit(title_surf, title_rect)

    for i, option in enumerate(options):
        color = (255, 220, 0) if i == gs.life_lost_selected else (180, 180, 180)
        surf = menu_font.render(option, True, color)
        rect = surf.get_rect(center=(width // 2, height // 2 - 20 + i * 56))
        if i == gs.life_lost_selected:
            pygame.draw.rect(screen, (30, 30, 80), rect.inflate(24, 10))
            pygame.draw.rect(screen, (0, 120, 200), rect.inflate(24, 10), 2)
        screen.blit(surf, rect)

    hint_surf = hint_font.render("UP / DOWN to navigate      ENTER to select", True, (80, 80, 100))
    hint_rect = hint_surf.get_rect(center=(width // 2, height - 36))
    screen.blit(hint_surf, hint_rect)
