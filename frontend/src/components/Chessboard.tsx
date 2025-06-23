import React, { useEffect } from 'react';
import Piece from './Piece';
import { useChessStore } from '../store';

const Chessboard: React.FC = () => {
  const board = useChessStore((state) => state.board);
  const selectedSquare = useChessStore((state) => state.selectedSquare);
  const selectSquare = useChessStore((state) => state.selectSquare);
  const sendMove = useChessStore((state) => state.sendMove);
  const fetchBoard = useChessStore((state) => state.fetchBoard);
  const loading = useChessStore((state) => state.loading);
  const error = useChessStore((state) => state.error);

  useEffect(() => {
    fetchBoard();
    // eslint-disable-next-line
  }, []);

  async function handleSquareClick(rowIdx: number, colIdx: number) {
    if (loading) return;
    if (selectedSquare) {
      if (selectedSquare[0] === rowIdx && selectedSquare[1] === colIdx) {
        selectSquare(null); // Deselect if clicking the same square
      } else {
        await sendMove(selectedSquare, [rowIdx, colIdx]);
        selectSquare(null);
      }
    } else if (board[rowIdx][colIdx]) {
      selectSquare([rowIdx, colIdx]);
    }
  }

  return (
    <div>
      {loading && <div style={{ color: 'orange', marginBottom: 8 }}>Loading...</div>}
      {error && <div style={{ color: 'red', marginBottom: 8 }}>{error}</div>}
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
                  cursor: loading ? 'not-allowed' : 'pointer',
                  boxSizing: 'border-box',
                  border: isSelected ? '2px solid #f90' : undefined,
                  opacity: loading ? 0.5 : 1,
                }}
              >
                {piece ? <Piece type={piece.type} color={piece.color} /> : null}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default Chessboard; 