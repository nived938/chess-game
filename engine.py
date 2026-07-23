import chess
import chess.pgn


class ChessEngine:
    """
    Wrapper around python-chess.
    Handles all chess rules and game state.
    """

    def __init__(self):

        self.board = chess.Board()

        self.move_history = []

        self.last_move = None

    # ==========================================
    # BASIC GAME STATE
    # ==========================================

    def reset(self):

        self.board.reset()

        self.move_history.clear()

        self.last_move = None

    def turn(self):

        return self.board.turn

    def fen(self):

        return self.board.fen()

    def copy(self):

        return self.board.copy()

    # ==========================================
    # GAME STATUS
    # ==========================================

    def is_check(self):

        return self.board.is_check()

    def is_checkmate(self):

        return self.board.is_checkmate()

    def is_stalemate(self):

        return self.board.is_stalemate()

    def is_insufficient_material(self):

        return self.board.is_insufficient_material()

    def is_fifty_moves(self):

        return self.board.is_fifty_moves()

    def is_repetition(self):

        return self.board.is_repetition()

    def is_game_over(self):

        return self.board.is_game_over()

    def result(self):

        if not self.is_game_over():
            return None

        return self.board.result()

    # ==========================================
    # PIECE ACCESS
    # ==========================================

    def piece_at(self, row, col):
        """
        Returns a python-chess Piece or None.
        """

        square = chess.square(col, 7 - row)

        return self.board.piece_at(square)

    def piece_symbol(self, row, col):
        """
        Returns 'P', 'k', etc., or None.
        """

        piece = self.piece_at(row, col)

        if piece is None:
            return None

        return piece.symbol()

    # ==========================================
    # TURN HELPERS
    # ==========================================

    def is_white_turn(self):

        return self.board.turn == chess.WHITE

    def is_black_turn(self):

        return self.board.turn == chess.BLACK

    # ==========================================
    # KING LOCATION
    # ==========================================

    def king_square(self, color):

        square = self.board.king(color)

        if square is None:
            return None

        row = 7 - chess.square_rank(square)
        col = chess.square_file(square)

        return row, col

    # ==========================================
    # LAST MOVE
    # ==========================================

    def get_last_move(self):

        return self.last_move

    # ==========================================
    # MOVE HISTORY
    # ==========================================

    def history(self):

        return self.move_history

    def move_count(self):

        return len(self.move_history)
    
        # ==========================================
    # LEGAL MOVES
    # ==========================================

    def legal_moves(self):
        """
        Returns a list of all legal moves.
        """

        return list(self.board.legal_moves)

    def legal_moves_from(self, row, col):
        """
        Returns all legal moves starting from a square.
        """

        from_square = chess.square(col, 7 - row)

        moves = []

        for move in self.board.legal_moves:
            if move.from_square == from_square:
                moves.append(move)

        return moves

    def legal_targets(self, row, col):
        """
        Returns a list of (row, col) destination squares.
        """

        targets = []

        for move in self.legal_moves_from(row, col):

            r = 7 - chess.square_rank(move.to_square)
            c = chess.square_file(move.to_square)

            targets.append((r, c))

        return targets

    # ==========================================
    # MOVE VALIDATION
    # ==========================================

    def is_legal(self, from_row, from_col, to_row, to_col):

        from_square = chess.square(from_col, 7 - from_row)
        to_square = chess.square(to_col, 7 - to_row)

        move = chess.Move(from_square, to_square)

        if move in self.board.legal_moves:
            return True

        # Promotion moves
        for promotion in (
            chess.QUEEN,
            chess.ROOK,
            chess.BISHOP,
            chess.KNIGHT,
        ):
            move = chess.Move(
                from_square,
                to_square,
                promotion=promotion
            )

            if move in self.board.legal_moves:
                return True

        return False

    # ==========================================
    # MAKE MOVE
    # ==========================================

    def make_move(
        self,
        from_row,
        from_col,
        to_row,
        to_col,
        promotion=None,
    ):

        from_square = chess.square(from_col, 7 - from_row)
        to_square = chess.square(to_col, 7 - to_row)

        move = chess.Move(
            from_square,
            to_square,
            promotion=promotion
        )

        # Automatically promote to queen if needed
        if (
            promotion is None
            and self.board.piece_at(from_square)
            and self.board.piece_at(from_square).piece_type == chess.PAWN
            and (to_row == 0 or to_row == 7)
        ):
            move = chess.Move(
                from_square,
                to_square,
                promotion=chess.QUEEN
            )

        if move not in self.board.legal_moves:
            return False

        self.board.push(move)

        self.move_history.append(move)

        self.last_move = move

        return True

    # ==========================================
    # UNDO
    # ==========================================

    def undo(self):

        if not self.board.move_stack:
            return False

        self.board.pop()

        if self.move_history:
            self.move_history.pop()

        if self.board.move_stack:
            self.last_move = self.board.move_stack[-1]
        else:
            self.last_move = None

        return True

    # ==========================================
    # SPECIAL MOVE HELPERS
    # ==========================================

    def is_capture(self, move):

        return self.board.is_capture(move)

    def is_castling(self, move):

        return self.board.is_castling(move)

    def is_en_passant(self, move):

        return self.board.is_en_passant(move)

    def gives_check(self, move):

        return self.board.gives_check(move)

    # ==========================================
    # PROMOTION
    # ==========================================

    def is_promotion_square(
        self,
        from_row,
        from_col,
        to_row,
        to_col,
    ):

        piece = self.piece_at(from_row, from_col)

        if piece is None:
            return False

        if piece.piece_type != chess.PAWN:
            return False

        if piece.color == chess.WHITE:
            return to_row == 0

        return to_row == 7
    
        # ==========================================
    # MOVE NOTATION
    # ==========================================

    def move_to_san(self, move):
        """
        Convert a move to Standard Algebraic Notation (SAN).
        Example: e4, Nf3, O-O
        """

        try:
            board_copy = self.board.copy()
            return board_copy.san(move)
        except Exception:
            return ""

    def move_to_uci(self, move):
        """
        Convert a move to UCI notation.
        Example: e2e4
        """

        return move.uci()

    # ==========================================
    # BOARD COORDINATES
    # ==========================================

    def square_from_coords(self, row, col):

        return chess.square(col, 7 - row)

    def coords_from_square(self, square):

        file = chess.square_file(square)
        rank = chess.square_rank(square)

        row = 7 - rank
        col = file

        return row, col

    # ==========================================
    # FEN
    # ==========================================

    def load_fen(self, fen):

        try:
            self.board.set_fen(fen)

            self.move_history.clear()
            self.last_move = None

            return True

        except ValueError:
            return False

    def current_fen(self):

        return self.board.fen()

    # ==========================================
    # PGN
    # ==========================================

    def export_pgn(self):

        game = chess.pgn.Game()

        node = game

        temp_board = chess.Board()

        for move in self.move_history:
            node = node.add_variation(move)
            temp_board.push(move)

        return str(game)

    # ==========================================
    # DRAW CONDITIONS
    # ==========================================

    def is_draw(self):

        return self.board.is_stalemate() \
            or self.board.is_insufficient_material() \
            or self.board.is_fifty_moves() \
            or self.board.is_repetition()

    # ==========================================
    # BOARD INFORMATION
    # ==========================================

    def pieces(self):
        """
        Returns a dictionary:
        {square: chess.Piece}
        """

        return self.board.piece_map()

    def occupied_squares(self):

        return list(self.board.piece_map().keys())

    # ==========================================
    # GAME STATUS
    # ==========================================

    def status(self):

        if self.is_checkmate():
            return "Checkmate"

        if self.is_stalemate():
            return "Stalemate"

        if self.is_insufficient_material():
            return "Draw by insufficient material"

        if self.is_fifty_moves():
            return "Draw by fifty-move rule"

        if self.is_repetition():
            return "Draw by repetition"

        if self.is_check():
            return "Check"

        return "Playing"

    # ==========================================
    # RESTART
    # ==========================================

    def restart(self):

        self.reset()

    # ==========================================
    # DEBUG
    # ==========================================

    def print_board(self):

        print(self.board)

    def __str__(self):

        return self.board.unicode()
    
    