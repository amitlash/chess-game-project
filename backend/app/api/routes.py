import logging
from typing import Dict, List

from app.core.ai_service import AIService
from app.core.exceptions import (
    AIServiceError,
    GameOverError,
    InvalidMoveError,
    ValidationError,
)
from app.core.game_engine import ChessGame
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)
game = ChessGame()
ai_service = AIService(use_multi_move_cache=True, cache_size=5)

"""
API routes for the chess backend.

- /board: GET current board state
- /move: POST a move (expects JSON body: {"from_pos": ..., "to_pos": ...})
- /reset: POST to reset the game
- /chat: POST chat message with AI assistant
- /ai-move: POST to get AI move suggestion
- /analyze: GET position analysis from AI
- /game-mode: POST to set game mode (human vs human, human vs ai)
"""


@router.get("/")
def read_root():
    return {"message": "Welcome to the Chess API with AI integration!"}


class MoveRequest(BaseModel):
    from_pos: str
    to_pos: str


class ChatRequest(BaseModel):
    message: str
    message_history: List[Dict[str, str]] = []


class GameModeRequest(BaseModel):
    mode: str  # "human_vs_human" or "human_vs_ai"
    ai_color: str = "black"  # "white" or "black"


class AIMoveRequest(BaseModel):
    board: Dict[str, str]
    turn: str
    move_history: List[Dict] = []


class AIStrategyRequest(BaseModel):
    use_multi_move_cache: bool = True
    cache_size: int = 5


@router.get("/board")
def get_board():
    """
    Retrieve the current game state including the board layout,
    current turn, whether the game is over, and move history.

    Returns:
        dict: Dictionary containing 'board', 'turn', 'game_over', and 'move_history' keys.
    """
    logger.debug("Fetching current board state.")
    return {
        "board": game.board,
        "turn": game.turn,
        "game_over": game.game_over,
        "move_history": game.move_history,
    }


@router.post("/move")
def make_move(move: MoveRequest):
    """
    Attempt to make a move from one position to another.

    Args:
        move (MoveRequest): The move request containing from_pos and to_pos.

    Returns:
        dict: Result of the move attempt including success status,
              updated board, current turn, game_over flag, and move history.

    Raises:
        GameOverError: If the game is already over.
        InvalidMoveError: If the move is invalid.
        InvalidPositionError: If the positions are invalid.
    """
    logger.info(f"Move request: {move.from_pos} to {move.to_pos} by {game.turn}.")
    success = game.make_move(move.from_pos, move.to_pos)
    logger.debug(f"Move success: {success}")
    return {
        "success": success,
        "board": game.board,
        "game_over": game.game_over,
        "turn": game.turn,
        "move_history": game.move_history,
    }


@router.post("/reset")
def reset_game():
    """
    Reset the chess game to its initial state.

    Returns:
        dict: Confirmation message that the game has been reset, including empty move history.
    """
    global game
    game.reset()
    logger.info("Game has been reset to initial state.")
    return {"message": "Game reset", "move_history": game.move_history}


@router.post("/chat")
def chat_with_ai(chat_request: ChatRequest):
    """
    Chat with the AI assistant about chess.

    Args:
        chat_request (ChatRequest): The chat request containing message and history.

    Returns:
        dict: AI assistant response and updated message history.

    Raises:
        AIServiceError: If there's an error with the AI service.
    """
    logger.info(f"Chat request received: {chat_request.message[:50]}...")

    # Use board-aware chat method with current game state
    ai_response = ai_service.chat_with_assistant(
        chat_request.message_history,
        chat_request.message,
        board=game.board,
        turn=game.turn,
    )

    # Update message history
    updated_history = chat_request.message_history + [
        {"role": "user", "content": chat_request.message},
        {"role": "assistant", "content": ai_response},
    ]

    logger.debug("Chat response generated successfully")
    return {"response": ai_response, "message_history": updated_history}


@router.post("/ai-move")
def get_ai_move(ai_request: AIMoveRequest):
    """
    Get an AI move suggestion for the current position.

    Args:
        ai_request (AIMoveRequest): The request containing board state and turn.

    Returns:
        dict: AI move suggestion or error message.

    Raises:
        AIServiceError: If there's an error with the AI service.
    """
    logger.info("AI move request received")

    ai_move = ai_service.generate_ai_move(
        ai_request.board,
        ai_request.turn,
        ai_request.move_history,
        game,  # Pass the game engine instance
    )

    if ai_move:
        from_pos, to_pos = ai_move
        logger.info(f"AI suggested move: {from_pos} to {to_pos}")
        return {
            "success": True,
            "from_pos": from_pos,
            "to_pos": to_pos,
            "move": f"{from_pos} {to_pos}",
        }
    else:
        logger.warning("No AI move available")
        return {"success": False, "message": "No legal moves available for AI"}


@router.get("/analyze")
def analyze_position():
    """
    Get AI analysis of the current board position.

    Returns:
        dict: AI analysis of the current position.

    Raises:
        AIServiceError: If there's an error with the AI service.
    """
    logger.info("Position analysis request received")

    analysis = ai_service.analyze_position(game.board, game.turn)

    logger.debug("Position analysis generated successfully")
    return {"analysis": analysis, "board": game.board, "turn": game.turn}


@router.post("/game-mode")
def set_game_mode(mode_request: GameModeRequest):
    """
    Set the game mode (human vs human or human vs ai).

    Args:
        mode_request (GameModeRequest): The game mode configuration.

    Returns:
        dict: Confirmation of game mode setting.

    Raises:
        ValidationError: If the game mode or AI color is invalid.
    """
    valid_modes = ["human_vs_human", "human_vs_ai"]
    valid_colors = ["white", "black"]

    if mode_request.mode not in valid_modes:
        raise ValidationError(
            "mode", mode_request.mode, f"Must be one of: {valid_modes}"
        )

    if mode_request.ai_color not in valid_colors:
        raise ValidationError(
            "ai_color", mode_request.ai_color, f"Must be one of: {valid_colors}"
        )

    # Store game mode in a simple way (in production, use proper state management)
    game.game_mode = mode_request.mode
    game.ai_color = mode_request.ai_color

    logger.info(
        f"Game mode set to: {mode_request.mode}, AI color: {mode_request.ai_color}"
    )

    return {
        "message": "Game mode updated successfully",
        "mode": mode_request.mode,
        "ai_color": mode_request.ai_color,
    }


@router.post("/ai-play")
def ai_play_move():
    """
    Make an AI move in the current game.
    This endpoint automatically makes the AI's move if it's the AI's turn.

    Returns:
        dict: Result of the AI move including updated game state.

    Raises:
        ValidationError: If AI mode is not enabled or it's not AI's turn.
        GameOverError: If the game is over.
        AIServiceError: If the AI cannot generate a valid move.
        InvalidMoveError: If the AI move is invalid.
    """
    # Check if it's AI's turn
    if not hasattr(game, "game_mode") or game.game_mode != "human_vs_ai":
        raise ValidationError(
            "game_mode",
            game.game_mode if hasattr(game, "game_mode") else None,
            "AI mode not enabled. Set game mode to 'human_vs_ai' first.",
        )

    if not hasattr(game, "ai_color"):
        game.ai_color = "black"  # Default AI color

    if game.turn != game.ai_color:
        raise ValidationError(
            "turn",
            game.turn,
            f"It's not AI's turn. Current turn: {game.turn}, AI color: {game.ai_color}",
        )

    # Generate AI move
    ai_move = ai_service.generate_ai_move(
        game.board,
        game.turn,
        game.move_history,
        game,  # Pass the game engine instance
    )

    if not ai_move:
        raise AIServiceError("AI could not generate a valid move.")

    # Make the AI move
    from_pos, to_pos = ai_move
    success = game.make_move(from_pos, to_pos)

    logger.info(f"AI made move: {from_pos} to {to_pos}, success: {success}")

    return {
        "success": success,
        "ai_move": {"from_pos": from_pos, "to_pos": to_pos},
        "board": game.board,
        "game_over": game.game_over,
        "turn": game.turn,
        "move_history": game.move_history,
    }


@router.post("/ai-strategy")
def set_ai_strategy(strategy_request: AIStrategyRequest):
    """
    Set the AI strategy (multi-move caching vs single-move full analysis).

    Args:
        strategy_request (AIStrategyRequest): The AI strategy configuration.

    Returns:
        dict: Confirmation of AI strategy setting.
    """
    # Update AI service strategy
    ai_service.set_strategy(
        use_multi_move_cache=strategy_request.use_multi_move_cache,
        cache_size=strategy_request.cache_size,
    )

    strategy_name = (
        "multi-move caching"
        if strategy_request.use_multi_move_cache
        else "single-move full analysis"
    )

    logger.info(
        f"AI strategy set to: {strategy_name}, cache size: {strategy_request.cache_size}"
    )

    return {
        "message": "AI strategy updated successfully",
        "strategy": strategy_name,
        "use_multi_move_cache": strategy_request.use_multi_move_cache,
        "cache_size": strategy_request.cache_size,
    }


@router.get("/ai-config")
def get_ai_config():
    """
    Get the current AI configuration.

    Returns:
        dict: Current AI strategy and configuration.
    """
    strategy_name = (
        "multi-move caching"
        if ai_service.use_multi_move_cache
        else "single-move full analysis"
    )

    return {
        "strategy": strategy_name,
        "use_multi_move_cache": ai_service.use_multi_move_cache,
        "cache_size": ai_service.cache_size,
        "cached_moves_count": len(ai_service.move_queue),
    }
