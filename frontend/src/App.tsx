import { useChessStore } from './store';
import Chessboard from './components/Chessboard';
import MoveHistory from './components/MoveHistory';

function App() {
  const sendReset = useChessStore((state) => state.sendReset);
  const loading = useChessStore((state) => state.loading);
  
  return (
    <div className="chess-game">
      <h1>Chess Game</h1>
      <div className="chess-controls">
        <button 
          className="reset-button" 
          onClick={sendReset}
          disabled={loading}
        >
          Reset Game
        </button>
      </div>
      <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center', alignItems: 'flex-start' }}>
        <Chessboard />
        <MoveHistory />
      </div>
    </div>
  )
}

export default App; 