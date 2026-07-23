import pygame


class SoundManager:

    def __init__(self):

        pygame.mixer.init()

        self.move = pygame.mixer.Sound(
            "sounds/move.wav"
        )

        self.capture = pygame.mixer.Sound(
            "sounds/capture.wav"
        )

        self.castle = pygame.mixer.Sound(
            "sounds/castle.wav"
        )

        self.check = pygame.mixer.Sound(
            "sounds/check.wav"
        )

        self.promote = pygame.mixer.Sound(
            "sounds/promote.wav"
        )

        self.game_over = pygame.mixer.Sound(
            "sounds/game_over.wav"
        )

    def play_move(self):
        self.move.play()

    def play_capture(self):
        self.capture.play()

    def play_castle(self):
        self.castle.play()

    def play_check(self):
        self.check.play()

    def play_promote(self):
        self.promote.play()

    def play_game_over(self):
        self.game_over.play()