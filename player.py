from config import FILLED, EMPTY, TRAIL, GRID_WIDTH, GRID_HEIGHT

class Player:
    def __init__(self):
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT - 2
        self.dx = 0
        self.dy = 0
        self.drawing = False

    def update(self, field, sound=None):
        if self.dx == 0 and self.dy == 0:
            return None

        nx = self.x + self.dx
        ny = self.y + self.dy

        # Prevent leaving field
        if nx < 0 or nx >= GRID_WIDTH or ny < 0 or ny >= GRID_HEIGHT:
            return None

        next_cell = field[ny][nx]

        # 🚫 Prevent moving back onto own trail (NO DEATH)
        if next_cell == TRAIL:
            return None

        # 🧱 Reached filled area
        if next_cell == FILLED:
            if self.drawing:
                # CLOSE THE CONTOUR:
                # convert last trail cell to filled
                field[self.y][self.x] = FILLED
                self.x = nx
                self.y = ny
                self.drawing = False
                return "closed"
            else:
                self.x = nx
                self.y = ny
                return None

        # 🟨 Move into empty area → draw trail
        if next_cell == EMPTY:
            field[self.y][self.x] = TRAIL
            self.x = nx
            self.y = ny
            self.drawing = True
            # sound.play()
            return None