import React from 'react';
import { useChessStore } from '../store';

const MoveHistory: React.FC = () => {
  const moveHistory = useChessStore((state) => state.moveHistory);
  return (
    <div className="move-history-container">
      <h3 className="move-history-title">Move History</h3>
      <ol className="move-history-list">
        {moveHistory.map((move, idx) => (
          <li key={idx} className="move-history-item">{move}</li>
        ))}
      </ol>
    </div>
  );
};

export default MoveHistory; 