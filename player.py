from config import GRID_WIDTH, GRID_HEIGHT, FILLED, TRAIL, EMPTY
from resources import AudioManager


class Player:
    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager
        self.reset()

    def reset(self):
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT - 1
        self.drawing = False
        self.move_clear()

    def move_clear(self):
        self.dx = 0
        self.dy = 0
        self.result = None

    def move_up(self, field):
        self.dy = -1
        self.update(field)
    
    def move_down(self, field):
        self.dy = 1
        self.update(field)

    def move_left(self, field):
        self.dx = -1
        self.update(field)

    def move_right(self, field):
        self.dx = 1
        self.update(field)

    def update(self, field, sound=None):
        if self.dx == 0 and self.dy == 0:
            self.result = None
            return

        nx = self.x + self.dx
        ny = self.y + self.dy

        # Prevent leaving field
        if nx < 0 or nx >= GRID_WIDTH or ny < 0 or ny >= GRID_HEIGHT:
            self.result = None
            return

        next_cell = field[ny][nx]

        # 🚫 Prevent moving back onto own trail (NO DEATH)
        if next_cell == TRAIL:
            self.result = None
            return

        # 🧱 Reached filled area
        if next_cell == FILLED:
            if self.drawing:
                # CLOSE THE CONTOUR:
                # convert last trail cell to filled
                field[self.y][self.x] = FILLED
                self.x = nx
                self.y = ny
                self.drawing = False
                self.result = "closed"
                return
            else:
                self.x = nx
                self.y = ny
                self.result = None
                return

        # 🟨 Move into empty area → draw trail
        if next_cell == EMPTY:
            is_filled = field[self.y][self.x] == FILLED
            field[self.y][self.x] = TRAIL if not is_filled else FILLED
            self.x = nx
            self.y = ny
            self.drawing = True
            # sound.play()
            self.result = None
            return
