import { create } from 'zustand';

export type PieceType = 'K' | 'Q' | 'R' | 'B' | 'N' | 'P';
export type PieceColor = 'white' | 'black';
export type Piece = { type: PieceType; color: PieceColor } | null;
export type Board = Piece[][];

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

export interface ChessState {
  board: Board;
  moveHistory: string[];
  turn: PieceColor;
  makeMove: (from: [number, number], to: [number, number]) => void;
  reset: () => void;
}

export const useChessStore = create<ChessState>((set, get) => ({
  board: getInitialBoard(),
  moveHistory: [],
  turn: 'white',
  makeMove: (from, to) => {
    // Placeholder: just add a move to history for now
    set((state) => ({
      moveHistory: [
        ...state.moveHistory,
        `(${from[0]},${from[1]}) → (${to[0]},${to[1]})`,
      ],
      turn: state.turn === 'white' ? 'black' : 'white',
    }));
  },
  reset: () => set({ board: getInitialBoard(), moveHistory: [], turn: 'white' }),
})); 