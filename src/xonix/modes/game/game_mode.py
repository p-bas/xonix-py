import pygame

from config import LEVELS, TRAIL
from resources import Sound
from .overlay_level_passed import OverlayLevelPassed
from .overlay_level_failed import OverlayLevelFailed
from .overlay_game_paused import OverlayGamePaused
from .game_stat_hud import GameStatHud
from .battle_field import BattleField
from .player import Player
from .enemy import Enemy
from common.xonix_events import XonixEvent

STARTING_LIFES_LEFT = 3

class GameMode:
    def __init__(self, sound_player, event_bus):
        self.sound_player = sound_player
        self.tick_sound = sound_player.get(Sound.TICK)
        self.game_stat_hud = GameStatHud()
        self.reset(level=1)

        self.event_bus = event_bus
        self.event_bus.subscribe(XonixEvent.RESUME_GAME, self._on_resume_game)
        self.event_bus.subscribe(XonixEvent.RETRY_LEVEL, self._on_retry_level)
        self.event_bus.subscribe(XonixEvent.NEXT_LEVEL, self._on_next_level)

    def reset(self, level):
        self.level = level
        self.field = BattleField()
        self.player = Player(self.sound_player)
        self.enemies = [Enemy() for _ in range(LEVELS[level]["enemies"])]
        self.lives_left = STARTING_LIFES_LEFT
        self.life_lost_selected = 0
        self.pause_selected = 0
        self.overlay = None

    def tick(self, clock):
        if self.overlay is not None:
            self.overlay.tick(clock)
        else:
            fps = LEVELS[self.level]["fps"]
            clock.tick(fps)

    def update(self):
        if self.overlay is None:
            self._update()
            self.game_stat_hud.update(self.field, self.level, self.lives_left)

    def handle_events(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.overlay is None:
            if event.key == pygame.K_ESCAPE:
                self.overlay = OverlayGamePaused(self.event_bus)

        elif self.overlay is not None:
            self.overlay.handle_events(event)

    def _update(self):
        player = self.player
        keys = pygame.key.get_pressed()
        player.move_clear()
        if keys[pygame.K_LEFT]:
            player.move_left(self.field)
        elif keys[pygame.K_RIGHT]:
            player.move_right(self.field)
        elif keys[pygame.K_UP]:
            player.move_up(self.field)
        elif keys[pygame.K_DOWN]:
            player.move_down(self.field)

        if player.result == "closed":
            self.field.flood_fill(self.enemies)
            coverage = self.field.calculate_coverage()
            if coverage >= LEVELS[self.level]["win"]:
                self.overlay = OverlayLevelPassed(self.event_bus, self.level)
                self.sound_player.play(Sound.WIN)
                return

        for enemy in self.enemies:
            enemy.move(self.field, self.tick_sound)
            if player.drawing:
                colide_with_player = (enemy.x == player.x and enemy.y == player.y)
                colide_with_trail = (self.field[enemy.y][enemy.x] == TRAIL)
                if colide_with_player or colide_with_trail:
                    self.lives_left -= 1
                    self.sound_player.play(Sound.FAIL)
                    self.overlay = OverlayLevelFailed(self.event_bus)
                    break

    def draw(self, screen):
        self.field.draw(screen, self.player, self.enemies)
        self.game_stat_hud.draw(screen)

        if self.overlay is not None:
            self.overlay.draw(screen)

    def _on_resume_game(self):
        self.overlay = None

    def _on_retry_level(self):
        self.overlay = None
        if self.lives_left > 0:
            self.field.consume_life(self.player)
        else:
            self.reset(self.level)

    def _on_next_level(self):
        self.overlay = None
        self.level += 1
        if self.level >= len(LEVELS):
            self.level = 1
        self.reset(self.level)
