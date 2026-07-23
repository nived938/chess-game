import pygame

from constants import *


class Settings:

    def __init__(self):

        self.visible = False

        self.font = pygame.font.SysFont(
            FONT_NAME,
            26,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            FONT_NAME,
            22
        )

        self.window = pygame.Rect(
            WIDTH // 2 - 220,
            HEIGHT // 2 - 220,
            440,
            440
        )

        self.close_button = pygame.Rect(
            self.window.right - 45,
            self.window.y + 10,
            35,
            35
        )

        self.sound = True
        self.animations = True

        self.board_theme = 0

        self.themes = [
            "Classic",
            "Wood",
            "Blue",
            "Green"
        ]

        self.sound_button = pygame.Rect(
            self.window.x + 30,
            self.window.y + 80,
            180,
            45
        )

        self.animation_button = pygame.Rect(
            self.window.x + 30,
            self.window.y + 145,
            180,
            45
        )

        self.theme_button = pygame.Rect(
            self.window.x + 30,
            self.window.y + 210,
            180,
            45
        )

    def open(self):

        self.visible = True

    def close(self):

        self.visible = False

    def draw(self, surface):

        if not self.visible:
            return

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 170))

        surface.blit(
            overlay,
            (0, 0)
        )

        pygame.draw.rect(
            surface,
            (35, 35, 35),
            self.window,
            border_radius=20
        )

        pygame.draw.rect(
            surface,
            (220, 220, 220),
            self.window,
            2,
            border_radius=20
        )

        title = self.font.render(
            "Settings",
            True,
            WHITE
        )

        surface.blit(
            title,
            (
                self.window.centerx - title.get_width() // 2,
                self.window.y + 20
            )
        )

        self.draw_button(
            surface,
            self.sound_button,
            f"Sound : {'ON' if self.sound else 'OFF'}"
        )

        self.draw_button(
            surface,
            self.animation_button,
            f"Animations : {'ON' if self.animations else 'OFF'}"
        )

        self.draw_button(
            surface,
            self.theme_button,
            f"Board : {self.themes[self.board_theme]}"
        )

        pygame.draw.rect(
            surface,
            (180, 60, 60),
            self.close_button,
            border_radius=8
        )

        x = self.small_font.render(
            "X",
            True,
            WHITE
        )

        surface.blit(
            x,
            (
                self.close_button.centerx - x.get_width() // 2,
                self.close_button.centery - x.get_height() // 2
            )
        )

    def draw_button(
        self,
        surface,
        rect,
        text
    ):

        pygame.draw.rect(
            surface,
            (60, 60, 60),
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            surface,
            (200, 200, 200),
            rect,
            2,
            border_radius=10
        )

        label = self.small_font.render(
            text,
            True,
            WHITE
        )

        surface.blit(
            label,
            (
                rect.centerx - label.get_width() // 2,
                rect.centery - label.get_height() // 2
            )
        )

    def mouse_down(self, pos):

        if not self.visible:
            return

        if self.close_button.collidepoint(pos):

            self.close()

            return

        if self.sound_button.collidepoint(pos):

            self.sound = not self.sound

            return

        if self.animation_button.collidepoint(pos):

            self.animations = not self.animations

            return

        if self.theme_button.collidepoint(pos):

            self.board_theme += 1

            self.board_theme %= len(self.themes)