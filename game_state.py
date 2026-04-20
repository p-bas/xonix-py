from config import STATE_MENU


class GameState:
    def __init__(self, max_lives=3):
        self.max_lives = max_lives
        self.lives = max_lives
        self.state = STATE_MENU
        self.level = 1
        self.menu_selected = 0
        self.life_lost_selected = 0
        self.pause_selected = 0
        self.is_fullscreen = False
        self.running = True
        self.field = []
        self.enemies = []
