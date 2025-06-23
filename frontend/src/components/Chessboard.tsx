import React from 'react';
import Piece from './Piece';
import { useChessStore } from '../store';

const Chessboard: React.FC = () => {
  const board = useChessStore((state) => state.board);
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
      {board.map((row, rowIdx) =>
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
              {piece ? <Piece type={piece.type} color={piece.color} /> : null}
            </div>
          );
        })
      )}
    </div>
  );
};

export default Chessboard; 