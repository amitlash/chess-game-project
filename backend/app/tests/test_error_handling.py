"""
Tests for error handling functionality.

This module tests the custom exception classes, error middleware,
and standardized error responses.
"""

import pytest
from app.core.exceptions import (
    AIServiceError,
    ChessGameError,
    GameOverError,
    InvalidMoveError,
    InvalidPositionError,
    ValidationError,
)
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestCustomExceptions:
    """Test custom exception classes."""

    def test_chess_game_error_base(self):
        """Test the base ChessGameError class."""
        error = ChessGameError("Test error", "TEST_ERROR", {"key": "value"}, 400)

        assert error.message == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.details == {"key": "value"}
        assert error.status_code == 400

        error_dict = error.to_dict()
        assert error_dict["error"] is True
        assert error_dict["message"] == "Test error"
        assert error_dict["error_code"] == "TEST_ERROR"
        assert error_dict["details"] == {"key": "value"}
        assert error_dict["status_code"] == 400

    def test_game_over_error(self):
        """Test GameOverError."""
        error = GameOverError()
        assert error.message == "Game is over. No more moves allowed."
        assert error.error_code == "GAME_OVER"
        assert error.status_code == 409

    def test_invalid_move_error(self):
        """Test InvalidMoveError."""
        error = InvalidMoveError("Invalid move", "e2", "e4", {"reason": "test"})
        assert error.message == "Invalid move"
        assert error.error_code == "INVALID_MOVE"
        assert error.status_code == 400
        assert error.details["from_pos"] == "e2"
        assert error.details["to_pos"] == "e4"
        assert error.details["reason"] == "test"

    def test_invalid_position_error(self):
        """Test InvalidPositionError."""
        error = InvalidPositionError("z9", {"reason": "test"})
        assert error.message == "Invalid position: z9"
        assert error.error_code == "INVALID_POSITION"
        assert error.status_code == 400
        assert error.details["position"] == "z9"
        assert error.details["reason"] == "test"

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("field", "value", "reason", {"extra": "data"})
        assert error.message == "Validation error for field: reason"
        assert error.error_code == "VALIDATION_ERROR"
        assert error.status_code == 400
        assert error.details["field"] == "field"
        assert error.details["value"] == "value"
        assert error.details["reason"] == "reason"
        assert error.details["extra"] == "data"


class TestErrorHandlingEndpoints:
    """Test error handling in API endpoints."""

    def test_invalid_move_endpoint(self):
        """Test that invalid moves return proper error responses."""
        # Reset the game first
        client.post("/reset")

        # Try to move from an empty square
        response = client.post("/move", json={"from_pos": "e3", "to_pos": "e4"})

        assert response.status_code == 400
        data = response.json()
        assert data["error"] is True
        assert data["error_code"] == "INVALID_MOVE"
        assert "No piece at source position" in data["message"]
        assert data["details"]["from_pos"] == "e3"
        assert data["details"]["to_pos"] == "e4"

    def test_invalid_position_endpoint(self):
        """Test that invalid positions return proper error responses."""
        # Reset the game first
        client.post("/reset")

        # Try to move from an invalid position
        response = client.post("/move", json={"from_pos": "z9", "to_pos": "e4"})

        assert response.status_code == 400
        data = response.json()
        assert data["error"] is True
        assert data["error_code"] == "INVALID_POSITION"
        assert "Invalid position: z9" in data["message"]
        assert data["details"]["position"] == "z9"

    def test_wrong_turn_endpoint(self):
        """Test that moving on wrong turn returns proper error responses."""
        # Reset the game first
        client.post("/reset")

        # Make a valid move first (white moves)
        client.post("/move", json={"from_pos": "e2", "to_pos": "e4"})

        # Try to move white again (should be black's turn now)
        response = client.post("/move", json={"from_pos": "d2", "to_pos": "d4"})

        assert response.status_code == 400
        data = response.json()
        assert data["error"] is True
        assert data["error_code"] == "INVALID_MOVE"
        assert "Wrong player's turn" in data["details"]["reason"]

    def test_validation_error_endpoint(self):
        """Test that validation errors return proper error responses."""
        # Try to set invalid game mode
        response = client.post(
            "/game-mode", json={"mode": "invalid_mode", "ai_color": "white"}
        )

        assert response.status_code == 400
        data = response.json()
        assert data["error"] is True
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "Validation error for mode" in data["message"]
        assert data["details"]["field"] == "mode"
        assert data["details"]["value"] == "invalid_mode"

    def test_ai_mode_validation(self):
        """Test AI mode validation errors."""
        # Try to make AI move without setting AI mode
        response = client.post("/ai-play")

        assert response.status_code == 400
        data = response.json()
        assert data["error"] is True
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "AI mode not enabled" in data["details"]["reason"]


class TestErrorMiddleware:
    """Test error middleware functionality."""

    def test_404_error_handling(self):
        """Test that 404 errors are handled properly."""
        response = client.get("/nonexistent-endpoint")

        assert response.status_code == 404
        data = response.json()
        assert data["error"] is True
        assert data["error_code"] == "HTTP_404"

    def test_validation_error_handling(self):
        """Test that Pydantic validation errors are handled properly."""
        # Send invalid JSON
        response = client.post("/move", json={"invalid": "data"})

        assert response.status_code == 422
        data = response.json()
        assert data["error"] is True
        assert data["error_code"] == "VALIDATION_ERROR"
        assert "validation_errors" in data["details"]

    def test_error_response_headers(self):
        """Test that error responses include proper headers."""
        response = client.post("/move", json={"from_pos": "e3", "to_pos": "e4"})

        assert response.status_code == 400
        assert "x-error-handled" in response.headers
        assert "x-request-id" in response.headers


class TestGameStateValidation:
    """Test game state validation with custom exceptions."""

    def test_game_over_after_checkmate(self):
        """Test that game over state is properly handled."""
        # This would require setting up a checkmate position
        # For now, we'll test the basic game over functionality

        # Reset the game
        client.post("/reset")

        # Make some moves to get to a position where we can test game over
        # This is a simplified test - in a real scenario, you'd set up a checkmate

        # For now, let's just verify that the game state is properly managed
        response = client.get("/board")
        assert response.status_code == 200
        data = response.json()
        assert data["game_over"] is False


if __name__ == "__main__":
    pytest.main([__file__])
