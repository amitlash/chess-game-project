import logging
import os
import time
from typing import Dict, List, Optional, Tuple

from dotenv import find_dotenv, load_dotenv
from groq import Groq

logger = logging.getLogger(__name__)

# Load environment variables
_ = load_dotenv(find_dotenv())
api_key = os.environ.get("GROQ_API_KEY")


class AIService:
    """
    AI service for chess game integration.
    Handles both conversational AI and chess move generation.
    """

    def __init__(self, use_multi_move_cache: bool = True, cache_size: int = 5):
        """
        Initialize the AI service with Groq client.

        Args:
            use_multi_move_cache: Whether to use multi-move caching strategy
            cache_size: Number of moves to generate ahead when using caching
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            logger.warning("GROQ_API_KEY not found in environment variables")

        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests
        self.move_queue: List[Tuple[str, str]] = []  # Simple queue for planned moves
        self.use_multi_move_cache = use_multi_move_cache
        self.cache_size = cache_size

        logger.info(
            f"AIService initialized - Multi-move cache: {use_multi_move_cache}, Cache size: {cache_size}"
        )

    def set_strategy(self, use_multi_move_cache: bool, cache_size: int = 5):
        """
        Set the AI strategy and cache size.

        Args:
            use_multi_move_cache: Whether to use multi-move caching strategy
            cache_size: Number of moves to generate ahead when using caching
        """
        self.use_multi_move_cache = use_multi_move_cache
        self.cache_size = cache_size
        self.move_queue = []  # Clear queue when changing strategy
        logger.info(
            f"AI strategy changed - Multi-move cache: {use_multi_move_cache}, Cache size: {cache_size}"
        )

    def _rate_limit(self):
        """Ensure minimum time between API requests to prevent rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def _get_completion(
        self, messages: List[Dict[str, str]], stream: bool = False
    ) -> str:
        """
        Get completion from Groq API.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            stream: Whether to stream the response

        Returns:
            The AI response as a string
        """
        if not self.client:
            return (
                "AI service is not available. Please check your API key configuration."
            )

        try:
            # Apply rate limiting
            self._rate_limit()

            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=stream,
                stop=None,
            )

            if stream:
                message = []
                for chunk in response:
                    text_chunk = chunk.choices[0].delta.content or ""
                    message.append(text_chunk)
                return "".join(message)
            else:
                return response.choices[0].message.content or ""

        except Exception as e:
            logger.error(f"Error getting AI completion: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    def chat_with_assistant(
        self,
        message_history: List[Dict[str, str]],
        user_message: str,
        board: Optional[Dict[str, str]] = None,
        turn: Optional[str] = None,
    ) -> str:
        """
        Chat with the AI assistant. If board is provided, use a robust prompt to ground the conversation in the actual board state.

        Args:
            message_history: Previous conversation history
            user_message: New user message
            board: (Optional) Current board state
            turn: (Optional) Current player's turn

        Returns:
            AI assistant response
        """
        if board is not None:
            # Build a list of all pieces and their positions
            piece_names = {
                "K": "King",
                "Q": "Queen",
                "R": "Rook",
                "B": "Bishop",
                "N": "Knight",
                "P": "Pawn",
                "k": "King",
                "q": "Queen",
                "r": "Rook",
                "b": "Bishop",
                "n": "Knight",
                "p": "Pawn",
            }
            piece_list = []
            for pos, piece in board.items():
                if piece != ".":
                    color = "White" if piece.isupper() else "Black"
                    piece_name = piece_names[piece]
                    piece_list.append(f"{color} {piece_name} on {pos}")
            piece_listing = "\n".join(piece_list)

            system_prompt = {
                "role": "system",
                "content": """You are a chess expert assistant. You will be given a chess board state and a mapping of all pieces and their positions.\n\nYour job is to:\n1. List all pieces and their positions for both White and Black, exactly as given.\n2. When answering questions or providing advice, refer ONLY to the pieces and pawns that are actually present on the board.\n3. Do NOT mention or analyze any piece, pawn, or square that does not exist in the given board state.\n4. If a square is empty, do not mention it.\n5. If a piece is in an unusual or illegal position, mention this fact.\n\nBe precise and do not hallucinate. Your responses must be based strictly on the provided board state.""",
            }

            board_context = f"""Current turn: {turn if turn else '?'}\n\nPieces on the board:\n{piece_listing}\n"""

            messages = (
                [system_prompt]
                + message_history
                + [{"role": "user", "content": board_context + user_message}]
            )
        else:
            system_prompt = {
                "role": "system",
                "content": """You are a helpful chess assistant. You can:\n- Answer questions about chess rules and strategies\n- Help analyze chess positions\n- Provide tips and advice for improving chess skills\n- Engage in friendly conversation about chess\n- Explain chess concepts in an accessible way\n\nBe friendly, knowledgeable, and encouraging. Keep responses concise but informative.""",
            }
            messages = (
                [system_prompt]
                + message_history
                + [{"role": "user", "content": user_message}]
            )
        return self._get_completion(messages)

    def _board_to_fen(self, board: Dict[str, str]) -> str:
        """
        Convert board state to FEN notation for AI analysis.

        Args:
            board: Dictionary mapping positions to pieces

        Returns:
            FEN string representation of the board
        """
        fen_parts = []

        # Convert board to FEN piece placement
        for rank in "87654321":
            rank_str = ""
            empty_count = 0

            for file in "abcdefgh":
                pos = file + rank
                piece = board.get(pos, ".")

                if piece == ".":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        rank_str += str(empty_count)
                        empty_count = 0
                    rank_str += piece

            if empty_count > 0:
                rank_str += str(empty_count)

            fen_parts.append(rank_str)

        return "/".join(fen_parts)

    def _get_legal_moves(
        self, board: Dict[str, str], turn: str, game_engine
    ) -> List[Tuple[str, str]]:
        """
        Get all legal moves for the current position using the game engine's validation.

        Args:
            board: Current board state
            turn: Current player's turn ('white' or 'black')
            game_engine: The ChessGame instance for validation

        Returns:
            List of legal moves as (from_pos, to_pos) tuples
        """
        legal_moves = []

        for from_pos, piece in board.items():
            if piece == ".":
                continue

            # Check if piece belongs to current player
            is_white_piece = piece.isupper()
            if (turn == "white" and not is_white_piece) or (
                turn == "black" and is_white_piece
            ):
                continue

            # Check all possible destination squares
            for to_pos in board.keys():
                if from_pos == to_pos:
                    continue

                # Use the game engine's validation
                if game_engine.is_legal_move(piece, from_pos, to_pos):
                    legal_moves.append((from_pos, to_pos))

        return legal_moves

    def generate_single_move_full_analysis(
        self,
        board: Dict[str, str],
        turn: str,
        move_history: List[Dict],
        game_engine=None,
    ) -> Optional[Tuple[str, str]]:
        """
        Generate a single AI move using full board analysis (no move restrictions).

        Args:
            board: Current board state
            turn: Current player's turn
            move_history: History of previous moves
            game_engine: The ChessGame instance for validation

        Returns:
            Tuple of (from_pos, to_pos) for the AI move, or None if no move possible
        """
        if not self.client:
            logger.warning("AI client not available for move generation")
            return None

        try:
            # Convert board to FEN for AI analysis
            fen = self._board_to_fen(board)

            # Create prompt for full board analysis
            system_prompt = {
                "role": "system",
                "content": """You are a chess AI assistant. Analyze the EXACT current position and suggest the best legal move.

                CRITICAL RULES:
                - You MUST analyze the actual current board position provided in FEN notation
                - Only suggest moves that are legal for the current position
                - Do NOT suggest moves that are impossible (e.g., moving pawns that have already moved)
                - Consider the actual piece positions, not generic opening theory
                - Analyze the full board position to determine the best strategic move
                - Respond with ONLY a move in the format "from_pos to_pos" (e.g., "e7 e5")
                - Do not include any explanations or additional text - just the move coordinates

                RESPONSE FORMAT: Respond with exactly "from_pos to_pos" (e.g., "e7 e5")
                """,
            }

            analysis_prompt = f"""CURRENT BOARD POSITION (FEN): {fen}
            CURRENT TURN: {turn}
            MOVES PLAYED: {len(move_history)}

            IMPORTANT: Analyze this EXACT position. Do not suggest generic opening moves.
            Look at what pieces are actually on the board and where they can legally move.

            Please suggest the best legal move for this specific position:"""

            messages = [system_prompt, {"role": "user", "content": analysis_prompt}]

            logger.info(f"AI full analysis prompt - FEN: {fen}, Turn: {turn}")

            response = self._get_completion(messages, stream=False)

            logger.info(f"AI full analysis raw response: '{response}'")

            # Parse the response to extract move coordinates
            from_pos, to_pos = self._parse_move_response(response)

            if from_pos and to_pos:
                logger.info(f"AI full analysis parsed move: {from_pos} to {to_pos}")

                # Validate that the suggested move is legal
                legal_moves = self._get_legal_moves(board, turn, game_engine)
                if (from_pos, to_pos) in legal_moves:
                    logger.info(
                        f"AI full analysis suggested valid move: {from_pos} to {to_pos}"
                    )
                    return (from_pos, to_pos)
                else:
                    logger.warning(
                        f"AI full analysis suggested illegal move: {from_pos} to {to_pos}"
                    )
                    logger.warning(f"Legal moves were: {legal_moves}")

                    # Try to find a similar legal move or fallback
                    for legal_move in legal_moves:
                        if legal_move[0] == from_pos or legal_move[1] == to_pos:
                            logger.info(
                                f"Found similar legal move: {legal_move[0]} to {legal_move[1]}"
                            )
                            return legal_move
            else:
                logger.warning(
                    f"AI full analysis response format invalid: '{response}'"
                )

            # Fallback: choose first legal move
            legal_moves = self._get_legal_moves(board, turn, game_engine)
            if legal_moves:
                logger.info("Using fallback move selection for full analysis")
                fallback_move = legal_moves[0]
                logger.info(f"Fallback move: {fallback_move[0]} to {fallback_move[1]}")
                return fallback_move

            logger.info("No legal moves available for AI")
            return None

        except Exception as e:
            logger.error(f"Error generating AI move with full analysis: {e}")
            return None

    def generate_multiple_moves_ahead(
        self,
        board: Dict[str, str],
        turn: str,
        move_history: List[Dict],
        game_engine=None,
        num_moves: int = 5,
    ) -> List[Tuple[str, str]]:
        """
        Generate multiple moves ahead to reduce API calls and improve strategy.

        Args:
            board: Current board state
            turn: Current player's turn
            move_history: History of previous moves
            game_engine: The ChessGame instance for validation
            num_moves: Number of moves to generate ahead

        Returns:
            List of (from_pos, to_pos) tuples for the next moves
        """
        if not self.client:
            logger.warning("AI client not available for move generation")
            return []

        try:
            # Convert board to FEN for AI analysis
            fen = self._board_to_fen(board)

            # Create prompt for multiple move generation
            system_prompt = {
                "role": "system",
                "content": f"""You are a chess AI assistant. Analyze the EXACT current position and predict the best {num_moves} moves you would make over the next {num_moves} turns, assuming your opponent makes reasonable responses.

                CRITICAL RULES:
                - You MUST analyze the actual current board position provided in FEN notation
                - You are predicting a SEQUENCE of moves over multiple turns, not alternative moves for the same position
                - Consider that after each of your moves, your opponent will respond, changing the board
                - Each move should be the best move for the position that will exist after the previous moves
                - Consider the actual piece positions, not generic opening theory
                - Respond with exactly {num_moves} moves in the format "move1, move2, move3, move4, move5"
                - Each move should be in the format "from_pos to_pos" (e.g., "e7 e5")
                - Do not include explanations - just the moves separated by commas

                RESPONSE FORMAT: "e7 e5, d7 d6, g8 f6, b8 c6, f8 e7"
                """,
            }

            analysis_prompt = f"""CURRENT BOARD POSITION (FEN): {fen}
            CURRENT TURN: {turn}
            MOVES PLAYED: {len(move_history)}

            IMPORTANT: Analyze this EXACT position and predict your next {num_moves} moves.
            Consider how the board will change after each move and your opponent's likely responses.

            Please predict the best {num_moves} moves you would make over the next {num_moves} turns:"""

            messages = [system_prompt, {"role": "user", "content": analysis_prompt}]

            logger.info(
                f"AI multi-move prompt - FEN: {fen}, Turn: {turn}, Requesting {num_moves} sequential moves"
            )

            response = self._get_completion(messages, stream=False)

            logger.info(f"AI multi-move raw response: '{response}'")

            # Parse the response to extract multiple moves
            moves = []
            response = response.strip()

            # Split by comma and parse each move
            move_strings = [move.strip() for move in response.split(",")]

            for move_str in move_strings:
                # Parse individual move using existing logic
                from_pos, to_pos = self._parse_move_response(move_str)
                if from_pos and to_pos:
                    moves.append((from_pos, to_pos))
                    logger.info(f"Parsed sequential move: {from_pos} to {to_pos}")
                else:
                    logger.warning(f"Could not parse move: '{move_str}'")

            # Validate moves against legal moves
            legal_moves = self._get_legal_moves(board, turn, game_engine)
            valid_moves = []

            for move in moves:
                if move in legal_moves:
                    valid_moves.append(move)
                    logger.info(f"Valid sequential move: {move[0]} to {move[1]}")
                else:
                    logger.warning(f"Invalid sequential move: {move[0]} to {move[1]}")

            # Update the move queue with the valid moves
            self.move_queue = valid_moves
            logger.info(
                f"Generated {len(valid_moves)} valid sequential moves out of {len(moves)} suggested (move_queue updated)"
            )
            return valid_moves

        except Exception as e:
            logger.error(f"Error generating multiple moves: {e}")
            return []

    def _parse_move_response(
        self, response: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse a single move response in various formats.

        Args:
            response: Move string in various formats

        Returns:
            Tuple of (from_pos, to_pos) or (None, None) if parsing fails
        """
        response = response.strip()

        # Try different formats: "e7 e5", "e7-e5", "e7e5", "Nb8 c6", "Ng8-f6"
        from_pos = None
        to_pos = None

        # Format 1: "e7 e5" or "Nb8 c6" (space separated)
        if " " in response:
            parts = response.split()
            if len(parts) >= 2:
                # Handle piece notation: "Nb8 c6" -> "b8 c6"
                from_part = parts[0]
                to_part = parts[1]

                # Remove piece letters (K, Q, R, B, N) from the beginning
                if len(from_part) >= 3 and from_part[0] in ["K", "Q", "R", "B", "N"]:
                    from_pos = from_part[1:]
                else:
                    from_pos = from_part

                if len(to_part) >= 3 and to_part[0] in ["K", "Q", "R", "B", "N"]:
                    to_pos = to_part[1:]
                else:
                    to_pos = to_part

        # Format 2: "e7-e5" or "Nb8-c6" (dash separated)
        elif "-" in response:
            parts = response.split("-")
            if len(parts) >= 2:
                from_part = parts[0]
                to_part = parts[1]

                # Remove piece letters (K, Q, R, B, N) from the beginning
                if len(from_part) >= 3 and from_part[0] in ["K", "Q", "R", "B", "N"]:
                    from_pos = from_part[1:]
                else:
                    from_pos = from_part

                if len(to_part) >= 3 and to_part[0] in ["K", "Q", "R", "B", "N"]:
                    to_pos = to_part[1:]
                else:
                    to_pos = to_part

        # Format 3: "e7e5" or "Nb8c6" (no separator, assume 2+2 characters)
        elif len(response) >= 4:
            # Handle piece notation: "Nb8c6" -> "b8c6"
            if response[0] in ["K", "Q", "R", "B", "N"]:
                # Skip the piece letter
                from_pos = response[1:3]
                to_pos = response[3:5]
            else:
                from_pos = response[:2]
                to_pos = response[2:4]

        return from_pos, to_pos

    def generate_ai_move(
        self,
        board: Dict[str, str],
        turn: str,
        move_history: List[Dict],
        game_engine=None,
    ) -> Optional[Tuple[str, str]]:
        """
        Generate an AI move based on current board state using the configured strategy.

        Args:
            board: Current board state
            turn: Current player's turn
            move_history: History of previous moves
            game_engine: The ChessGame instance for validation

        Returns:
            Tuple of (from_pos, to_pos) for the AI move, or None if no move possible
        """
        if not self.client:
            logger.warning("AI client not available for move generation")
            return None

        try:
            if self.use_multi_move_cache:
                logger.info("Using multi-move caching strategy (queue)")
                cached_move = self.get_cached_move(board, turn, game_engine)
                if cached_move:
                    logger.info(
                        f"Returning cached move: {cached_move[0]} to {cached_move[1]}"
                    )
                    return cached_move
                logger.info(
                    "No cached moves available or all were illegal, generating new moves"
                )
                moves = self.generate_multiple_moves_ahead(
                    board, turn, move_history, game_engine, num_moves=self.cache_size
                )
                logger.info(
                    f"Generated {len(moves)} new moves, queue now has {len(self.move_queue)} moves"
                )
                if moves:
                    logger.info(
                        f"Returning first generated move: {moves[0][0]} to {moves[0][1]}"
                    )
                    return moves[0]
            else:
                logger.info("Using single-move full analysis strategy")
                return self.generate_single_move_full_analysis(
                    board, turn, move_history, game_engine
                )

            # Fallback: get legal moves and choose first one
            legal_moves = self._get_legal_moves(board, turn, game_engine)
            if legal_moves:
                logger.info("Using fallback move selection")
                fallback_move = legal_moves[0]
                logger.info(f"Fallback move: {fallback_move[0]} to {fallback_move[1]}")
                return fallback_move

            logger.info("No legal moves available for AI")
            return None

        except Exception as e:
            logger.error(f"Error generating AI move: {e}")
            return None

    def analyze_position(self, board: Dict[str, str], turn: str) -> str:
        """
        Analyze the current chess position and provide insights.

        Args:
            board: Current board state
            turn: Current player's turn

        Returns:
            AI analysis of the position
        """
        fen = self._board_to_fen(board)

        # Build a list of all pieces and their positions
        piece_names = {
            "K": "King",
            "Q": "Queen",
            "R": "Rook",
            "B": "Bishop",
            "N": "Knight",
            "P": "Pawn",
            "k": "King",
            "q": "Queen",
            "r": "Rook",
            "b": "Bishop",
            "n": "Knight",
            "p": "Pawn",
        }
        piece_list = []
        for pos, piece in board.items():
            if piece != ".":
                color = "White" if piece.isupper() else "Black"
                piece_name = piece_names[piece]
                piece_list.append(f"{color} {piece_name} on {pos}")
        piece_listing = "\n".join(piece_list)

        system_prompt = {
            "role": "system",
            "content": """You are a chess expert. You will be given a chess board state in FEN notation and a mapping of all pieces and their positions.\n\nYour job is to:\n1. List all pieces and their positions for both White and Black, exactly as given.\n2. Provide a brief, insightful analysis of the position, referring ONLY to the pieces and pawns that are actually present on the board.\n3. Do NOT mention or analyze any piece, pawn, or square that does not exist in the given board state.\n4. If a square is empty, do not mention it.\n5. If a piece is in an unusual or illegal position, mention this fact.\n\nBe precise and do not hallucinate. Your analysis must be based strictly on the provided board state.""",
        }

        analysis_prompt = f"""FEN: {fen}\nCurrent turn: {turn}\n\nPieces on the board:\n{piece_listing}\n\nPlease analyze this position as described above."""

        messages = [system_prompt, {"role": "user", "content": analysis_prompt}]

        return self._get_completion(messages, stream=False)

    def get_cached_move(
        self, board: Dict[str, str], turn: str, game_engine=None
    ) -> Optional[Tuple[str, str]]:
        """
        Get a move from the queue if available and legal.
        """
        logger.info(f"Checking move queue. Queue length: {len(self.move_queue)}")
        if self.move_queue:
            # Validate the next move is still legal
            legal_moves = self._get_legal_moves(board, turn, game_engine)
            logger.info(f"Legal moves available: {len(legal_moves)}")
            logger.info(f"Move queue contents: {self.move_queue}")

            while self.move_queue:
                move = self.move_queue.pop(0)
                from_pos, to_pos = move
                logger.info(f"Checking cached move: {from_pos} to {to_pos}")

                # Strong validation: Check if the move makes sense for current board
                if from_pos in board and to_pos in board:
                    from_piece = board[from_pos]
                    to_piece = board[to_pos]

                    # Check if we're trying to capture our own piece
                    if to_piece != ".":
                        is_white_piece = to_piece.isupper()
                        if (turn == "white" and is_white_piece) or (
                            turn == "black" and not is_white_piece
                        ):
                            logger.warning(
                                f"Discarded cached move (would capture own piece): {from_pos} to {to_pos} ({from_piece} capturing {to_piece})"
                            )
                            continue

                    # Check if the piece at from_pos belongs to current player
                    if from_piece != ".":
                        is_white_piece = from_piece.isupper()
                        if (turn == "white" and not is_white_piece) or (
                            turn == "black" and is_white_piece
                        ):
                            logger.warning(
                                f"Discarded cached move (wrong piece color): {from_pos} to {to_pos} ({from_piece} is not {turn}'s piece)"
                            )
                            continue

                # Final check: Is it in the legal moves list
                if move in legal_moves:
                    logger.info(f"Using cached move from queue: {from_pos} to {to_pos}")
                    return move
                else:
                    logger.info(
                        f"Discarded cached move (no longer legal): {from_pos} to {to_pos}"
                    )
        else:
            logger.info("Move queue is empty")
        return None
