import React from 'react';

const placeholderMoves = [
  'e4', 'e5',
  'Nf3', 'Nc6',
  'Bb5', 'a6',
  'Ba4', 'Nf6',
  'O-O', 'Be7',
];

const MoveHistory: React.FC = () => {
  return (
    <div style={{ width: 200, minHeight: 400, background: '#fafafa', border: '2px solid #333', padding: 16 }}>
      <h3>Move History</h3>
      <ol>
        {placeholderMoves.map((move, idx) => (
          <li key={idx}>{move}</li>
        ))}
      </ol>
    </div>
  );
};

export default MoveHistory; 