import React from 'react';
import { useChessStore } from '../store';

const MoveHistory: React.FC = () => {
  const moveHistory = useChessStore((state) => state.moveHistory);
  return (
    <div style={{ width: 200, minHeight: 400, background: '#fafafa', border: '2px solid #333', padding: 16 }}>
      <h3>Move History</h3>
      <ol>
        {moveHistory.map((move, idx) => (
          <li key={idx}>{move}</li>
        ))}
      </ol>
    </div>
  );
};

export default MoveHistory; 