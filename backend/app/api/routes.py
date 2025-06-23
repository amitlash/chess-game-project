import logging
from fastapi import APIRouter
from core.game_engine import ChessGame
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)
game = ChessGame()

"""
API routes for the chess backend.

- /board: GET current board state
- /move: POST a move (expects JSON body: {"from_pos": ..., "to_pos": ...})
- /reset: POST to reset the game
"""

class MoveRequest(BaseModel):
    from_pos: str
    to_pos: str

@router.get("/board")
def get_board():
    """
    Retrieve the current game state including the board layout,
    current turn, and whether the game is over.

    Returns:
        dict: Dictionary containing 'board', 'turn', and 'game_over' keys.
    """
    logger.debug("Fetching current board state.")
    return {
        "board": game.board,
        "turn": game.turn,
        "game_over": game.game_over
    }

@router.post("/move")
def make_move(move: MoveRequest):
    """
    Attempt to make a move from one position to another.

    Args:
        move (MoveRequest): The move request containing from_pos and to_pos.

    Returns:
        dict: Result of the move attempt including success status,
              updated board, current turn, and game_over flag.
    """
    logger.info(f"Move request: {move.from_pos} to {move.to_pos} by {game.turn}.")
    success = game.make_move(move.from_pos, move.to_pos)
    logger.debug(f"Move success: {success}")
    return {
        "success": success,
        "board": game.board,
        "game_over": game.game_over,
        "turn": game.turn
    }

@router.post("/reset")
def reset_game():
    """
    Reset the chess game to its initial state.

    Returns:
        dict: Confirmation message that the game has been reset.
    """
    global game
    game = ChessGame()
    logger.info("Game has been reset to initial state.")
    return {"message": "Game reset"}
