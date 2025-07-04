import './App.css';
import { useChessStore } from './store';
import Chessboard from './components/Chessboard';
import MoveHistory from './components/MoveHistory';
import React, { useEffect, useState } from 'react';

function App() {
  const sendReset = useChessStore((state) => state.sendReset);
  const loading = useChessStore((state) => state.loading);
  const error = useChessStore((state) => state.error);

  // Add delayed loading state for the loading message
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

  return (
    <div
      className="chess-game"
      style={{ gap: 8, paddingTop: 12, paddingBottom: 0, minHeight: 'unset' }}
    >
      <h1 style={{ marginBottom: 8, marginTop: 8 }}>Chess Game</h1>
      <div
        style={{ display: 'flex', gap: '2rem', justifyContent: 'center', alignItems: 'flex-start' }}
      >
        <Chessboard />
        <MoveHistory />
      </div>
      <div
        className="chess-controls"
        style={{ marginTop: 16, marginBottom: 0, justifyContent: 'center' }}
      >
        <button className="reset-button" onClick={sendReset} disabled={loading}>
          Reset Game
        </button>
      </div>
      <div
        style={{
          minHeight: 24,
          marginTop: 4,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {delayedLoading && <span style={{ color: 'orange' }}>Loading...</span>}
        {!loading && error && <span style={{ color: 'red' }}>{error}</span>}
      </div>
    </div>
  );
}

export default App;
