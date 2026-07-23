import pygame
import chess

from save_manager import SaveManager
from constants import *
from piece import Piece
from engine import ChessEngine
from sound import SoundManager
from promotion_ui import PromotionUI

class Board:

    def __init__(self):

        # ==========================================
        # Engine
        # ==========================================

        self.engine = ChessEngine()

        # ==========================================
        # UI Board
        # ==========================================

        self.board = [
            [None for _ in range(8)]
            for _ in range(8)
        ]

        # ==========================================
        # Sounds
        # ==========================================

        self.sound = SoundManager()

        # ==========================================
        # Promotion
        # ==========================================

        self.awaiting_promotion = False

        self.promotion_move = None

        self.promotion_ui = PromotionUI()

        # ==========================================
        # Selection
        # ==========================================

        self.selected_piece = None

        self.selected_square = None

        self.legal_moves = []

        # ==========================================
        # Drag
        # ==========================================

        self.dragging = False

        self.mouse_x = 0

        self.mouse_y = 0

        # ==========================================
        # Animation
        # ==========================================

        self.animating = False

        self.animation_piece = None

        self.animation_from = None

        self.animation_to = None

        self.animation_progress = 0.0

        self.animation_speed = 0.10

        self.pending_move = None

        # ==========================================
        # Board State
        # ==========================================

        self.flipped = False

        self.last_move = None

        self.move_history = []

        # ==========================================
        # Chess Clock
        # ==========================================

        self.initial_time = 10 * 60

        self.white_time = self.initial_time

        self.black_time = self.initial_time

        self.last_tick = pygame.time.get_ticks()

        self.clock_running = True

        # ==========================================
        # UI Buttons
        # ==========================================

        self.button_font = pygame.font.SysFont(
            FONT_NAME,
            20,
            bold=True
        )

        button_x = SIDEBAR_X + 190

        self.restart_button = pygame.Rect(
            button_x,
            20,
            145,
            42
        )

        self.undo_button = pygame.Rect(
            button_x,
            75,
            145,
            42
        )

        self.flip_button = pygame.Rect(
            button_x,
            130,
            145,
            42
        )

        self.white_captured = []

        self.black_captured = []

        # ==========================================
        # Game Mode
        # ==========================================

        self.solo = True

        self.player_is_white = True

        # ==========================================
        # Sync Pieces
        # ==========================================

        self.sync_board()


        SaveManager.load(self)


    def restart(self):

        self.engine.reset()

        self.white_captured.clear()

        self.black_captured.clear()

        self.move_history.clear()

        self.white_time = self.initial_time

        self.black_time = self.initial_time

        self.clock_running = True

        self.last_tick = pygame.time.get_ticks()

        self.awaiting_promotion = False

        self.promotion_move = None

        self.clear_selection()

        self.sync_board()

        SaveManager.save(self)


    def game_over(self):

        return self.engine.board.is_game_over()
    
    def timeout(self):

        return (

            self.white_time <= 0

            or

            self.black_time <= 0

        )


    def result(self):

        return self.engine.board.result()


    def status(self):

        return self.engine.board


    def turn(self):

        return self.engine.turn()


    def white_to_move(self):

        return self.engine.turn() == chess.WHITE


    def black_to_move(self):

        return self.engine.turn() == chess.BLACK
    
    # ==========================================================
    # BUILD UI BOARD
    # ==========================================================

    def sync_board(self):

        self.board = [
            [None for _ in range(8)]
            for _ in range(8)
        ]

        for square in chess.SQUARES:

            piece = self.engine.board.piece_at(square)

            if piece is None:
                continue

            row, col = self.engine.coords_from_square(square)

            # Convert python-chess piece to its symbol
            symbol = piece.symbol()

            self.board[row][col] = Piece(
                symbol,
                row,
                col
            )

        # ==========================================================
    # PIECE HELPERS
    # ==========================================================

    def get_piece(
        self,
        row,
        col
    ):

        if row < 0 or row > 7:
            return None

        if col < 0 or col > 7:
            return None

        return self.board[row][col]
    
    def set_piece(
        self,
        row,
        col,
        piece
    ):

        self.board[row][col] = piece

        if piece:

            piece.row = row
            piece.col = col

    def remove_piece(
        self,
        row,
        col
    ):

        self.board[row][col] = None

        # ==========================================================
    # SELECTION
    # ==========================================================

    def clear_selection(self):

        self.selected_piece = None

        self.selected_square = None

        self.legal_moves.clear()

        # ==========================================================
    # CONTROL
    # ==========================================================

    def can_control(
        self,
        color
    ):

        if not self.solo:
            return True

        return color == (
            chess.WHITE
            if self.player_is_white
            else chess.BLACK
        )
    
        # ==========================================================
    # BOARD FLIP
    # ==========================================================

    def flip(self):

        self.flipped = not self.flipped

    def board_to_screen(self, row, col):

        if self.flipped:
            row = 7 - row
            col = 7 - col

        offset = (TILE_SIZE - PIECE_SIZE) // 2

        x = BOARD_X + col * TILE_SIZE + offset
        y = BOARD_Y + row * TILE_SIZE + offset

        return x, y
    
    def screen_to_board(
        self,
        x,
        y
    ):

        x -= BOARD_X
        y -= BOARD_Y

        if x < 0 or y < 0:
            return None

        col = x // TILE_SIZE
        row = y // TILE_SIZE

        if row > 7 or col > 7:
            return None

        if self.flipped:
            row = 7 - row
            col = 7 - col

        return int(row), int(col)
    
        # ==========================================================
    # KEYBOARD
    # ==========================================================

    def key_down(
        self,
        key
    ):
        
        mods = pygame.key.get_mods()

        if mods & pygame.KMOD_CTRL:

            if key == pygame.K_s:

                SaveManager.save(self)

                print("Game Saved")

                return

            if key == pygame.K_l:

                SaveManager.load(self)

                print("Game Loaded")

                return

        if key == pygame.K_f:

            self.flip()

        elif key == pygame.K_r:

            self.restart()

        elif key == pygame.K_u:

            self.undo()

    # ==========================================================
    # UNDO
    # ==========================================================

    def undo(self):

        if len(self.engine.history()) == 0:

            return

        self.engine.undo()

        self.awaiting_promotion = False

        self.clear_selection()

        self.sync_board()

        SaveManager.save(self)

        self.last_move = self.engine.get_last_move()

        # ==========================================================
    # SELECT PIECE
    # ==========================================================

    def select_square(
        self,
        row,
        col
    ):

        piece = self.get_piece(
            row,
            col
        )

        if piece is None:

            self.clear_selection()

            return

        self.selected_piece = piece

        self.selected_square = (
            row,
            col
        )

        self.legal_moves.clear()

        for move in self.engine.board.legal_moves:

            from_row, from_col = (
                self.engine.coords_from_square(
                    move.from_square
                )
            )

            if (
                from_row == row
                and from_col == col
            ):

                to_row, to_col = (
                    self.engine.coords_from_square(
                        move.to_square
                    )
                )

                self.legal_moves.append(
                    (
                        to_row,
                        to_col
                    )
                )

        # ==========================================================
    # LEGAL MOVE
    # ==========================================================

    def is_legal_square(
        self,
        row,
        col
    ):

        return (
            row,
            col
        ) in self.legal_moves
    
        # ==========================================================
    # CHECK
    # ==========================================================

    def king_in_check(self):

        return self.engine.board.is_check()
    
    def checked_king_square(self):

        if not self.engine.board.is_check():
            return None

        king_square = self.engine.board.king(
            self.engine.turn()
        )

        if king_square is None:
            return None

        return self.engine.coords_from_square(
            king_square
        )
    
        # ==========================================================
    # LAST MOVE
    # ==========================================================

    def update_last_move(self):

        if len(self.engine.board.move_stack) == 0:

            self.last_move = None

            return

        self.last_move = (
            self.engine.board.move_stack[-1]
        )

        # ==========================================================
    # CAPTURED PIECES
    # ==========================================================

    def capture_piece(
        self,
        piece
    ):

        if piece is None:
            return

        if piece.color == chess.WHITE:

            self.white_captured.append(
                piece
            )

        else:

            self.black_captured.append(
                piece
            )

        # ==========================================================
    # ANIMATION STATUS
    # ==========================================================

    def is_animating(self):

        return self.animating
    
        # ==========================================================
    # PROMOTION STATE
    # ==========================================================

    def promotion_active(self):

        return self.awaiting_promotion


    def cancel_promotion(self):

        self.awaiting_promotion = False

        self.promotion_move = None

        self.promotion_ui.hide()

        # ==========================================================
    # START MOVE ANIMATION
    # ==========================================================

    def start_move_animation(
        self,
        from_row,
        from_col,
        to_row,
        to_col,
        promotion=None
    ):

        if self.animating:
            return False

        piece = self.get_piece(
            from_row,
            from_col
        )

        if piece is None:
            return False

        self.animation_piece = piece

        self.animation_from = self.board_to_screen(
            from_row,
            from_col
        )

        self.animation_to = self.board_to_screen(
            to_row,
            to_col
        )

        piece.x, piece.y = self.animation_from

        self.animation_progress = 0.0

        self.pending_move = (
            from_row,
            from_col,
            to_row,
            to_col,
            promotion
        )

        self.animating = True

        return True
    
        # ==========================================================
    # FINISH ANIMATION
    # ==========================================================

    def finish_animation(self):

        if self.pending_move is None:
            return

        (
            from_row,
            from_col,
            to_row,
            to_col,
            promotion
        ) = self.pending_move

        self.animating = False

        self.animation_piece = None

        self.animation_from = None

        self.animation_to = None

        self.animation_progress = 0.0

        self.pending_move = None

        self.make_move(
            from_row,
            from_col,
            to_row,
            to_col,
            promotion
        )

        # ==========================================================
    # UPDATE ANIMATION
    # ==========================================================

    def update_animation(self):

        if not self.animating:
            return

        self.animation_progress += self.animation_speed

        if self.animation_progress >= 1.0:

            self.animation_progress = 1.0

            self.finish_animation()

            return

        start_x, start_y = self.animation_from

        end_x, end_y = self.animation_to

        t = self.animation_progress

        self.animation_piece.x = (
            start_x +
            (end_x - start_x) * t
        )

        self.animation_piece.y = (
            start_y +
            (end_y - start_y) * t
        )

        # ==========================================================
    # CANCEL ANIMATION
    # ==========================================================

    def cancel_animation(self):

        self.animating = False

        self.animation_piece = None

        self.animation_from = None

        self.animation_to = None

        self.pending_move = None

        self.animation_progress = 0.0

        # ==========================================================
    # HELPERS
    # ==========================================================

    def moving_piece(self):

        return self.animation_piece


    def has_pending_move(self):

        return self.pending_move is not None
    
        # ==========================================================
    # UPDATE
    # ==========================================================

    def update(self):

        if self.timeout():

            self.clock_running = False

        self.promotion_ui.update()

        # ==========================================
        # Chess Clock
        # ==========================================

        if self.clock_running and not self.game_over():

            now = pygame.time.get_ticks()

            dt = (now - self.last_tick) / 1000

            self.last_tick = now

            if self.engine.turn() == chess.WHITE:

                self.white_time -= dt

            else:

                self.black_time -= dt

            self.white_time = max(0, self.white_time)

            self.black_time = max(0, self.black_time)

        self.update_animation()

        for row in self.board:

            for piece in row:

                if piece:

                    piece.update()

        # ==========================================================
    # MAKE MOVE
    # ==========================================================

    def make_move(
        self,
        from_row,
        from_col,
        to_row,
        to_col,
        promotion=None
    ):

        # -----------------------------
        # Legal move?
        # -----------------------------

        if not self.engine.is_legal(
            from_row,
            from_col,
            to_row,
            to_col
        ):
            return False

        moving_piece = self.get_piece(
            from_row,
            from_col
        )

        if moving_piece is None:
            return False

        captured_piece = self.get_piece(
            to_row,
            to_col
        )

        # -----------------------------
        # Promotion
        # -----------------------------

        if (
            promotion is None
            and
            self.engine.is_promotion_square(
                from_row,
                from_col,
                to_row,
                to_col
            )
        ):

            # Human player
            if self.can_control(
                moving_piece.color
            ):

                self.awaiting_promotion = True

                self.promotion_move = (
                    from_row,
                    from_col,
                    to_row,
                    to_col
                )

                self.promotion_ui.show(
                    moving_piece.color
                )

                return True

            # AI
            else:

                promotion = chess.QUEEN

        # -----------------------------
        # Engine Move
        # -----------------------------

        success = self.engine.make_move(
            from_row,
            from_col,
            to_row,
            to_col,
            promotion
        )

        if not success:
            return False

        # -----------------------------
        # Sounds
        # -----------------------------

        if captured_piece:

            self.capture_piece(
                captured_piece
            )

            self.sound.play_capture()

        else:

            self.sound.play_move()

        if self.engine.board.is_check():

            self.sound.play_check()

        if self.engine.board.is_checkmate():

            self.sound.play_check()

        # -----------------------------
        # Refresh Board
        # -----------------------------

        self.sync_board()

        self.last_move = self.engine.get_last_move()

        self.move_history = list(
            self.engine.board.move_stack
        )

        SaveManager.save(self)

        self.clear_selection()

        self.awaiting_promotion = False

        self.promotion_move = None

        self.promotion_ui.hide()

        return True
    
        # ==========================================================
    # FINISH PROMOTION
    # ==========================================================

    def finish_promotion(
        self,
        promotion
    ):

        if self.promotion_move is None:
            return

        (
            from_row,
            from_col,
            to_row,
            to_col
        ) = self.promotion_move

        self.awaiting_promotion = False

        self.promotion_move = None

        self.make_move(
            from_row,
            from_col,
            to_row,
            to_col,
            promotion
        )

        # ==========================================================
    # MOUSE
    # ==========================================================

    def mouse_down(
        self,
        pos
    ):

        # ------------------------------------------
        # Promotion Popup
        # ------------------------------------------

        if self.awaiting_promotion:

            promotion = self.promotion_ui.click(pos)

            if promotion is None:
                return

            self.finish_promotion(
                promotion
            )

            return

        # ------------------------------------------
        # Ignore clicks while animation is running
        # ------------------------------------------

        if self.animating:
            return
        
        # ==========================================
        # Buttons
        # ==========================================

        if self.restart_button.collidepoint(pos):

            self.restart()

            return

        if self.undo_button.collidepoint(pos):

            self.undo()

            return

        if self.flip_button.collidepoint(pos):

            self.flip()

            return

        square = self.screen_to_board(
            pos[0],
            pos[1]
        )

        if square is None:

            self.clear_selection()

            return

        row, col = square

        clicked_piece = self.get_piece(
            row,
            col
        )

        # ------------------------------------------
        # Nothing selected yet
        # ------------------------------------------

        if self.selected_piece is None:

            if (
                clicked_piece
                and
                clicked_piece.color == self.engine.turn()
                and
                self.can_control(clicked_piece.color)
            ):

                self.select_square(
                    row,
                    col
                )

            return

        # ------------------------------------------
        # Clicked same piece
        # ------------------------------------------

        if clicked_piece == self.selected_piece:

            self.clear_selection()

            return

        # ------------------------------------------
        # Clicked another friendly piece
        # ------------------------------------------

        if (
            clicked_piece
            and
            clicked_piece.color == self.engine.turn()
            and
            self.can_control(clicked_piece.color)
        ):

            self.select_square(
                row,
                col
            )

            return

        # ------------------------------------------
        # Move piece
        # ------------------------------------------

        if (
            row,
            col
        ) in self.legal_moves:

            self.start_move_animation(

                self.selected_piece.row,

                self.selected_piece.col,

                row,

                col

            )

            return

        # ------------------------------------------
        # Invalid click
        # ------------------------------------------

        self.clear_selection()

        # ==========================================================
    # MOUSE MOTION
    # ==========================================================

    def mouse_motion(
        self,
        pos
    ):

        self.mouse_x = pos[0]

        self.mouse_y = pos[1]


    # ==========================================================
    # MOUSE UP
    # ==========================================================

    def mouse_up(
        self,
        pos
    ):

        pass

    def draw_board(self, surface):

        for row in range(8):

            for col in range(8):

                if (row + col) % 2 == 0:
                    color = LIGHT_SQUARE
                else:
                    color = DARK_SQUARE

                x = BOARD_X + col * TILE_SIZE
                y = BOARD_Y + row * TILE_SIZE

                pygame.draw.rect(
                    surface,
                    color,
                    (
                        x,
                        y,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                )

    # ==========================================================
    # DRAW
    # ==========================================================

    def draw(self, surface):

        self.draw_board(surface)

        self.draw_side_panel(surface)

        self.draw_captured(surface)

        self.draw_move_history(surface)

        self.draw_material(surface)

        self.draw_clock(surface)

        self.draw_last_move(surface)

        self.draw_check(surface)

        self.draw_legal_moves(surface)

        self.draw_selected(surface)

        self.draw_pieces(surface)

        self.draw_coordinates(surface)

        self.draw_turn(surface)

        self.draw_buttons(surface)

        if self.awaiting_promotion:

            self.promotion_ui.draw(surface)

        self.draw_game_over(surface)

        # ==========================================================
    # DRAW PIECES
    # ==========================================================

    def draw_pieces(self, surface):

        for row in self.board:

            for piece in row:

                if piece is None:
                    continue

                if self.animating and piece == self.animation_piece:
                    continue

                draw_row = piece.row
                draw_col = piece.col

                if self.flipped:
                    draw_row = 7 - draw_row
                    draw_col = 7 - draw_col

                offset = (TILE_SIZE - PIECE_SIZE) // 2

                piece.x = BOARD_X + draw_col * TILE_SIZE + offset
                piece.y = BOARD_Y + draw_row * TILE_SIZE + offset

                piece.draw(surface)

        if self.animating and self.animation_piece:
            self.animation_piece.draw(surface)

    # ==========================================================
    # DRAW SELECTED
    # ==========================================================

    def draw_selected(self, surface):

        if self.selected_piece is None:
            return

        row = self.selected_piece.row
        col = self.selected_piece.col

        if self.flipped:
            row = 7 - row
            col = 7 - col

        x = BOARD_X + col * TILE_SIZE
        y = BOARD_Y + row * TILE_SIZE

        pygame.draw.rect(
            surface,
            SELECTED_COLOR,
            (x, y, TILE_SIZE, TILE_SIZE),
            4
        )

    # ==========================================================
    # DRAW LEGAL MOVES
    # ==========================================================

    def draw_legal_moves(self, surface):

        for row, col in self.legal_moves:

            x, y = self.board_to_screen(
                row,
                col
            )

            pygame.draw.circle(

                surface,

                (60,180,255),

                (

                    x + SQUARE_SIZE//2,

                    y + SQUARE_SIZE//2

                ),

                12

            )

            # ==========================================================
    # LAST MOVE
    # ==========================================================

    def draw_last_move(self, surface):

        if self.last_move is None:
            return

        move = self.last_move

        from_row, from_col = self.engine.coords_from_square(
            move.from_square
        )

        to_row, to_col = self.engine.coords_from_square(
            move.to_square
        )

        for row, col in [

            (from_row, from_col),

            (to_row, to_col)

        ]:

            x, y = self.board_to_screen(
                row,
                col
            )

            s = pygame.Surface(
                (
                    SQUARE_SIZE,
                    SQUARE_SIZE
                ),
                pygame.SRCALPHA
            )

            s.fill((255,255,0,70))

            surface.blit(
                s,
                (x,y)
            )

    # ==========================================================
    # CHECK
    # ==========================================================

    def draw_check(self, surface):

        if not self.engine.board.is_check():
            return

        king_square = self.engine.board.king(
            self.engine.board.turn
        )

        row, col = self.engine.coords_from_square(
            king_square
        )

        x, y = self.board_to_screen(
            row,
            col
        )

        pygame.draw.rect(

            surface,

            (255,0,0),

            (

                x,
                y,
                SQUARE_SIZE,
                SQUARE_SIZE

            ),

            5

        )

    # ==========================================================
    # DRAW COORDINATES
    # ==========================================================

    def draw_coordinates(self, surface):

        font = pygame.font.SysFont(
            FONT_NAME,
            16,
            bold=True
        )

        files = "ABCDEFGH"

        for col in range(8):

            board_col = col if not self.flipped else 7 - col

            text = font.render(
                files[board_col],
                True,
                (210, 210, 210)
            )

            x = BOARD_X + col * TILE_SIZE + 6
            y = BOARD_Y + BOARD_HEIGHT + 4

            surface.blit(text, (x, y))

        for row in range(8):

            number = 8 - row if not self.flipped else row + 1

            text = font.render(
                str(number),
                True,
                (210, 210, 210)
            )

            x = BOARD_X - 18
            y = BOARD_Y + row * TILE_SIZE + 4

            surface.blit(text, (x, y))

        # ==========================================================
    # DRAW TURN
    # ==========================================================

    def draw_turn(self, surface):

        font = pygame.font.SysFont(
            FONT_NAME,
            24,
            bold=True
        )

        if self.engine.turn() == chess.WHITE:

            text = "White to Move"

        else:

            text = "Black to Move"

        label = font.render(
            text,
            True,
            WHITE
        )

        surface.blit(
            label,
            (
                BOARD_X + BOARD_WIDTH // 2 - label.get_width() // 2,
                10
            )
        )

    # ==========================================================
    # GAME OVER
    # ==========================================================

    def draw_game_over(self, surface):

        if not self.game_over():
            return

        font = pygame.font.SysFont(
            FONT_NAME,
            48,
            bold=True
        )

        result = self.result()

        text = font.render(
            result,
            True,
            (255,255,255)
        )

        bg = pygame.Surface(
            (WIDTH,90),
            pygame.SRCALPHA
        )

        bg.fill((0,0,0,180))

        surface.blit(
            bg,
            (
                0,
                HEIGHT//2-45
            )
        )

        surface.blit(

            text,

            (

                WIDTH//2-text.get_width()//2,

                HEIGHT//2-text.get_height()//2

            )

        )

    # ==========================================================
    # DRAW BUTTONS
    # ==========================================================

    def draw_buttons(self, surface):

        buttons = [

            (self.restart_button, "Restart"),

            (self.undo_button, "Undo"),

            (self.flip_button, "Flip Board")

        ]

        mouse = pygame.mouse.get_pos()

        for rect, text in buttons:

            color = (60,60,60)

            if rect.collidepoint(mouse):

                color = (95,95,95)

            pygame.draw.rect(

                surface,

                color,

                rect,

                border_radius=10

            )

            pygame.draw.rect(

                surface,

                (220,220,220),

                rect,

                2,

                border_radius=10

            )

            label = self.button_font.render(

                text,

                True,

                WHITE

            )

            surface.blit(

                label,

                (

                    rect.centerx-label.get_width()//2,

                    rect.centery-label.get_height()//2

                )

            )

    # ==========================================================
    # SIDE PANEL
    # ==========================================================

    def draw_side_panel(self, surface):

        panel = pygame.Rect(
            BOARD_X + BOARD_WIDTH,
            0,
            WIDTH - (BOARD_X + BOARD_WIDTH),
            HEIGHT
        )

        pygame.draw.rect(
            surface,
            (34, 34, 34),
            panel
        )

        pygame.draw.line(
            surface,
            (70, 70, 70),
            (BOARD_X + BOARD_WIDTH, 0),
            (BOARD_X + BOARD_WIDTH, HEIGHT),
            2
        )

    # ==========================================================
    # CAPTURED PIECES
    # ==========================================================

    def draw_captured(self, surface):

        font = pygame.font.SysFont(
            FONT_NAME,
            22,
            bold=True
        )

        title = font.render(
            "Captured",
            True,
            WHITE
        )

        surface.blit(
            title,
            (SIDEBAR_X + 20, 20)
        )

        x = SIDEBAR_X + 20
        y = 60

        for piece in self.black_captured:

            if piece.image:

                image = pygame.transform.smoothscale(
                    piece.image,
                    (34, 34)
                )

                surface.blit(
                    image,
                    (x, y)
                )

            x += 36

        # -------------------------
        # White captured pieces
        # -------------------------

        SIDEBAR_X + 20
        y = 115

        for piece in self.white_captured:

            if piece.image:

                image = pygame.transform.smoothscale(
                    piece.image,
                    (34, 34)
                )

                surface.blit(
                    image,
                    (x, y)
                )

            x += 36

    # ==========================================================
    # MOVE HISTORY
    # ==========================================================

    def draw_move_history(self, surface):

        title_font = pygame.font.SysFont(

            FONT_NAME,

            22,

            bold=True

        )

        font = pygame.font.SysFont(

            FONT_NAME,

            18

        )

        title = title_font.render(

            "Moves",

            True,

            WHITE

        )

        surface.blit(
            title,
            (SIDEBAR_X + 20, 180)
        )

        y = 220

        moves = self.engine.history()

        for i in range(0, len(moves), 2):

            white = moves[i]

            black = ""

            if i + 1 < len(moves):

                black = moves[i+1]

            line = f"{i//2+1}. {white} {black}"

            text = font.render(

                line,

                True,

                (230,230,230)

            )

            surface.blit(
                text,
                (SIDEBAR_X + 20, y)
            )

            y += 24

            if y > HEIGHT - 20:

                break

    # ==========================================================
    # MATERIAL
    # ==========================================================

    def draw_material(self, surface):

        values = {

            chess.PAWN:1,

            chess.KNIGHT:3,

            chess.BISHOP:3,

            chess.ROOK:5,

            chess.QUEEN:9

        }

        white = 0
        black = 0

        for square in chess.SQUARES:

            piece = self.engine.board.piece_at(square)

            if piece is None:

                continue

            if piece.piece_type == chess.KING:

                continue

            if piece.color == chess.WHITE:

                white += values[piece.piece_type]

            else:

                black += values[piece.piece_type]

        font = pygame.font.SysFont(

            FONT_NAME,

            22,

            bold=True

        )

        text = font.render(

            f"Material  W:{white}  B:{black}",

            True,

            WHITE

        )

        surface.blit(
            text,
            (SIDEBAR_X + 20,560)
        )

    # ==========================================================
    # DRAW CLOCK
    # ==========================================================

    def draw_clock(self, surface):

        font = pygame.font.SysFont(

            FONT_NAME,

            28,

            bold=True

        )

        white = font.render(

            self.format_time(self.white_time),

            True,

            WHITE

        )

        black = font.render(

            self.format_time(self.black_time),

            True,

            WHITE

        )

        surface.blit(

            white,

            (720, 430)

        )

        surface.blit(

            black,

            (720, 480)

        )

        label = pygame.font.SysFont(

            FONT_NAME,

            22,

            bold=True

        )

        surface.blit(

            label.render("White", True, WHITE),

            (695, 405)

        )

        surface.blit(

            label.render("Black", True, WHITE),

            (695, 455)

        )

    # ==========================================================
    # FORMAT CLOCK
    # ==========================================================

    def format_time(self, seconds):

        minutes = int(seconds // 60)

        secs = int(seconds % 60)

        return f"{minutes:02}:{secs:02}"