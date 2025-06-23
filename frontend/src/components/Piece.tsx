import React from 'react';

const unicodePieces: Record<string, { white: string; black: string }> = {
  K: { white: '\u2654', black: '\u265A' },
  Q: { white: '\u2655', black: '\u265B' },
  R: { white: '\u2656', black: '\u265C' },
  B: { white: '\u2657', black: '\u265D' },
  N: { white: '\u2658', black: '\u265E' },
  P: { white: '\u2659', black: '\u265F' },
};

interface PieceProps {
  type: 'K' | 'Q' | 'R' | 'B' | 'N' | 'P';
  color: 'white' | 'black';
}

const Piece: React.FC<PieceProps> = ({ type, color }) => {
  return <span>{String.fromCharCode(parseInt(unicodePieces[type][color].replace('\\u', ''), 16))}</span>;
};

export default Piece; 