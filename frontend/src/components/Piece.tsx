import React from 'react';

const unicodePieces: Record<string, { white: string; black: string }> = {
  K: { white: '♔', black: '♚' },
  Q: { white: '♕', black: '♛' },
  R: { white: '♖', black: '♜' },
  B: { white: '♗', black: '♝' },
  N: { white: '♘', black: '♞' },
  P: { white: '♙', black: '♟' },
};

interface PieceProps {
  type: 'K' | 'Q' | 'R' | 'B' | 'N' | 'P';
  color: 'white' | 'black';
}

const Piece: React.FC<PieceProps> = ({ type, color }) => {
  return (
    <span style={{ color: color === 'white' ? '#fff' : '#222', textShadow: color === 'white' ? '0 0 2px #000' : '0 0 2px #fff' }}>
      {unicodePieces[type][color]}
    </span>
  );
};

export default Piece; 