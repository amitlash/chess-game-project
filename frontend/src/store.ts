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
  selectedSquare: [number, number] | null;
  selectSquare: (square: [number, number] | null) => void;
  movePiece: (to: [number, number]) => void;
  reset: () => void;
}

export const useChessStore = create<ChessState>((set, get) => ({
  board: getInitialBoard(),
  moveHistory: [],
  turn: 'white',
  selectedSquare: null,
  selectSquare: (square) => set({ selectedSquare: square }),
  movePiece: (to) => {
    const { selectedSquare, board, turn, moveHistory } = get();
    if (!selectedSquare) return;
    const [fromRow, fromCol] = selectedSquare;
    const [toRow, toCol] = to;
    const piece = board[fromRow][fromCol];
    if (!piece || piece.color !== turn) return;
    // For now, allow any move (no validation)
    const newBoard = board.map((row) => row.slice());
    newBoard[toRow][toCol] = piece;
    newBoard[fromRow][fromCol] = null;
    set({
      board: newBoard,
      moveHistory: [
        ...moveHistory,
        `${piece.color} ${piece.type}: (${fromRow},${fromCol}) → (${toRow},${toCol})`,
      ],
      turn: turn === 'white' ? 'black' : 'white',
      selectedSquare: null,
    });
  },
  reset: () => set({ board: getInitialBoard(), moveHistory: [], turn: 'white', selectedSquare: null }),
})); 