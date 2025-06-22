import logging
from typing import Dict

Position = str  # e.g., 'e4'
Piece = str     # e.g., 'P', 'k', etc.

logger = logging.getLogger(__name__)


class ChessGame:
    def __init__(self):
        self.board: Dict[Position, Piece] = self._initial_board()
        self.turn = 'white'
        self.game_over = False
        logger.info("ChessGame initialized.")

    def _initial_board(self) -> Dict[Position, Piece]:
        # Setup pieces with uppercase for White, lowercase for Black
        pieces = {
            'a1': 'R', 'b1': 'N', 'c1': 'B', 'd1': 'Q', 'e1': 'K', 'f1': 'B', 'g1': 'N', 'h1': 'R',
            'a2': 'P', 'b2': 'P', 'c2': 'P', 'd2': 'P', 'e2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P',
            'a7': 'p', 'b7': 'p', 'c7': 'p', 'd7': 'p', 'e7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p',
            'a8': 'r', 'b8': 'n', 'c8': 'b', 'd8': 'q', 'e8': 'k', 'f8': 'b', 'g8': 'n', 'h8': 'r',
        }
        board = {}
        for rank in '12345678':
            for file in 'abcdefgh':
                pos = file + rank
                board[pos] = pieces.get(pos, '.')
        logger.debug("Initial board setup complete.")
        return board

    def is_valid_pos(self, pos: Position) -> bool:
        return len(pos) == 2 and pos[0] in 'abcdefgh' and pos[1] in '12345678'

    def is_white_piece(self, piece: Piece) -> bool:
        return piece.isupper() and piece != '.'

    def is_black_piece(self, piece: Piece) -> bool:
        return piece.islower() and piece != '.'

    def get_piece_color(self, piece: Piece) -> str:
        if piece == '.':
            return 'none'
        return 'white' if self.is_white_piece(piece) else 'black'

    def _piece_name(self, symbol: str) -> str:
        return {
            'p': 'pawn', 'r': 'rook', 'n': 'knight',
            'b': 'bishop', 'q': 'queen', 'k': 'king'
        }.get(symbol.lower(), 'piece')

    def check_game_over(self):
        pieces = self.board.values()
        has_white_king = 'K' in pieces
        has_black_king = 'k' in pieces

        if not has_white_king:
            logger.info("Black wins — White's king is missing.")
            self.game_over = True
        elif not has_black_king:
            logger.info("White wins — Black's king is missing.")
            self.game_over = True

    def make_move(self, from_pos: Position, to_pos: Position) -> bool:
        logger.debug(f"Attempting move from {from_pos} to {to_pos} by {self.turn}.")
        if not (self.is_valid_pos(from_pos) and self.is_valid_pos(to_pos)):
            logger.warning("Invalid board position.")
            return False

        piece = self.board[from_pos]
        if piece == '.':
            logger.warning("No piece at source position.")
            return False

        if self.get_piece_color(piece) != self.turn:
            logger.warning(f"It's {self.turn}'s turn, but tried to move {piece}.")
            return False

        target_piece = self.board[to_pos]
        if self.get_piece_color(target_piece) == self.turn:
            logger.warning("Cannot capture your own piece.")
            return False

        if not self.is_legal_move(piece, from_pos, to_pos):
            logger.warning("Illegal move attempted.")
            return False

        if target_piece != '.':
            logger.info(f"{self.turn.capitalize()} {self._piece_name(piece)} captures {self.get_piece_color(target_piece)} {self._piece_name(target_piece)} on {to_pos}.")

        self.board[to_pos] = piece
        self.board[from_pos] = '.'

        self.check_game_over()

        if not self.game_over:
            self.turn = 'black' if self.turn == 'white' else 'white'
            logger.debug(f"Turn switched to {self.turn}.")
        return True

    def is_legal_move(self, piece: Piece, from_pos: Position, to_pos: Position) -> bool:
        # Define movement rules for each piece type (no castling, no en passant, no promotion)
        df = ord(to_pos[0]) - ord(from_pos[0])
        dr = int(to_pos[1]) - int(from_pos[1])

        if piece.upper() == 'P':
            return self._legal_pawn_move(piece, from_pos, to_pos, df, dr)
        if piece.upper() == 'N':
            return (abs(df), abs(dr)) in [(1, 2), (2, 1)]
        if piece.upper() == 'B':
            return abs(df) == abs(dr) and self._is_path_clear(from_pos, to_pos)
        if piece.upper() == 'R':
            return (df == 0 or dr == 0) and self._is_path_clear(from_pos, to_pos)
        if piece.upper() == 'Q':
            return (abs(df) == abs(dr) or df == 0 or dr == 0) and self._is_path_clear(from_pos, to_pos)
        if piece.upper() == 'K':
            return max(abs(df), abs(dr)) == 1
        return False

    def _legal_pawn_move(self, piece: Piece, from_pos: Position, to_pos: Position, df: int, dr: int) -> bool:
        direction = 1 if piece.isupper() else -1
        start_rank = '2' if piece.isupper() else '7'
        target = self.board[to_pos]

        if df == 0:
            if dr == direction and target == '.':
                return True
            if from_pos[1] == start_rank and dr == 2 * direction:
                intermediate = from_pos[0] + str(int(from_pos[1]) + direction)
                return self.board[intermediate] == '.' and target == '.'
        if abs(df) == 1 and dr == direction and target != '.' and self.get_piece_color(target) != self.get_piece_color(piece):
            return True
        return False

    def _is_path_clear(self, from_pos: Position, to_pos: Position) -> bool:
        # Checks if path is clear between from_pos and to_pos for sliding pieces
        df = ord(to_pos[0]) - ord(from_pos[0])
        dr = int(to_pos[1]) - int(from_pos[1])
        step_f = (df > 0) - (df < 0)
        step_r = (dr > 0) - (dr < 0)

        f, r = ord(from_pos[0]) + step_f, int(from_pos[1]) + step_r
        while (f, r) != (ord(to_pos[0]), int(to_pos[1])):
            pos = chr(f) + str(r)
            if self.board[pos] != '.':
                return False
            f += step_f
            r += step_r
        return True

    def remove_piece(self, symbol: str):
        for pos, piece in self.board.items():
            if piece == symbol:
                self.board[pos] = '.'
                logger.debug(f"Removed piece {symbol} from {pos}.")
                break
