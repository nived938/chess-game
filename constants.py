import os

# ==========================
# WINDOW SETTINGS
# ==========================

WIDTH = 1100
HEIGHT = 710
FPS = 60

# ==========================
# BOARD SETTINGS
# ==========================

BOARD_SIZE = 8
TILE_SIZE = 80

# Compatibility aliases
SQSIZE = TILE_SIZE
SQUARE_SIZE = TILE_SIZE

BOARD_WIDTH = TILE_SIZE * BOARD_SIZE
BOARD_HEIGHT = TILE_SIZE * BOARD_SIZE

BOARD_X = 40
BOARD_Y = 50

# ==========================
# SIDEBAR
# ==========================

SIDEBAR_X = BOARD_X + BOARD_WIDTH + 20
SIDEBAR_WIDTH = WIDTH - SIDEBAR_X - 20

# ==========================
# COLORS
# ==========================

LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)

BACKGROUND = (32, 33, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SELECTED_COLOR = (255, 215, 0)

LEGAL_MOVE_COLOR = (40, 190, 40)

CAPTURE_COLOR = (220, 40, 40)

LAST_MOVE_COLOR = (90, 180, 255)

CHECK_COLOR = (255, 70, 70)

TEXT_COLOR = (235, 235, 235)

# ==========================
# ANIMATION
# ==========================

MOVE_ANIMATION_SPEED = 15

PIECE_SCALE = 0.88

# ==========================
# PIECE IMAGE SIZE
# ==========================

PIECE_SIZE = int(TILE_SIZE * PIECE_SCALE)

# ==========================
# ASSET PATH
# ==========================

ASSET_DIR = "assets"

# ==========================
# PIECE IMAGE FILES
# ==========================

PIECE_IMAGES = {

    "P": "white_pawn.png",
    "R": "white_rook.png",
    "N": "white_knight.png",
    "B": "white_bishop.png",
    "Q": "white_queen.png",
    "K": "white_king.png",

    "p": "black_pawn.png",
    "r": "black_rook.png",
    "n": "black_knight.png",
    "b": "black_bishop.png",
    "q": "black_queen.png",
    "k": "black_king.png",
}

# ==========================
# START POSITION (FEN)
# ==========================

START_FEN = "startpos"

# ==========================
# BOARD LABELS
# ==========================

FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]

RANKS = ["8", "7", "6", "5", "4", "3", "2", "1"]

# ==========================
# PROMOTION PIECES
# ==========================

PROMOTION_OPTIONS = [
    "q",
    "r",
    "b",
    "n"
]

# ==========================
# GAME MODES
# ==========================

PLAYER_VS_PLAYER = 0
PLAYER_VS_AI = 1

# ==========================
# FONTS
# ==========================

FONT_NAME = "arial"

FONT_SMALL = 18
FONT_MEDIUM = 24
FONT_LARGE = 32