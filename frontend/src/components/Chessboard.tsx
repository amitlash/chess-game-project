import React, { useEffect, useState } from 'react';
import Piece from './Piece';
import { useChessStore } from '../store';
import { aiPlayMove } from '../services/api';

interface ChessboardProps {
  gameMode?: string;
  aiColor?: string;
}

const Chessboard: React.FC<ChessboardProps> = ({
  gameMode = 'human_vs_human',
  aiColor = 'black',
}) => {
  const board = useChessStore((state) => state.board);
  const selectedSquare = useChessStore((state) => state.selectedSquare);
  const selectSquare = useChessStore((state) => state.selectSquare);
  const sendMove = useChessStore((state) => state.sendMove);
  const fetchBoard = useChessStore((state) => state.fetchBoard);
  const loading = useChessStore((state) => state.loading);
  const gameOver = useChessStore((state) => state.gameOver);
  const turn = useChessStore((state) => state.turn);

  // AI mode state
  const [isAITurn, setIsAITurn] = useState(false);
  const [lastAIMoveTime, setLastAIMoveTime] = useState(0);

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

  // Check for AI turn and make AI move if needed
  useEffect(() => {
    const checkAndMakeAIMove = async () => {
      const now = Date.now();
      const timeSinceLastMove = now - lastAIMoveTime;

      // Prevent rapid AI move requests (minimum 2 seconds between moves)
      if (timeSinceLastMove < 2000) {
        return;
      }

      if (gameMode === 'human_vs_ai' && turn === aiColor && !gameOver && !loading && !isAITurn) {
        setIsAITurn(true);
        setLastAIMoveTime(now);

        try {
          console.log(`AI's turn (${aiColor}). Making move...`);
          const response = await aiPlayMove();

          if (response.success) {
            console.log(`AI moved: ${response.ai_move.from_pos} to ${response.ai_move.to_pos}`);
            // The board will be updated automatically through the store
            await fetchBoard();
          } else {
            console.error('AI move failed');
          }
        } catch (error) {
          console.error('Error making AI move:', error);
        } finally {
          setIsAITurn(false);
        }
      }
    };

    checkAndMakeAIMove();
  }, [gameMode, turn, aiColor, gameOver, loading, isAITurn, lastAIMoveTime]);

  async function handleSquareClick(rowIdx: number, colIdx: number) {
    if (loading || gameOver || isAITurn) return;

    // Don't allow moves if it's AI's turn
    if (gameMode === 'human_vs_ai' && turn === aiColor) {
      return;
    }

    if (selectedSquare) {
      if (selectedSquare[0] === rowIdx && selectedSquare[1] === colIdx) {
        selectSquare(null); // Deselect if clicking the same square
      } else {
        await sendMove(selectedSquare, [rowIdx, colIdx]);
        selectSquare(null);
      }
    } else if (board[rowIdx][colIdx]) {
      // Only allow selecting pieces of the current player's color
      const piece = board[rowIdx][colIdx];
      if (piece && piece.color === turn) {
        selectSquare([rowIdx, colIdx]);
      }
    }
  }

  const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  const ranks = ['8', '7', '6', '5', '4', '3', '2', '1'];

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

      {isAITurn && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.3)',
            color: 'white',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 10,
            fontSize: '1.5rem',
            fontWeight: 'bold',
          }}
        >
          <div>🤖 AI is thinking...</div>
          <div style={{ fontSize: '1rem', marginTop: '0.5rem' }}>Please wait</div>
        </div>
      )}

      {/* Chessboard with coordinates */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {/* Top coordinate area (empty for now, could be used for perspective) */}
        <div style={{ height: 20, width: 400 }}></div>

        <div style={{ display: 'flex', alignItems: 'center' }}>
          {/* Left coordinate area (ranks) */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              width: 20,
              height: 400,
              justifyContent: 'space-between',
              alignItems: 'center',
              paddingTop: 0,
              paddingBottom: 0,
              boxSizing: 'border-box',
            }}
          >
            {ranks.map((rank) => (
              <div key={rank} className="chessboard-coordinate chessboard-rank">
                {rank}
              </div>
            ))}
          </div>

          {/* Main chessboard */}
          <div
            style={{
              display: 'grid',
              gridTemplateRows: 'repeat(8, 1fr)',
              gridTemplateColumns: 'repeat(8, 1fr)',
              width: 400,
              height: 400,
              border: '2px solid #333',
              opacity: gameOver || isAITurn ? 0.6 : delayedLoading ? 0.5 : 1,
            }}
          >
            {board.map((row, rowIdx) =>
              row.map((piece, colIdx) => {
                const isLight = (rowIdx + colIdx) % 2 === 1;
                const isSelected =
                  selectedSquare && selectedSquare[0] === rowIdx && selectedSquare[1] === colIdx;

                // Determine if this square should be clickable
                const isClickable =
                  !loading &&
                  !gameOver &&
                  !isAITurn &&
                  (gameMode === 'human_vs_human' ||
                    (gameMode === 'human_vs_ai' && turn !== aiColor));

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
                      cursor: isClickable ? 'pointer' : 'not-allowed',
                      boxSizing: 'border-box',
                      border: isSelected ? '2px solid #f90' : undefined,
                      opacity: delayedLoading || isAITurn ? 0.5 : 1,
                    }}
                  >
                    {piece ? <Piece type={piece.type} color={piece.color} /> : null}
                  </div>
                );
              }),
            )}
          </div>

          {/* Right coordinate area (empty for now, could be used for perspective) */}
          <div style={{ width: 20, height: 400 }}></div>
        </div>

        {/* Bottom coordinate area (files) */}
        <div
          style={{
            display: 'flex',
            width: 400,
            height: 20,
            justifyContent: 'space-between',
            alignItems: 'center',
            paddingLeft: 0,
            paddingRight: 0,
            boxSizing: 'border-box',
          }}
        >
          {files.map((file) => (
            <div key={file} className="chessboard-coordinate chessboard-file">
              {file}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Chessboard;
