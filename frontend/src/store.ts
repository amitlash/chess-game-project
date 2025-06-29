import { create } from 'zustand';
import * as api from './services/api';

export type PieceType = 'K' | 'Q' | 'R' | 'B' | 'N' | 'P';
export type PieceColor = 'white' | 'black';
export type Piece = { type: PieceType; color: PieceColor } | null;
export type Board = Piece[][];

// Move record type matching backend
export interface MoveRecord {
  from_pos: string;
  to_pos: string;
  piece: string;
  color: PieceColor;
  captured_piece?: string | null;
  is_capture: boolean;
  algebraic_notation: string;
  turn_number: number;
}

function getInitialBoard(): Board {
  return [
    [
      { type: 'R', color: 'black' },
      { type: 'N', color: 'black' },
      { type: 'B', color: 'black' },
      { type: 'Q', color: 'black' },
      { type: 'K', color: 'black' },
      { type: 'B', color: 'black' },
      { type: 'N', color: 'black' },
      { type: 'R', color: 'black' },
    ],
    Array.from({ length: 8 }, () => ({ type: 'P', color: 'black' })),
    ...Array.from({ length: 4 }, () => Array.from({ length: 8 }, () => null)),
    Array.from({ length: 8 }, () => ({ type: 'P', color: 'white' })),
    [
      { type: 'R', color: 'white' },
      { type: 'N', color: 'white' },
      { type: 'B', color: 'white' },
      { type: 'Q', color: 'white' },
      { type: 'K', color: 'white' },
      { type: 'B', color: 'white' },
      { type: 'N', color: 'white' },
      { type: 'R', color: 'white' },
    ],
  ];
}

function backendBoardToFrontend(board: Record<string, string>): Board {
  const files = 'abcdefgh';
  const ranks = '87654321';
  return ranks.split('').map((rank) =>
    files.split('').map((file) => {
      const code = board[file + rank];
      if (!code || code === '.') return null;
      const color = code === code.toUpperCase() ? 'white' : 'black';
      const type = code.toUpperCase() as PieceType;
      return { type, color };
    }),
  );
}

export interface ChessState {
  board: Board;
  moveHistory: MoveRecord[];
  turn: PieceColor;
  gameOver: boolean;
  selectedSquare: [number, number] | null;
  loading: boolean;
  error: string | null;
  fetchBoard: () => Promise<void>;
  sendMove: (from: [number, number], to: [number, number]) => Promise<void>;
  sendReset: () => Promise<void>;
  selectSquare: (square: [number, number] | null) => void;
  movePiece: () => void;
  reset: () => void;
}

export const useChessStore = create<ChessState>((set, get) => ({
  board: getInitialBoard(),
  moveHistory: [],
  turn: 'white',
  gameOver: false,
  selectedSquare: null,
  loading: false,
  error: null,
  fetchBoard: async () => {
    set({ loading: true, error: null });
    try {
      const data = await api.getBoard();
      set({
        board: backendBoardToFrontend(data.board),
        turn: data.turn === 'white' ? 'white' : 'black',
        gameOver: data.game_over,
        moveHistory: data.move_history || [],
        loading: false,
        error: null,
      });
    } catch (e: unknown) {
      const errorMessage = e instanceof Error ? e.message : 'Failed to fetch board';
      set({ loading: false, error: errorMessage });
    }
  },
  sendMove: async (from, to) => {
    if (get().gameOver) {
      console.warn('Attempted to move after game over.');
      return;
    }
    set({ loading: true, error: null });
    try {
      const files = 'abcdefgh';
      const ranks = '87654321';
      const from_pos = files[from[1]] + ranks[from[0]];
      const to_pos = files[to[1]] + ranks[to[0]];
      const data = await api.makeMove(from_pos, to_pos);
      set({
        board: backendBoardToFrontend(data.board),
        turn: data.turn === 'white' ? 'white' : 'black',
        gameOver: data.game_over,
        moveHistory: data.move_history || [],
        loading: false,
        error: null,
      });
    } catch (e: unknown) {
      const errorMessage = e instanceof Error ? e.message : 'Failed to make move';
      set({ loading: false, error: errorMessage });
    }
  },
  sendReset: async () => {
    set({ loading: true, error: null });
    try {
      const data = await api.resetGame();
      set({ moveHistory: data.move_history || [] });
      await get().fetchBoard();
    } catch (e: unknown) {
      const errorMessage = e instanceof Error ? e.message : 'Failed to reset game';
      set({ loading: false, error: errorMessage });
    }
  },
  selectSquare: (square) => set({ selectedSquare: square }),
  movePiece: () => {
    // This will be replaced by sendMove in the UI
  },
  reset: () =>
    set({
      board: getInitialBoard(),
      moveHistory: [],
      turn: 'white',
      selectedSquare: null,
      gameOver: false,
    }),
}));
