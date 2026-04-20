import logging
import pygame

from config import LEVELS, STATE_PLAYING, STATE_WIN, STATE_MENU, STATE_LIFE_LOST, STATE_PAUSED
from resources import ResourceLoader, Sound, AudioManager
from player import Player
from game_state import GameState
from game_logic import start_level, draw_field, draw_hud
import menu_mode
import playing_mode
import pause_mode
import life_lost_mode

logging.basicConfig(level=logging.INFO)


def main():
    pygame.init()

    loader = ResourceLoader()
    sound_player = AudioManager(loader)
    player = Player(sound_player)
    tick_sound = sound_player.get(Sound.TICK)

    from config import WIDTH, HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Xonix")
    clock = pygame.time.Clock()

    gs = GameState()
    gs.field, gs.enemies = start_level(player, gs.level)

    while gs.running:
        fps = LEVELS[gs.level]["fps"] if gs.state == STATE_PLAYING else 30
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gs.running = False
            elif gs.state == STATE_MENU:
                screen = menu_mode.handle_events(event, gs, screen, player)
            elif gs.state == STATE_PLAYING:
                playing_mode.handle_events(event, gs)
            elif gs.state == STATE_PAUSED:
                pause_mode.handle_events(event, gs)
            elif gs.state == STATE_WIN:
                playing_mode.handle_win_events(event, gs, player)
            elif gs.state == STATE_LIFE_LOST:
                life_lost_mode.handle_events(event, gs, player)

        if gs.state == STATE_MENU:
            menu_mode.draw(screen, gs)
            pygame.display.flip()
            continue

        if gs.state == STATE_PAUSED:
            draw_field(screen, gs.field, player, gs.enemies)
            draw_hud(screen, gs.field, gs.level, gs.lives)
            pause_mode.draw_overlay(screen, gs)
            pygame.display.flip()
            continue

        if gs.state == STATE_PLAYING:
            playing_mode.update(gs, player, sound_player, tick_sound)

        draw_field(screen, gs.field, player, gs.enemies)
        draw_hud(screen, gs.field, gs.level, gs.lives)

        if gs.state == STATE_LIFE_LOST:
            life_lost_mode.draw_overlay(screen, gs)

        if gs.state == STATE_WIN:
            playing_mode.draw_win_overlay(screen, gs)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
