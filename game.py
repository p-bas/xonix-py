import pygame
from config import STATE_PLAYING, STATE_DEAD, STATE_WIN, GRID_WIDTH, GRID_HEIGHT, WIDTH, HEIGHT, CELL_SIZE, COLORS, LEVELS, TRAIL
from enemy import Enemy
from player import Player
from utils import create_field, flood_fill, calculate_coverage, draw_overlay, draw_hud
from sound_manager import SoundManager

class Game:
    def __init__(self):
        self.state = STATE_PLAYING
        self.level = 0
        self.sound_manager = SoundManager()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Xonix (pygame)")
        self.clock = pygame.time.Clock()
        self.field, self.player, self.enemies = self.start_level(self.level)

    def start_level(self, level):
        field = create_field()
        player = Player()
        enemies = [Enemy(GRID_WIDTH, GRID_HEIGHT) for _ in range(LEVELS[level]["enemies"])]
        return field, player, enemies

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state == STATE_WIN and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.level += 1
                    if self.level >= len(LEVELS):
                        self.state = STATE_WIN  # final win
                    else:
                        self.field, self.player, self.enemies = self.start_level(self.level)
                        self.state = STATE_PLAYING
                elif event.key == pygame.K_ESCAPE:
                    return False

            if self.state == STATE_DEAD and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.level = 0
                    self.field, self.player, self.enemies = self.start_level(self.level)
                    self.state = STATE_PLAYING
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        if self.state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            self.player.dx = self.player.dy = 0
            if keys[pygame.K_LEFT]:
                self.player.dx = -1
            elif keys[pygame.K_RIGHT]:
                self.player.dx = 1
            elif keys[pygame.K_UP]:
                self.player.dy = -1
            elif keys[pygame.K_DOWN]:
                self.player.dy = 1

            result = self.player.update(self.field, self.sound_manager.play_rub())

            if result == "closed":
                flood_fill(self.field, self.enemies)
                coverage = calculate_coverage(self.field)
                if coverage >= LEVELS[self.level]["win"]:
                    self.state = STATE_WIN
                    self.sound_manager.play_win()

            for enemy in self.enemies:
                enemy.move(self.field, self.sound_manager.play_tick())

                if enemy.x == self.player.x and enemy.y == self.player.y:
                    self.state = STATE_DEAD
                    self.sound_manager.play_fail()
                    break

                if self.player.drawing and self.field[enemy.y][enemy.x] == TRAIL:
                    self.state = STATE_DEAD
                    self.sound_manager.play_fail()
                    break

    def draw(self):
        self.screen.fill((0, 0, 0))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = COLORS[self.field[y][x]]
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

        pygame.draw.rect(
            self.screen,
            COLORS["player"],
            (self.player.x * CELL_SIZE, self.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

        for enemy in self.enemies:
            pygame.draw.circle(
                self.screen,
                COLORS["enemy"],
                (
                    enemy.x * CELL_SIZE + CELL_SIZE // 2,
                    enemy.y * CELL_SIZE + CELL_SIZE // 2,
                ),
                CELL_SIZE // 2,
            )

        draw_hud(self.screen, self.field, self.level)

        if self.state == STATE_DEAD:
            draw_overlay(self.screen, "YOU ARE DEAD")

        if self.state == STATE_WIN:
            if self.level < len(LEVELS):
                draw_overlay(self.screen, f"LEVEL {self.level + 1} COMPLETE")
            else:
                draw_overlay(self.screen, "YOU COMPLETED ALL LEVELS!")

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(LEVELS[self.level]["fps"])
            running = self.handle_events()
            self.update()
            self.draw()

        pygame.quit()