import React, { useEffect, useState } from 'react';
import Piece from './Piece';
import { useChessStore } from '../store';

const Chessboard: React.FC = () => {
  const board = useChessStore((state) => state.board);
  const selectedSquare = useChessStore((state) => state.selectedSquare);
  const selectSquare = useChessStore((state) => state.selectSquare);
  const sendMove = useChessStore((state) => state.sendMove);
  const fetchBoard = useChessStore((state) => state.fetchBoard);
  const loading = useChessStore((state) => state.loading);
  const gameOver = useChessStore((state) => state.gameOver);
  const turn = useChessStore((state) => state.turn);

  // Add delayed loading state for opacity
  const [delayedLoading, setDelayedLoading] = useState(false);
  useEffect(() => {
    let timeout: ReturnType<typeof setTimeout> | null = null;
    if (loading) {
      timeout = setTimeout(() => setDelayedLoading(true), 400);
    } else {
      setDelayedLoading(false);
    }
    return () => {
      if (timeout) clearTimeout(timeout);
    };
  }, [loading]);

  useEffect(() => {
    fetchBoard();
    // eslint-disable-next-line
  }, []);

  async function handleSquareClick(rowIdx: number, colIdx: number) {
    if (loading || gameOver) return;
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
    <div style={{ position: 'relative' }}>
      {gameOver && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.5)',
            color: 'white',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 10,
            fontSize: '2rem',
            fontWeight: 'bold',
          }}
        >
          <div>Game Over</div>
          <div style={{ fontSize: '1.2rem', marginTop: '0.5rem' }}>
            {turn === 'white' ? 'Black' : 'White'} wins!
          </div>
        </div>
      )}
      <div
        style={{
          display: 'grid',
          gridTemplateRows: 'repeat(8, 1fr)',
          gridTemplateColumns: 'repeat(8, 1fr)',
          width: 400,
          height: 400,
          border: '2px solid #333',
          opacity: gameOver ? 0.6 : delayedLoading ? 0.5 : 1,
        }}
      >
        {board.map((row, rowIdx) =>
          row.map((piece, colIdx) => {
            const isLight = (rowIdx + colIdx) % 2 === 1;
            const isSelected =
              selectedSquare && selectedSquare[0] === rowIdx && selectedSquare[1] === colIdx;
            return (
              <div
                key={`${rowIdx}-${colIdx}`}
                onClick={() => handleSquareClick(rowIdx, colIdx)}
                style={{
                  background: isSelected ? '#ff0' : isLight ? '#f0d9b5' : '#b58863',
                  width: '100%',
                  height: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 32,
                  cursor: loading || gameOver ? 'not-allowed' : 'pointer',
                  boxSizing: 'border-box',
                  border: isSelected ? '2px solid #f90' : undefined,
                  opacity: delayedLoading ? 0.5 : 1,
                }}
              >
                {piece ? <Piece type={piece.type} color={piece.color} /> : null}
              </div>
            );
          }),
        )}
      </div>
    </div>
  );
};

export default Chessboard;
