# test_chess.py
import unittest
from groq_testing.chess_game.backend.core.chessboard import ChessGame

class TestChessGame(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()

    def test_initial_board_contains_kings(self):
        pieces = self.game.board.values()
        self.assertIn('K', pieces)
        self.assertIn('k', pieces)

    def test_valid_pawn_move(self):
        result = self.game.make_move('e2', 'e4')
        self.assertTrue(result)
        self.assertEqual(self.game.board['e4'], 'P')
        self.assertEqual(self.game.board['e2'], '.')

    def test_invalid_move_from_empty_square(self):
        result = self.game.make_move('e3', 'e4')
        self.assertFalse(result)

    def test_cannot_capture_own_piece(self):
        result = self.game.make_move('e1', 'd1')  # King into Queen
        self.assertFalse(result)

    def test_turn_enforcement(self):
        self.game.make_move('e2', 'e4')  # White moves
        result = self.game.make_move('d2', 'd4')  # White tries again
        self.assertFalse(result)

    def test_capture_announced_and_successful(self):
        # Setup custom board where white pawn can capture black pawn
        self.game.board = {k: '.' for k in self.game.board}
        self.game.board['e4'] = 'P'
        self.game.board['d5'] = 'p'
        self.game.turn = 'white'
        result = self.game.make_move('e4', 'd5')
        self.assertTrue(result)
        self.assertEqual(self.game.board['d5'], 'P')
        self.assertEqual(self.game.board['e4'], '.')

    def test_game_over_when_king_missing(self):
        self.game.remove_piece('k') # Delete black king
        self.game.check_game_over()
        self.assertTrue(self.game.game_over)

    def test_blocked_bishop_cannot_move(self):
        # Standard position: f1 bishop blocked by e2 pawn
        result = self.game.make_move('f1', 'c4')
        self.assertFalse(result)

    def test_knight_can_jump_over_pieces(self):
        # g1 knight jumping to f3 in starting position
        result = self.game.make_move('g1', 'f3')
        self.assertTrue(result)
        self.assertEqual(self.game.board['f3'], 'N')
        self.assertEqual(self.game.board['g1'], '.')

    def test_rook_cannot_jump_over_pieces(self):
        # Rook at a1 is blocked by pawn at a2
        result = self.game.make_move('a1', 'a4')
        self.assertFalse(result)

    def test_pawn_double_move_blocked(self):
        # Block e2 pawn with a piece on e3, then try to double move to e4
        self.game.board['e3'] = 'x'  # simulate obstacle
        result = self.game.make_move('e2', 'e4')
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
