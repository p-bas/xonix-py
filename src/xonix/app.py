import logging
import pygame

from config import WIDTH, HEIGHT
from resources import ResourceLoader, AudioManager

from common.xonix_events import XonixEvent, XonixEventBus
from modes.landing.landing_mode import LandingMode
from modes.game.game_mode import GameMode


logging.basicConfig(level=logging.INFO)

class App:
    def __init__(self):
        pygame.init()

        loader = ResourceLoader()
        sound_player = AudioManager(loader)

        event_bus = XonixEventBus()

        self.game_mode = GameMode(sound_player, event_bus)
        self.landing = LandingMode(event_bus)

        event_bus.subscribe(XonixEvent.START_GAME, self.start_game)
        event_bus.subscribe(XonixEvent.SHOW_MENU, self.show_menu)
        event_bus.subscribe(XonixEvent.TOGGLE_FULLSCREEN, self.toggle_fullscreen)
        event_bus.subscribe(XonixEvent.EXIT_GAME, self.exit)

        self.exit_fullscreen()
        self.mode = self.landing
        self.running = True


    def run(self):
        pygame.display.set_caption("Xonix")
        clock = pygame.time.Clock()

        while self.running:
            mode = self.mode

            mode.tick(clock)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                else:
                    mode.handle_events(event)

            mode.update()
            mode.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


    def exit(self):
        self.running = False


    def start_game(self):
        self.game_mode.reset(level=1)
        self.mode = self.game_mode


    def show_menu(self):
        self.mode = self.landing


    def toggle_fullscreen(self):
        if self.screen.get_flags() & pygame.FULLSCREEN:
            self.exit_fullscreen()
        else:
            self.enter_fullscreen()


    def enter_fullscreen(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def exit_fullscreen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
