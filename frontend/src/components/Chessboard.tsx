import React from 'react';
import Piece from './Piece';
import { useChessStore } from '../store';

const Chessboard: React.FC = () => {
  const board = useChessStore((state) => state.board);
  const selectedSquare = useChessStore((state) => state.selectedSquare);
  const selectSquare = useChessStore((state) => state.selectSquare);
  const movePiece = useChessStore((state) => state.movePiece);

  function handleSquareClick(rowIdx: number, colIdx: number) {
    if (selectedSquare) {
      if (selectedSquare[0] === rowIdx && selectedSquare[1] === colIdx) {
        selectSquare(null); // Deselect if clicking the same square
      } else {
        movePiece([rowIdx, colIdx]);
      }
    } else if (board[rowIdx][colIdx]) {
      selectSquare([rowIdx, colIdx]);
    }
  }

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
          const isSelected = selectedSquare && selectedSquare[0] === rowIdx && selectedSquare[1] === colIdx;
          return (
            <div
              key={`${rowIdx}-${colIdx}`}
              onClick={() => handleSquareClick(rowIdx, colIdx)}
              style={{
                background: isSelected
                  ? '#ff0'
                  : isLight
                  ? '#f0d9b5'
                  : '#b58863',
                width: '100%',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 32,
                cursor: 'pointer',
                boxSizing: 'border-box',
                border: isSelected ? '2px solid #f90' : undefined,
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