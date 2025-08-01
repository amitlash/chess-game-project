import unittest

from app.core.exceptions import GameOverError, InvalidMoveError, InvalidPositionError
from app.core.game_engine import ChessGame


class TestChessGame(unittest.TestCase):
    """Unit tests for the ChessGame logic engine."""

    def setUp(self):
        """Initialize a new ChessGame instance before each test."""
        self.game = ChessGame()

    def test_board_has_kings_initially(self):
        """Test that the initial board contains both kings."""
        pieces = self.game.board.values()
        self.assertIn("K", pieces)
        self.assertIn("k", pieces)

    def test_white_pawn_valid_move(self):
        """Test that a valid white pawn move is executed correctly."""
        self.assertTrue(self.game.make_move("e2", "e4"))
        self.assertEqual(self.game.board["e4"], "P")
        self.assertEqual(self.game.board["e2"], ".")

    def test_move_from_empty_square_fails(self):
        """Test that moving a piece from an empty square fails."""
        with self.assertRaises(InvalidMoveError) as context:
            self.game.make_move("e3", "e4")
        self.assertIn("No piece at source position", str(context.exception))

    def test_cannot_capture_own_piece(self):
        """Test that a piece cannot capture another piece of the same color."""
        with self.assertRaises(InvalidMoveError) as context:
            self.game.make_move("e1", "d1")  # King to queen
        self.assertIn("Cannot capture your own piece", str(context.exception))

    def test_turn_enforced_properly(self):
        """Test that players cannot move twice in a row."""
        self.game.make_move("e2", "e4")  # White
        with self.assertRaises(InvalidMoveError) as context:
            self.game.make_move("d2", "d4")  # White again
        self.assertIn("It's black's turn", str(context.exception))

    def test_capture_and_update_successful(self):
        """Test that capturing an enemy piece works and updates the board."""
        self.game.board = {pos: "." for pos in self.game.board}
        self.game.board["e4"] = "P"
        self.game.board["d5"] = "p"
        self.game.turn = "white"
        self.assertTrue(self.game.make_move("e4", "d5"))
        self.assertEqual(self.game.board["d5"], "P")

    def test_game_ends_if_king_removed(self):
        """Test that the game ends if a king is removed from the board."""
        self.game.remove_piece("k")
        self.game.check_game_over()
        self.assertTrue(self.game.game_over)

    def test_bishop_cannot_jump(self):
        """Test that a bishop cannot jump over other pieces."""
        with self.assertRaises(InvalidMoveError) as context:
            self.game.make_move("f1", "c4")
        self.assertIn("Illegal move", str(context.exception))

    def test_knight_can_jump(self):
        """Test that a knight can jump over other pieces."""
        self.assertTrue(self.game.make_move("g1", "f3"))
        self.assertEqual(self.game.board["f3"], "N")

    def test_rook_cannot_jump_over_pieces(self):
        """Test that a rook cannot move through other pieces."""
        with self.assertRaises(InvalidMoveError) as context:
            self.game.make_move("a1", "a4")
        self.assertIn("Illegal move", str(context.exception))

    def test_pawn_blocked_from_double_move(self):
        """Test that a pawn cannot double move if blocked on the path."""
        self.game.board["e3"] = "x"
        with self.assertRaises(InvalidMoveError) as context:
            self.game.make_move("e2", "e4")
        self.assertIn("Illegal move", str(context.exception))

    def test_cannot_move_after_game_over(self):
        """Test that no more moves can be made once the game is over."""
        # Set up a scenario where white can capture the black king
        self.game.board = {pos: "." for pos in self.game.board}
        self.game.board["e8"] = "k"  # Black King
        self.game.board["e1"] = "K"  # White King
        self.game.board["d8"] = "Q"  # White Queen
        self.game.turn = "white"

        # White captures the black king, ending the game
        self.assertTrue(self.game.make_move("d8", "e8"))
        self.assertTrue(self.game.game_over)

        # Attempt another move with white (the winning color)
        self.game.board["a1"] = "R"  # Add a rook to move
        with self.assertRaises(GameOverError) as context:
            self.game.make_move("a1", "a2")
        self.assertIn("Game is over", str(context.exception))


if __name__ == "__main__":
    unittest.main()
