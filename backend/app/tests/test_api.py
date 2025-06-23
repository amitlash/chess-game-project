# This test file supports both unittest and pytest.
# The sys.path workaround ensures 'main' is importable when running from backend/app.
from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_board_initial():
    response = client.get("/board")
    assert response.status_code == 200
    data = response.json()
    assert "board" in data and isinstance(data["board"], dict)
    assert data["turn"] == "white"


def test_move():
    client.post("/reset")
    response = client.post("/move", json={"from_pos": "e2", "to_pos": "e4"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["board"]["e4"] == "P"
    assert data["board"]["e2"] == "."


def test_reset():
    response = client.post("/reset")
    assert response.status_code == 200
    assert response.json()["message"] == "Game reset"