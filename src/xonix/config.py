CELL_SIZE = 10
GRID_WIDTH = 150
GRID_HEIGHT = 80

WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE


EMPTY = 0
FILLED = 1
TRAIL = 2

# Colors
COLORS = {
  EMPTY: (0, 0, 0),
  FILLED: (2, 250, 176), #(0, 120, 255),
  TRAIL: (252, 146, 219), #(255, 255, 0),
  "player": (136, 0, 214), #(0, 255, 0),
  "enemy": (255, 0, 0),
}

LEVELS_DEV = [
  "fake level: 0",
  {"fps": 30, "enemies": 1, "win": 1},
  {"fps": 31, "enemies": 2, "win": 1},
]

LEVELS_PROD = [
  "fake record - level 0",
  {"fps": 40, "enemies": 2, "win": 65},
  {"fps": 41, "enemies": 2, "win": 70},
  {"fps": 41, "enemies": 2, "win": 70},
  {"fps": 42, "enemies": 3, "win": 65},
  {"fps": 42, "enemies": 3, "win": 70},
  {"fps": 43, "enemies": 3, "win": 75},
  {"fps": 43, "enemies": 4, "win": 70},
  {"fps": 44, "enemies": 4, "win": 75},
  {"fps": 44, "enemies": 4, "win": 80},
  {"fps": 46, "enemies": 5, "win": 75},
  {"fps": 48, "enemies": 5, "win": 80},
  {"fps": 48, "enemies": 6, "win": 75},
  {"fps": 48, "enemies": 6, "win": 80},
  {"fps": 48, "enemies": 7, "win": 80},
  {"fps": 49, "enemies": 7, "win": 83},
  {"fps": 49, "enemies": 8, "win": 83},
  {"fps": 50, "enemies": 8, "win": 83},
  {"fps": 50, "enemies": 9, "win": 83},
  {"fps": 50, "enemies": 10, "win": 83},
]

LEVELS = LEVELS_PROD
