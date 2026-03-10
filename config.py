# ---------------- CONFIG ----------------
STATE_PLAYING = 0
STATE_DEAD = 1
STATE_WIN = 2

WIN_PERCENT = 80

CELL_SIZE = 10
GRID_WIDTH = 150
GRID_HEIGHT = 80

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS = 50

EMPTY = 0
FILLED = 1
TRAIL = 2

# Colors
COLORS = {
    EMPTY: (0, 0, 0),
    FILLED: (0, 120, 255),
    TRAIL: (255, 255, 0),
    "player": (0, 255, 0),
    "enemy": (255, 0, 0),
}

LEVELS = [
    {"fps": 40, "enemies": 2, "win": 60},
    {"fps": 50, "enemies": 2, "win": 65},
    {"fps": 60, "enemies": 2, "win": 60},
    {"fps": 50, "enemies": 3, "win": 60},
    {"fps": 50, "enemies": 3, "win": 70},
    {"fps": 60, "enemies": 3, "win": 70},
    {"fps": 60, "enemies": 3, "win": 80},
    {"fps": 60, "enemies": 4, "win": 65},
    {"fps": 60, "enemies": 4, "win": 75},
    {"fps": 70, "enemies": 4, "win": 60},
    {"fps": 70, "enemies": 4, "win": 70},
]

# ----------------------------------------