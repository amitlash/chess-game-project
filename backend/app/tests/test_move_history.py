import pytest
from app.core.game_engine import ChessGame


class TestMoveHistory:
    """Test cases for move history tracking functionality."""

    def test_new_game_has_empty_move_history(self):
        """Test that a new game starts with an empty move history."""
        game = ChessGame()
        assert game.move_history == []

    def test_make_move_adds_to_history(self):
        """Test that making a move adds it to the move history."""
        game = ChessGame()
        game.make_move("e2", "e4")
        assert len(game.move_history) == 1
        assert game.move_history[0]["from_pos"] == "e2"
        assert game.move_history[0]["to_pos"] == "e4"
        assert game.move_history[0]["piece"] == "P"
        assert game.move_history[0]["color"] == "white"

    def test_multiple_moves_accumulate_in_history(self):
        """Test that multiple moves are properly accumulated in history."""
        game = ChessGame()
        game.make_move("e2", "e4")  # White pawn
        game.make_move("e7", "e5")  # Black pawn
        game.make_move("g1", "f3")  # White knight

        assert len(game.move_history) == 3
        assert game.move_history[0]["color"] == "white"
        assert game.move_history[1]["color"] == "black"
        assert game.move_history[2]["color"] == "white"

    def test_move_history_includes_capture_information(self):
        """Test that move history includes capture information."""
        game = ChessGame()
        # Set up a capture scenario
        game.board["e4"] = "P"  # White pawn
        game.board["d5"] = "p"  # Black pawn
        game.turn = "white"

        game.make_move("e4", "d5")  # White captures black pawn

        assert len(game.move_history) == 1
        assert game.move_history[0]["captured_piece"] == "p"
        assert game.move_history[0]["is_capture"] == True

    def test_move_history_includes_algebraic_notation(self):
        """Test that move history includes algebraic notation."""
        game = ChessGame()
        game.make_move("e2", "e4")

        assert len(game.move_history) == 1
        assert "algebraic_notation" in game.move_history[0]
        assert game.move_history[0]["algebraic_notation"] == "e4"

    def test_reset_game_clears_move_history(self):
        """Test that resetting the game clears the move history."""
        game = ChessGame()
        game.make_move("e2", "e4")
        game.make_move("e7", "e5")

        assert len(game.move_history) == 2

        game.reset()
        assert game.move_history == []

    def test_move_history_preserves_game_state(self):
        """Test that move history doesn't interfere with game state."""
        game = ChessGame()
        game.make_move("e2", "e4")
        game.make_move("e7", "e5")

        # Verify game state is still correct
        assert game.board["e4"] == "P"
        assert game.board["e5"] == "p"
        assert game.turn == "white"
        assert not game.game_over

    def test_invalid_moves_not_added_to_history(self):
        """Test that invalid moves are not added to move history."""
        game = ChessGame()
        initial_history_length = len(game.move_history)

        # Try to make an invalid move
        success = game.make_move("e2", "e9")  # Invalid position

        assert not success
        assert len(game.move_history) == initial_history_length

    def test_move_history_includes_turn_number(self):
        """Test that move history includes turn number information."""
        game = ChessGame()
        game.make_move("e2", "e4")  # Turn 1, White
        game.make_move("e7", "e5")  # Turn 1, Black
        game.make_move("g1", "f3")  # Turn 2, White

        assert game.move_history[0]["turn_number"] == 1
        assert game.move_history[1]["turn_number"] == 1
        assert game.move_history[2]["turn_number"] == 2
