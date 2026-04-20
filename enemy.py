import random

from config import GRID_WIDTH, GRID_HEIGHT, FILLED


class Enemy:
    def __init__(self):
        self.x = random.randint(2, GRID_WIDTH - 3)
        self.y = random.randint(2, GRID_HEIGHT - 3)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def move(self, field, tick_sound=None):
        reflected = False
        hit_x = field[self.y][self.x + self.dx] == FILLED
        hit_y = field[self.y + self.dy][self.x] == FILLED

        # Corner collision: reflect both directions
        if hit_x and hit_y:
            self.dx *= -1
            self.dy *= -1
            reflected = True
        else:
            # Reflect only the blocked axis
            if hit_x:
                self.dx *= -1
                reflected = True
            if hit_y:
                self.dy *= -1
                reflected = True

        if reflected and tick_sound:
            tick_sound.play()

        self.x += self.dx
        self.y += self.dy
