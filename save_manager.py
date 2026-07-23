import json
import chess


class SaveManager:

    SAVE_FILE = "savegame.json"

    @staticmethod
    def save(board):

        data = {
            "fen": board.engine.board.fen(),
            "flipped": board.flipped,
            "solo": board.solo,
            "player_is_white": board.player_is_white
        }

        with open(SaveManager.SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load(board):

        try:

            with open(SaveManager.SAVE_FILE, "r") as f:
                data = json.load(f)

        except FileNotFoundError:

            return False

        board.engine.board = chess.Board(data["fen"])

        board.flipped = data.get(
            "flipped",
            False
        )

        board.solo = data.get(
            "solo",
            True
        )

        board.player_is_white = data.get(
            "player_is_white",
            True
        )

        board.sync_board()

        return True