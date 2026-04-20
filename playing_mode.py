import pygame

from config import STATE_PAUSED, STATE_WIN, STATE_LIFE_LOST, STATE_MENU, STATE_PLAYING, LEVELS, TRAIL
from resources import Sound
from game_logic import flood_fill, calculate_coverage, start_level


def handle_events(event, gs):
    """Handle keyboard events while playing (ESC to pause)."""
    if event.type != pygame.KEYDOWN:
        return

    if event.key == pygame.K_ESCAPE:
        gs.state = STATE_PAUSED
        gs.pause_selected = 0
        print(f"Game paused. State: {gs.state}")


def handle_win_events(event, gs, player):
    """Handle keyboard events in the win state (R for next level, ESC for menu)."""
    if event.type != pygame.KEYDOWN:
        return

    if event.key == pygame.K_r:
        gs.level += 1
        gs.lives = gs.max_lives
        print(f"Starting level {gs.level}, len: {len(LEVELS)}")
        if gs.level >= len(LEVELS):
            gs.level = 1
        gs.field, gs.enemies = start_level(player, gs.level)
        gs.state = STATE_PLAYING
    elif event.key == pygame.K_ESCAPE:
        gs.state = STATE_MENU
        gs.menu_selected = 0


def update(gs, player, sound_player, tick_sound):
    """Update player movement, flood fill, enemy movement and collision detection."""
    keys = pygame.key.get_pressed()
    player.move_clear()
    if keys[pygame.K_LEFT]:
        player.move_left(gs.field)
    elif keys[pygame.K_RIGHT]:
        player.move_right(gs.field)
    elif keys[pygame.K_UP]:
        player.move_up(gs.field)
    elif keys[pygame.K_DOWN]:
        player.move_down(gs.field)

    if player.result == "closed":
        flood_fill(gs.field, gs.enemies)
        coverage = calculate_coverage(gs.field)
        if coverage >= LEVELS[gs.level]["win"]:
            gs.state = STATE_WIN
            sound_player.play(Sound.WIN)
            return  # skip enemy movement after win

    for enemy in gs.enemies:
        enemy.move(gs.field, tick_sound)

        if enemy.x == player.x and enemy.y == player.y:
            gs.lives -= 1
            sound_player.play(Sound.FAIL)
            gs.state = STATE_LIFE_LOST
            gs.life_lost_selected = 0
            break

        elif player.drawing and gs.field[enemy.y][enemy.x] == TRAIL:
            gs.lives -= 1
            sound_player.play(Sound.FAIL)
            gs.state = STATE_LIFE_LOST
            gs.life_lost_selected = 0
            break


def draw_win_overlay(screen, gs):
    """Draw win overlay on top of the already-rendered game field."""
    width, height = screen.get_size()

    if (gs.level + 1) < len(LEVELS):
        text = f"LEVEL {gs.level} COMPLETE"
    else:
        text = "YOU COMPLETED ALL LEVELS!"

    overlay = pygame.Surface((width, height))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 64)
    small_font = pygame.font.SysFont(None, 32)

    text_surf = font.render(text, True, (255, 0, 0))
    hint_surf = small_font.render("Press R to Restart or ESC to Exit", True, (255, 255, 255))

    screen.blit(text_surf, text_surf.get_rect(center=(width // 2, height // 2 - 20)))
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height // 2 + 30)))
