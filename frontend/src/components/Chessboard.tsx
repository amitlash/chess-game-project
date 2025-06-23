import React from 'react';
import Piece from './Piece';

const initialBoard = [
  ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
  ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
  [null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null],
  [null, null, null, null, null, null, null, null],
  ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
  ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
];

const Chessboard: React.FC = () => {
  return (
    <div
      style={{
        display: 'grid',
        gridTemplateRows: 'repeat(8, 1fr)',
        gridTemplateColumns: 'repeat(8, 1fr)',
        width: 400,
        height: 400,
        border: '2px solid #333',
      }}
    >
      {initialBoard.map((row, rowIdx) =>
        row.map((piece, colIdx) => {
          const isLight = (rowIdx + colIdx) % 2 === 1;
          return (
            <div
              key={`${rowIdx}-${colIdx}`}
              style={{
                background: isLight ? '#f0d9b5' : '#b58863',
                width: '100%',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 32,
              }}
            >
              {piece ? (
                <Piece type={piece[1]} color={piece[0] === 'w' ? 'white' : 'black'} />
              ) : null}
            </div>
          );
        })
      )}
    </div>
  );
};

export default Chessboard; 