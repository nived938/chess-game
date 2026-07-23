import pygame
import chess
import time

from ai import ChessAI
from board import Board
from piece import load_piece_images
from constants import *


class Game:

    def __init__(
        self,
        solo=True,
        player_is_white=True
    ):
        print("----------------")
        print("solo =", solo)
        print("player_is_white =", player_is_white)
        print("----------------")

        # Load all piece images once
        load_piece_images()

        # Chess board
        self.board = Board()

        self.board.solo = solo

        self.board.player_is_white = player_is_white

        # ==========================================
        # Game Mode
        # ==========================================

        self.solo = solo

        self.player_is_white = player_is_white

        # ==========================================
        # First Move
        # ==========================================

        self.first_ai_move = (
            self.solo
            and not self.player_is_white
        )

        self.ai = ChessAI()

        if self.solo:

            if self.player_is_white:

                self.ai.set_color(chess.BLACK)

            else:

                self.ai.set_color(chess.WHITE)

        else:

            self.ai.disable()

        # AI Thinking
        self.ai_delay = 1000          # milliseconds
        self.ai_start_time = None
        self.ai_thinking = False

        # Running state
        self.running = True

        # Background color
        self.background_color = BACKGROUND

    def update_ai(self):

        if not self.solo:
            return

        if self.board.animating:
            return

        if self.board.game_over():
            return
        
        if self.board.engine.turn() != self.ai.get_color():
            return

        move = self.ai.get_best_move(
            self.board.engine.board
        )

        if move is None:
            return

        from_row, from_col = self.board.engine.coords_from_square(
            move.from_square
        )

        to_row, to_col = self.board.engine.coords_from_square(
            move.to_square
        )

        promotion = move.promotion

        self.board.start_move_animation(
            from_row,
            from_col,
            to_row,
            to_col,
            promotion
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):

        self.board.update()

        # ==========================================
        # AI plays first if player chose Black
        # ==========================================

        if self.first_ai_move:

            if not self.board.animating:

                self.update_ai()

                self.first_ai_move = False

            return

        if not self.solo:
            return

        if self.board.game_over():
            return

        # AI only moves on its turn
        if self.board.engine.turn() != self.ai.get_color():

            self.ai_thinking = False
            self.ai_start_time = None
            return

        current_time = pygame.time.get_ticks()

        # Start thinking
        if not self.ai_thinking:

            self.ai_thinking = True
            self.ai_start_time = current_time
            return

        # Wait before moving
        if current_time - self.ai_start_time < self.ai_delay:
            return

        self.update_ai()

        self.ai_thinking = False
        self.ai_start_time = None

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen):

        screen.fill(self.background_color)

        print("Calling draw:", self.board.draw)
        self.board.draw(screen)

        if self.ai_thinking:

            font = pygame.font.SysFont(
                FONT_NAME,
                24,
                bold=True
            )

            text = font.render(
                "ChessAI is thinking...",
                True,
                (255, 255, 255)
            )

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    20
                )
            )

    # =========================================================
    # EVENT HANDLING
    # =========================================================

    def handle_event(self, event):

        if event.type == pygame.QUIT:

            self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                self.board.mouse_down(event.pos)

        elif event.type == pygame.MOUSEMOTION:

            self.board.mouse_motion(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                self.board.mouse_up(event.pos)

        elif event.type == pygame.KEYDOWN:

            self.board.key_down(event.key)

    # =========================================================
    # SHORTCUTS
    # =========================================================

    def restart(self):

        self.board.restart()

    def undo(self):

        self.board.undo()

    def flip(self):

        self.board.flip()

    # =========================================================
    # GAME STATUS
    # =========================================================

    def is_running(self):

        return self.running

    def stop(self):

        self.running = False

    def is_game_over(self):

        return self.board.game_over()

    def result(self):

        return self.board.result()

    # =========================================================
    # ACCESSORS
    # =========================================================

    def get_board(self):

        return self.board

    def status(self):

        return self.board.status()

    def current_turn(self):

        if self.board.white_to_move():
            return "White"

        return "Black"

    # =========================================================
    # DEBUG
    # =========================================================

    def print_board(self):

        self.board.print_board()