import os
import chess
import chess.engine


class ChessAI:

    def __init__(
        self,
        stockfish_path="stockfish/stockfish.exe",
        difficulty=1,
        think_time=0.3
    ):

        self.stockfish_path = stockfish_path

        self.difficulty = difficulty

        self.think_time = think_time

        self.engine = None

        self.enabled = True

        self.color = chess.BLACK

        self.load_engine()

    # ==========================================================
    # LOAD ENGINE
    # ==========================================================

    def load_engine(self):

        print("Loading Stockfish...")

        print(self.stockfish_path)

        self.engine = chess.engine.SimpleEngine.popen_uci(
            self.stockfish_path
        )

        print("Stockfish Loaded!")

        self.set_difficulty(self.difficulty)

    # ==========================================================
    # ENABLE / DISABLE
    # ==========================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    def is_enabled(self):

        return self.enabled

    # ==========================================================
    # AI COLOR
    # ==========================================================

    def set_color(self, color):

        self.color = color

    def get_color(self):

        return self.color

    # ==========================================================
    # THINK TIME
    # ==========================================================

    def set_think_time(self, seconds):

        self.think_time = seconds

    def get_think_time(self):

        return self.think_time

    # ==========================================================
    # DIFFICULTY
    # ==========================================================

    def set_difficulty(self, level):

        level = max(1, min(level, 20))

        self.difficulty = level

        skill = level - 1

        self.engine.configure({

            "Skill Level": skill

        })

    def get_difficulty(self):

        return self.difficulty
    
    # ==========================================================
    # SHOULD AI MOVE?
    # ==========================================================

    def should_move(self, board):

        if not self.enabled:
            return False

        if board.is_game_over():
            return False

        return board.turn == self.color

    # ==========================================================
    # BEST MOVE
    # ==========================================================

    def get_best_move(self, board):

        if self.engine is None:
            return None

        if board.is_game_over():
            return None

        try:

            result = self.engine.play(
                board,
                chess.engine.Limit(
                    time=self.think_time
                )
            )

            return result.move

        except Exception as e:

            print("Stockfish Error:", e)

            return None

    # ==========================================================
    # MAKE AI MOVE
    # ==========================================================

    def make_move(self, board):

        if not self.should_move(board):
            return None

        return self.get_best_move(board)

    # ==========================================================
    # EVALUATE POSITION
    # ==========================================================

    def evaluate(self, board):

        info = self.engine.analyse(
            board,
            chess.engine.Limit(depth=12)
        )

        return info

    # ==========================================================
    # SET ELO
    # ==========================================================

    def set_elo(self, elo):

        elo = max(1350, min(elo, 3200))

        self.engine.configure({

            "UCI_LimitStrength": True,

            "UCI_Elo": elo

        })

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        pass

    # ==========================================================
    # CLOSE ENGINE
    # ==========================================================

    def close(self):

        if self.engine:

            self.engine.quit()

            self.engine = None

    # ==========================================================
    # DEBUG
    # ==========================================================

    def __str__(self):

        return (
            f"ChessAI("
            f"Difficulty={self.difficulty}, "
            f"Think={self.think_time}s)"
        )