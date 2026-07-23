import pygame

from constants import *


class Button:

    def __init__(
        self,
        text,
        x,
        y,
        width,
        height
    ):

        self.text = text

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.hover = False

        self.scale = 1.0

    def update(self):

        mouse = pygame.mouse.get_pos()

        self.hover = self.rect.collidepoint(mouse)

        target = 1.05 if self.hover else 1.0

        self.scale += (
            target - self.scale
        ) * 0.20

    def draw(
        self,
        surface,
        font
    ):

        w = self.rect.width * self.scale
        h = self.rect.height * self.scale

        x = self.rect.centerx - w / 2
        y = self.rect.centery - h / 2

        button = pygame.Rect(
            x,
            y,
            w,
            h
        )

        color = (
            70,
            70,
            70
        )

        if self.hover:

            color = (
                100,
                100,
                100
            )

        pygame.draw.rect(
            surface,
            color,
            button,
            border_radius=18
        )

        pygame.draw.rect(
            surface,
            (220, 220, 220),
            button,
            2,
            border_radius=18
        )

        text = font.render(
            self.text,
            True,
            WHITE
        )

        surface.blit(
            text,
            (
                button.centerx - text.get_width() // 2,
                button.centery - text.get_height() // 2
            )
        )

    def clicked(
        self,
        pos
    ):

        return self.rect.collidepoint(pos)


class Menu:

    MAIN_MENU = 0

    SIDE_MENU = 1

    def __init__(self):

        self.state = self.MAIN_MENU

        self.selected_mode = None

        self.finished = False

        self.play_white = True

        self.title_font = pygame.font.SysFont(
            FONT_NAME,
            60,
            bold=True
        )

        self.button_font = pygame.font.SysFont(
            FONT_NAME,
            30,
            bold=True
        )

        button_width = 300

        button_height = 70

        center_x = WIDTH // 2 - button_width // 2

        self.multiplayer_button = Button(
            "Multiplayer",
            center_x,
            280,
            button_width,
            button_height
        )

        self.solo_button = Button(
            "Solo Player",
            center_x,
            380,
            button_width,
            button_height
        )

        self.white_button = Button(
            "White",
            center_x,
            300,
            button_width,
            button_height
        )

        self.black_button = Button(
            "Black",
            center_x,
            400,
            button_width,
            button_height
        )

    def update(self):

        if self.state == self.MAIN_MENU:

            self.multiplayer_button.update()

            self.solo_button.update()

        else:

            self.white_button.update()

            self.black_button.update()

    def draw(
        self,
        surface
    ):

        surface.fill(BACKGROUND)

        if self.state == self.MAIN_MENU:

            title = self.title_font.render(
                "CHESS",
                True,
                WHITE
            )

            surface.blit(
                title,
                (
                    WIDTH // 2 - title.get_width() // 2,
                    120
                )
            )

            self.multiplayer_button.draw(
                surface,
                self.button_font
            )

            self.solo_button.draw(
                surface,
                self.button_font
            )

        else:

            title = self.title_font.render(
                "Choose Side",
                True,
                WHITE
            )

            surface.blit(
                title,
                (
                    WIDTH // 2 - title.get_width() // 2,
                    120
                )
            )

            self.white_button.draw(
                surface,
                self.button_font
            )

            self.black_button.draw(
                surface,
                self.button_font
            )

    def mouse_down(
        self,
        pos
    ):

        if self.state == self.MAIN_MENU:

            if self.multiplayer_button.clicked(pos):

                self.selected_mode = "multiplayer"

                self.state = self.SIDE_MENU

                return

            if self.solo_button.clicked(pos):

                self.selected_mode = "solo"

                self.state = self.SIDE_MENU

                return

        else:

            if self.white_button.clicked(pos):

                self.play_white = True

                self.finished = True

                return

            if self.black_button.clicked(pos):

                self.play_white = False

                self.finished = True

                return

    def is_finished(self):

        return self.finished

    def is_solo(self):

        return self.selected_mode == "solo"

    def is_multiplayer(self):

        return self.selected_mode == "multiplayer"