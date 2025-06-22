from typing import Dict, Tuple
import sys


# Define types for clarity
Position = str  # e.g. 'e4'
Piece = str     # e.g. 'P' for white pawn, 'p' for black pawn, 'K' for white king, etc.

class ChessGame:
    def __init__(self):
        self.board: Dict[Position, Piece] = self._initial_board()
        self.turn = 'white'  # 'white' or 'black'
        self.game_over = False
    
    def _piece_name(self, symbol: str) -> str:
        names = {
            'p': 'pawn', 'r': 'rook', 'n': 'knight',
            'b': 'bishop', 'q': 'queen', 'k': 'king'
        }
        return names.get(symbol.lower(), 'piece')


    def _initial_board(self) -> Dict[Position, Piece]:
        # Setup pieces with uppercase for White, lowercase for Black
        pieces = {
            'a1': 'R', 'b1': 'N', 'c1': 'B', 'd1': 'Q', 'e1': 'K', 'f1': 'B', 'g1': 'N', 'h1': 'R',
            'a2': 'P', 'b2': 'P', 'c2': 'P', 'd2': 'P', 'e2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P',
            'a7': 'p', 'b7': 'p', 'c7': 'p', 'd7': 'p', 'e7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p',
            'a8': 'r', 'b8': 'n', 'c8': 'b', 'd8': 'q', 'e8': 'k', 'f8': 'b', 'g8': 'n', 'h8': 'r',
        }
        # Fill empty squares with None or empty string
        board = {}
        files = 'abcdefgh'
        ranks = '12345678'
        for r in ranks:
            for f in files:
                pos = f + r
                board[pos] = pieces.get(pos, '.')
        return board

    def print_board(self):
        print("\n  +------------------------+")
        for rank in reversed('12345678'):
            row = [self.board[f + rank] for f in 'abcdefgh']
            print(f"{rank} | {' '.join(row)} |")
        print("  +------------------------+")
        print("    a b c d e f g h\n")

    def is_white_piece(self, piece: Piece) -> bool:
        return piece.isupper() and piece != '.'

    def is_black_piece(self, piece: Piece) -> bool:
        return piece.islower() and piece != '.'

    def is_valid_pos(self, pos: Position) -> bool:
        return len(pos) == 2 and pos[0] in 'abcdefgh' and pos[1] in '12345678'

    def get_piece_color(self, piece: Piece) -> str:
        if piece == '.':
            return 'none'
        return 'white' if piece.isupper() else 'black'

    def check_game_over(self):
        # Check for presence of kings
        pieces = self.board.values()
        has_white_king = 'K' in pieces
        has_black_king = 'k' in pieces

        if not has_white_king:
            print("Black wins! White's king is missing.")
            self.game_over = True
        elif not has_black_king:
            print("White wins! Black's king is missing.")
            self.game_over = True

    def make_move(self, from_pos: Position, to_pos: Position) -> bool:
        # Basic validation: positions valid
        if not (self.is_valid_pos(from_pos) and self.is_valid_pos(to_pos)):
            print("Invalid board position.")
            return False
        piece = self.board[from_pos]
        if piece == '.':
            print("No piece at source.")
            return False
        if self.get_piece_color(piece) != self.turn:
            print(f"It's {self.turn}'s turn.")
            return False
        target_piece = self.board[to_pos]
        if self.get_piece_color(target_piece) == self.turn:
            print("Cannot capture your own piece.")
            return False

        # Validate the move according to piece type
        if not self.is_legal_move(piece, from_pos, to_pos):
            print("Illegal move for piece.")
            return False

        # Capture announcement
        if target_piece != '.':
            color = 'white' if target_piece.isupper() else 'black'
            piece_name = self._piece_name(target_piece)
            print(f"{self.turn.capitalize()} captures {color} {piece_name} on {to_pos}!")

        # Execute move
        self.board[to_pos] = piece
        self.board[from_pos] = '.'

        self.check_game_over()
        if not self.game_over:
            # Switch turn
            self.turn = 'black' if self.turn == 'white' else 'white'
        return True


    def is_legal_move(self, piece: Piece, from_pos: Position, to_pos: Position) -> bool:
        # Define movement rules for each piece type (no castling, no en passant, no promotion)
        file_from, rank_from = from_pos
        file_to, rank_to = to_pos
        df = ord(file_to) - ord(file_from)
        dr = int(rank_to) - int(rank_from)

        # Pawn moves
        if piece.upper() == 'P':
            return self._legal_pawn_move(piece, from_pos, to_pos, df, dr)

        # Knight moves
        if piece.upper() == 'N':
            return (abs(df), abs(dr)) in [(1, 2), (2, 1)]

        # Bishop moves
        if piece.upper() == 'B':
            if abs(df) == abs(dr):
                return self._is_path_clear(from_pos, to_pos)
            return False

        # Rook moves
        if piece.upper() == 'R':
            if df == 0 or dr == 0:
                return self._is_path_clear(from_pos, to_pos)
            return False

        # Queen moves
        if piece.upper() == 'Q':
            if abs(df) == abs(dr) or df == 0 or dr == 0:
                return self._is_path_clear(from_pos, to_pos)
            return False

        # King moves
        if piece.upper() == 'K':
            return max(abs(df), abs(dr)) == 1

        return False

    def _legal_pawn_move(self, piece: Piece, from_pos: Position, to_pos: Position, df: int, dr: int) -> bool:
        direction = 1 if piece.isupper() else -1  # White moves up, black down
        start_rank = '2' if piece.isupper() else '7'
        target_piece = self.board[to_pos]

        # Normal move forward
        if df == 0:
            if dr == direction and target_piece == '.':
                return True
            # Double move from start
            if (from_pos[1] == start_rank and dr == 2 * direction):
                intermediate_pos = from_pos[0] + str(int(from_pos[1]) + direction)
                if self.board[intermediate_pos] == '.' and target_piece == '.':
                    return True
        # Capture
        if abs(df) == 1 and dr == direction and target_piece != '.' and self.get_piece_color(target_piece) != self.get_piece_color(piece):
            return True
        return False

    def _is_path_clear(self, from_pos: Position, to_pos: Position) -> bool:
        # Checks if path is clear between from_pos and to_pos for sliding pieces
        file_from, rank_from = from_pos
        file_to, rank_to = to_pos
        df = ord(file_to) - ord(file_from)
        dr = int(rank_to) - int(rank_from)

        step_file = (df > 0) - (df < 0)
        step_rank = (dr > 0) - (dr < 0)

        current_file = ord(file_from) + step_file
        current_rank = int(rank_from) + step_rank

        while (current_file != ord(file_to)) or (current_rank != int(rank_to)):
            pos = chr(current_file) + str(current_rank)
            if self.board[pos] != '.':
                return False
            current_file += step_file
            current_rank += step_rank
        return True
    
    def remove_piece(self, symbol: str):
        for pos, piece in self.board.items():
            if piece == symbol:
                self.board[pos] = '.'
                break


    def run(self):
        print("Welcome to Simple Chess!")
        while not self.game_over:
            self.print_board()
            print(f"{self.turn.capitalize()}'s move (e.g. e2 e4): ", end='')
            move = input().strip().lower().split()
            if move == ['exit'] or move == ['quit']:
                print("Game ended.")
                break
            if len(move) != 2:
                print("Invalid input. Enter source and destination like: e2 e4")
                continue
            from_pos, to_pos = move
            self.make_move(from_pos, to_pos)

        print("Final board:")
        self.print_board()
        print("Game over.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import unittest
        unittest.main(module="test_chess", argv=sys.argv[:1])  # avoid passing test as test name
    else:
        game = ChessGame()
        game.run()
