import os
import pygame
import chess

from constants import *

# ==========================================
# IMAGE CACHE
# ==========================================

_piece_images = {}


def load_piece_images():
    """
    Load and cache all piece images.
    Call this once when the game starts.
    """

    global _piece_images

    if _piece_images:
        return

    for symbol, filename in PIECE_IMAGES.items():

        path = os.path.join(ASSET_DIR, filename)

        image = pygame.image.load(path).convert_alpha()

        image = pygame.transform.smoothscale(
            image,
            (PIECE_SIZE, PIECE_SIZE)
        )

        _piece_images[symbol] = image


def get_piece_image(symbol):
    """
    Returns a cached image.
    """

    return _piece_images.get(symbol)


# ==========================================
# PIECE CLASS
# ==========================================

class Piece:

    def __init__(self, symbol, row, col):

        self.symbol = symbol

        self.row = row
        self.col = col

        self.image = get_piece_image(symbol)

        # Current drawing position
        self.x = BOARD_X + col * TILE_SIZE
        self.y = BOARD_Y + row * TILE_SIZE

    # --------------------------------------

    @property
    def color(self):

        if self.symbol.isupper():
            return chess.WHITE

        return chess.BLACK

    # --------------------------------------

    @property
    def piece_type(self):

        mapping = {
            "P": chess.PAWN,
            "R": chess.ROOK,
            "N": chess.KNIGHT,
            "B": chess.BISHOP,
            "Q": chess.QUEEN,
            "K": chess.KING,
            "p": chess.PAWN,
            "r": chess.ROOK,
            "n": chess.KNIGHT,
            "b": chess.BISHOP,
            "q": chess.QUEEN,
            "k": chess.KING,
        }

        return mapping[self.symbol]

    # --------------------------------------

    @property
    def rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            PIECE_SIZE,
            PIECE_SIZE
        )

    # --------------------------------------

    def set_square(self, row, col):

        self.row = row
        self.col = col

        self.target_x = BOARD_X + col * TILE_SIZE
        self.target_y = BOARD_Y + row * TILE_SIZE

        self.animating = True

    # --------------------------------------

    def update(self):

    # Board controls the movement animation now.
        pass

    # --------------------------------------

    def draw_shadow(self, surface):

        if self.image is None:
            return

        shadow = self.image.copy()

        shadow.fill(
            (0, 0, 0, 100),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        surface.blit(
            shadow,
            (self.x + 4, self.y + 5)
        )

    # --------------------------------------

    def draw(self, surface):

        if self.image is None:
            return

        surface.blit(
            self.image,
            (
                int(self.x),
                int(self.y)
            )
        )

    # --------------------------------------

    def contains_point(self, pos):

        mx, my = pos

        return self.rect.collidepoint(mx, my)

    # --------------------------------------

    def copy(self):

        new_piece = Piece(
            self.symbol,
            self.row,
            self.col
        )

        new_piece.x = self.x
        new_piece.y = self.y

        new_piece.target_x = self.target_x
        new_piece.target_y = self.target_y

        new_piece.dragging = False
        new_piece.animating = False

        return new_piece

    # --------------------------------------

    def __repr__(self):

        return (
            f"Piece("
            f"{self.symbol}, "
            f"row={self.row}, "
            f"col={self.col}"
            f")"
        )