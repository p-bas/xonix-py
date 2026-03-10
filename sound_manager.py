import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.tick_sound = pygame.mixer.Sound("sounds/ball.wav")
        self.tick_sound.set_volume(0.25)

        self.win_sound = pygame.mixer.Sound("sounds/win.wav")
        self.win_sound.set_volume(0.7)

        self.fail_sound = pygame.mixer.Sound("sounds/fail.wav")
        self.fail_sound.set_volume(0.5)

        self.rub_sound = pygame.mixer.Sound("sounds/scratch.wav")
        self.rub_sound.set_volume(0.3)

    def play_tick(self):
        self.tick_sound.play()

    def play_win(self):
        self.win_sound.play()

    def play_fail(self):
        self.fail_sound.play()

    def play_rub(self):
        self.rub_sound.play()