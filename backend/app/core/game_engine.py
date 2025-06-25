import logging
from typing import Dict

Position = str  # e.g., 'e4'
Piece = str     # e.g., 'P', 'k', etc.

logger = logging.getLogger(__name__)


class ChessGame:
    """
    A class to manage the state and rules of a chess game.
    Provides methods to make moves, validate legality, and detect game-over conditions.
    """

    def __init__(self):
        """
        Initialize the chess game with the starting board, white's turn, and game not over.
        """
        self.board: Dict[Position, Piece] = self._initial_board()
        self.turn = 'white'
        self.game_over = False
        logger.info("ChessGame initialized.")

    def _initial_board(self) -> Dict[Position, Piece]:
        """
        Create and return the initial board layout for a new chess game.

        Returns:
            Dict[Position, Piece]: A mapping of positions to pieces.
        """
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
        """
        Check whether a position is valid on a chess board.

        Args:
            pos (Position): Position string, e.g., 'e4'.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        return len(pos) == 2 and pos[0] in 'abcdefgh' and pos[1] in '12345678'

    def is_white_piece(self, piece: Piece) -> bool:
        """
        Check if a piece belongs to White.

        Args:
            piece (Piece): Piece character.

        Returns:
            bool: True if white, False otherwise.
        """
        return piece.isupper() and piece != '.'

    def is_black_piece(self, piece: Piece) -> bool:
        """
        Check if a piece belongs to Black.

        Args:
            piece (Piece): Piece character.

        Returns:
            bool: True if black, False otherwise.
        """
        return piece.islower() and piece != '.'

    def get_piece_color(self, piece: Piece) -> str:
        """
        Return the color of the piece.

        Args:
            piece (Piece): Piece character.

        Returns:
            str: 'white', 'black', or 'none'.
        """
        if piece == '.':
            return 'none'
        return 'white' if self.is_white_piece(piece) else 'black'

    def _piece_name(self, symbol: str) -> str:
        """
        Convert a piece symbol to a human-readable name.

        Args:
            symbol (str): Piece character.

        Returns:
            str: Name of the piece.
        """
        return {
            'p': 'pawn', 'r': 'rook', 'n': 'knight',
            'b': 'bishop', 'q': 'queen', 'k': 'king'
        }.get(symbol.lower(), 'piece')

    def check_game_over(self):
        """
        Check if either king is missing and set the game_over flag if so.
        Logs the result.
        """
        pieces = self.board.values()
        has_white_king = 'K' in pieces
        has_black_king = 'k' in pieces

        if not has_white_king:
            logger.info("Game over: Black wins — White's king is missing from the board.")
            self.game_over = True
        elif not has_black_king:
            logger.info("Game over: White wins — Black's king is missing from the board.")
            self.game_over = True

    def make_move(self, from_pos: Position, to_pos: Position) -> bool:
        """
        Attempt to move a piece from one position to another.

        Args:
            from_pos (Position): Source square.
            to_pos (Position): Destination square.

        Returns:
            bool: True if move is legal and executed, False otherwise.
        """
        logger.debug(f"Attempting move from {from_pos} to {to_pos} by {self.turn} (moving piece: {self.board[from_pos]} [{self.get_piece_color(self.board[from_pos])}]).")
        if not (self.is_valid_pos(from_pos) and self.is_valid_pos(to_pos)):
            logger.warning(f"Invalid board position: from {from_pos} to {to_pos}.")
            return False

        piece = self.board[from_pos]
        if piece == '.':
            logger.warning(f"No piece at source position {from_pos}.")
            return False

        if self.get_piece_color(piece) != self.turn:
            logger.warning(f"It's {self.turn}'s turn, but tried to move {piece} ({self.get_piece_color(piece)}) from {from_pos}.")
            return False

        target_piece = self.board[to_pos]
        if self.get_piece_color(target_piece) == self.turn:
            logger.warning(f"Invalid move: Cannot capture your own piece ({target_piece}) at {to_pos}.")
            return False

        if not self.is_legal_move(piece, from_pos, to_pos):
            logger.warning(f"Illegal move attempted: {piece} ({self.get_piece_color(piece)}) from {from_pos} to {to_pos}.")
            return False

        if target_piece != '.':
            logger.info(f"{self.turn.capitalize()} {self._piece_name(piece)} ({piece}) captures {self.get_piece_color(target_piece)} {self._piece_name(target_piece)} ({target_piece}) on {to_pos}.")

        self.board[to_pos] = piece
        self.board[from_pos] = '.'

        self.check_game_over()

        if not self.game_over:
            self.turn = 'black' if self.turn == 'white' else 'white'
            logger.debug(f"Turn switched to {self.turn}.")
        return True

    def is_legal_move(self, piece: Piece, from_pos: Position, to_pos: Position) -> bool:
        """
        Determine whether a move is legal for the specified piece.

        Args:
            piece (Piece): Piece to move.
            from_pos (Position): Starting square.
            to_pos (Position): Destination square.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
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
        """
        Check whether a pawn move is legal.

        Args:
            piece (Piece): The pawn.
            from_pos (Position): Start square.
            to_pos (Position): Target square.
            df (int): File delta.
            dr (int): Rank delta.

        Returns:
            bool: True if pawn move is legal, else False.
        """
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
        """
        Check whether all squares between two positions are empty (for sliding pieces).

        Args:
            from_pos (Position): Start square.
            to_pos (Position): End square.

        Returns:
            bool: True if path is clear, else False.
        """
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
        """
        Remove the first occurrence of a piece with the given symbol from the board.
        Used in test - not in game.

        Args:
            symbol (str): Character representing the piece to remove.
        """
        for pos, piece in self.board.items():
            if piece == symbol:
                self.board[pos] = '.'
                logger.debug(f"Removed piece {symbol} from {pos}.")
                break
