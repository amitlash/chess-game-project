from fastapi import APIRouter
from app.core.chessboard import ChessGame

router = APIRouter()
game = ChessGame()

@router.get("/board")
def get_board():
    return {"board": game.board, "turn": game.turn, "game_over": game.game_over}

@router.post("/move")
def make_move(from_pos: str, to_pos: str):
    success = game.make_move(from_pos, to_pos)
    return {"success": success, "board": game.board, "game_over": game.game_over, "turn": game.turn}

@router.post("/reset")
def reset_game():
    global game
    game = ChessGame()
    return {"message": "Game reset"}