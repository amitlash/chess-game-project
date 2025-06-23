import React from 'react';

interface PieceProps {
  type: 'K' | 'Q' | 'R' | 'B' | 'N' | 'P';
  color: 'white' | 'black';
}

const pieceToFile = {
  K: { white: 'wK.svg', black: 'bK.svg' },
  Q: { white: 'wQ.svg', black: 'bQ.svg' },
  R: { white: 'wR.svg', black: 'bR.svg' },
  B: { white: 'wB.svg', black: 'bB.svg' },
  N: { white: 'wN.svg', black: 'bN.svg' },
  P: { white: 'wP.svg', black: 'bP.svg' },
};

const Piece: React.FC<PieceProps> = ({ type, color }) => {
  const fileName = pieceToFile[type][color];
  const src = new URL(`../assets/pieces/${fileName}`, import.meta.url).href;
  return <img src={src} alt={`${color} ${type}`} style={{ width: 40, height: 40 }} draggable={false} />;
};

export default Piece; 