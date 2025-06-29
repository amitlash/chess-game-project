import React, { useRef, useEffect } from 'react';
import { useChessStore } from '../store';
import type { MoveRecord } from '../store';

const MoveHistory: React.FC = () => {
  const moveHistory = useChessStore((state) => state.moveHistory);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Group moves by turn number
  const groupedMoves: { turn: number; white?: MoveRecord; black?: MoveRecord }[] = [];
  for (let i = 0; i < moveHistory.length; i += 2) {
    const white = moveHistory[i];
    const black = moveHistory[i + 1];
    groupedMoves.push({ turn: white.turn_number, white, black });
  }

  // Find the last move index for highlighting
  const lastMoveIdx = moveHistory.length - 1;
  const lastMove = moveHistory[lastMoveIdx];

  // Auto-scroll to bottom when new moves are added
  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  }, [moveHistory.length]);

  return (
    <div className="move-history-container">
      <h3 className="move-history-title">Move History</h3>
      <div
        ref={scrollContainerRef}
        style={{
          overflowY: 'auto',
          maxHeight: '340px',
          width: '100%',
        }}
      >
        <table
          style={{
            width: '100%',
            borderCollapse: 'collapse',
            fontSize: '0.95rem',
            color: '#f3f6fa',
          }}
        >
          <thead>
            <tr>
              <th
                style={{
                  textAlign: 'right',
                  width: 35,
                  padding: '8px 4px',
                  borderBottom: '1px solid rgba(96,165,250,0.3)',
                  color: '#f3f6fa',
                  fontWeight: 600,
                }}
              >
                #
              </th>
              <th
                style={{
                  textAlign: 'center',
                  width: 70,
                  padding: '8px 4px',
                  borderBottom: '1px solid rgba(96,165,250,0.3)',
                  color: '#f3f6fa',
                  fontWeight: 600,
                }}
              >
                White
              </th>
              <th
                style={{
                  textAlign: 'center',
                  width: 70,
                  padding: '8px 4px',
                  borderBottom: '1px solid rgba(96,165,250,0.3)',
                  color: '#f3f6fa',
                  fontWeight: 600,
                }}
              >
                Black
              </th>
            </tr>
          </thead>
          <tbody>
            {groupedMoves.map(({ turn, white, black }) => (
              <tr key={turn}>
                <td
                  style={{
                    textAlign: 'right',
                    fontWeight: 600,
                    padding: '6px 4px',
                    color: 'rgba(243, 246, 250, 0.7)',
                  }}
                >
                  {turn}.
                </td>
                <td
                  style={{
                    background:
                      lastMove === white
                        ? 'linear-gradient(90deg, #60a5fa 0%, #818cf8 100%)'
                        : 'transparent',
                    color: lastMove === white ? '#fff' : '#f3f6fa',
                    fontWeight: lastMove === white ? 700 : 500,
                    borderRadius: 6,
                    cursor: 'pointer',
                    textAlign: 'center',
                    padding: '6px 4px',
                    minWidth: 60,
                    transition: 'all 0.18s',
                  }}
                  title={white ? `${white.from_pos}→${white.to_pos}` : ''}
                >
                  {white ? white.algebraic_notation : ''}
                </td>
                <td
                  style={{
                    background:
                      lastMove === black
                        ? 'linear-gradient(90deg, #60a5fa 0%, #818cf8 100%)'
                        : 'transparent',
                    color: lastMove === black ? '#fff' : '#f3f6fa',
                    fontWeight: lastMove === black ? 700 : 500,
                    borderRadius: 6,
                    cursor: 'pointer',
                    textAlign: 'center',
                    padding: '6px 4px',
                    minWidth: 60,
                    transition: 'all 0.18s',
                  }}
                  title={black ? `${black.from_pos}→${black.to_pos}` : ''}
                >
                  {black ? black.algebraic_notation : ''}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MoveHistory;
