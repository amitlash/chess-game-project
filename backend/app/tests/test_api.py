# This test file supports both unittest and pytest.
# The sys.path workaround ensures 'main' is importable when running from backend/app.
from fastapi.testclient import TestClient
from app.main import app
from app.api.routes import game # Import the game instance
import pytest

client = TestClient(app)

def test_board_initial():
    response = client.get("/board")
    assert response.status_code == 200
    data = response.json()
    assert "board" in data
    assert "turn" in data
    assert "game_over" in data
    assert "move_history" in data
    assert data["move_history"] == []


def test_move():
    client.post("/reset")
    response = client.post("/move", json={"from_pos": "e2", "to_pos": "e4"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "move_history" in data
    assert len(data["move_history"]) == 1
    assert data["move_history"][0]["from_pos"] == "e2"
    assert data["move_history"][0]["to_pos"] == "e4"
    assert data["move_history"][0]["piece"] == "P"
    assert data["move_history"][0]["color"] == "white"


def test_reset():
    # First make a move to have some history
    client.post("/move", json={"from_pos": "e2", "to_pos": "e4"})
    
    response = client.post("/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Game reset"
    assert "move_history" in data
    assert data["move_history"] == []

def test_move_after_game_over_fails():
    """Test that making a move after the game is over returns a 409 Conflict."""
    # Reset to ensure clean state
    client.post("/reset")
    
    # Remove the white king to end the game
    from app.api.routes import game
    game.remove_piece('K')  # Remove white king to end game
    game.check_game_over()  # Explicitly check game over condition
    
    # Verify game is over
    assert game.game_over == True
    
    # Try to make another move
    response = client.post("/move", json={"from_pos": "e2", "to_pos": "e4"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Game is over. No more moves allowed."