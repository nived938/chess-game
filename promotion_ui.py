import pygame
import chess

from constants import *
from piece import get_piece_image


class PromotionUI:

    def __init__(self):

        print("PromotionUI __init__ called")

        self.visible = False
        self.color = chess.WHITE
        self.selected = None

        self.alpha = 0
        self.target_alpha = 180

        self.hover_index = -1
        self.scale = [1.0] * 4

        self.box_size = 90
        self.padding = 18

        self.width = self.box_size * 4 + self.padding * 5
        self.height = self.box_size + self.padding * 2

        self.x = (WIDTH - self.width) // 2
        self.y = (HEIGHT - self.height) // 2

        self.rects = []

    def update(self):

        if not self.visible:
            return

        # Fade animation
        if self.alpha < self.target_alpha:

            self.alpha += 15

            if self.alpha > self.target_alpha:
                self.alpha = self.target_alpha

        # Mouse hover
        mouse = pygame.mouse.get_pos()

        self.hover_index = -1

        for i, rect in enumerate(self.rects):

            if rect.collidepoint(mouse):

                self.hover_index = i

                self.scale[i] += (
                    1.12 - self.scale[i]
                ) * 0.25

            else:

                self.scale[i] += (
                    1.0 - self.scale[i]
                ) * 0.25

    # ==========================================
    # Show / Hide
    # ==========================================

    def show(self, color):

        print("SHOW CALLED")

        self.visible = True
        self.color = color
        self.selected = None
        self.alpha = 0

        self.build_rects()

        print("visible =", self.visible)

    def hide(self):

        self.visible = False

        self.selected = None

    # ==========================================
    # Build button rectangles
    # ==========================================

    def build_rects(self):

        self.rects.clear()

        for i in range(4):

            x = (
                self.x
                + self.padding
                + i * (self.box_size + self.padding)
            )

            y = self.y + self.padding

            self.rects.append(

                pygame.Rect(
                    x,
                    y,
                    self.box_size,
                    self.box_size
                )

            )

    # ==========================================
    # Draw
    # ==========================================

    def draw(self, surface):

        print("Drawing promotion UI")

        if not self.visible:
            return

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, self.alpha))

        surface.blit(
            overlay,
            (0, 0)
        )

        pygame.draw.rect(

            surface,

            (35, 35, 35),

            (
                self.x,
                self.y,
                self.width,
                self.height
            ),

            border_radius=15

        )

        pygame.draw.rect(

            surface,

            (220, 220, 220),

            (
                self.x,
                self.y,
                self.width,
                self.height
            ),

            2,

            border_radius=15

        )

        names = [

            "queen",
            "rook",
            "bishop",
            "knight"

        ]

        piece_color = "white" if self.color == chess.WHITE else "black"

        for rect, name in zip(self.rects, names):

            i = self.rects.index(rect)

            scaled = rect.inflate(

                rect.width * (self.scale[i]-1),

                rect.height * (self.scale[i]-1)

            )

            button_color = (60, 60, 60)

            if i == self.hover_index:
                button_color = (90, 90, 90)

            pygame.draw.rect(

                surface,

                button_color,

                scaled,

                border_radius=12

            )

            pygame.draw.rect(

                surface,

                (220,220,220),

                scaled,

                2,

                border_radius=15

            )

            font = pygame.font.SysFont(
                "arial",
                30,
                bold=True
            )

            title = font.render(
                "Choose Promotion",
                True,
                (240, 240, 240)
            )

            surface.blit(
                title,
                (
                    WIDTH // 2 - title.get_width() // 2,
                    self.y - 55
                )
            )

            symbol_map = {
                ("white", "queen"): "Q",
                ("white", "rook"): "R",
                ("white", "bishop"): "B",
                ("white", "knight"): "N",
                ("black", "queen"): "q",
                ("black", "rook"): "r",
                ("black", "bishop"): "b",
                ("black", "knight"): "n",
            }

            symbol = symbol_map[(piece_color, name)]

            image = get_piece_image(symbol)

            img = pygame.transform.smoothscale(

                image,

                (

                    int(image.get_width()*self.scale[i]),

                    int(image.get_height()*self.scale[i])

                )

            )

            img_rect = img.get_rect(
                center=scaled.center
            )

            surface.blit(
                img,
                img_rect
            )

    # ==========================================
    # Mouse Click
    # ==========================================

    def click(self, pos):

        if not self.visible:
            return None

        pieces = [

            chess.QUEEN,
            chess.ROOK,
            chess.BISHOP,
            chess.KNIGHT

        ]

        for rect, piece in zip(
            self.rects,
            pieces
        ):

            if rect.collidepoint(pos):

                self.hide()

                return piece

        return None