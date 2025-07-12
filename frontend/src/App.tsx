import './App.css';
import { useChessStore } from './store';
import Chessboard from './components/Chessboard';
import MoveHistory from './components/MoveHistory';
import GameModeSelector from './components/GameModeSelector';
import ChatInterface from './components/ChatInterface';
import AIAnalysis from './components/AIAnalysis';
import AIStrategySelector from './components/AIStrategySelector';
import { useEffect, useState } from 'react';

function App() {
  const sendReset = useChessStore((state) => state.sendReset);
  const loading = useChessStore((state) => state.loading);
  const error = useChessStore((state) => state.error);

  // AI feature states
  const [gameMode, setGameMode] = useState('human_vs_human');
  const [aiColor, setAIColor] = useState('black');
  const [chatOpen, setChatOpen] = useState(false);
  const [analysisOpen, setAnalysisOpen] = useState(false);
  const [showStrategySelector, setShowStrategySelector] = useState(false);

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

  useEffect(() => {
    // Initialize the game
    const fetchBoard = useChessStore.getState().fetchBoard;
    fetchBoard();
  }, []);

  // Handle game mode changes
  const handleGameModeChange = (mode: string, color: string) => {
    setGameMode(mode);
    setAIColor(color);
    console.log(`Game mode changed to: ${mode}, AI color: ${color}`);
  };

  // Handle chat toggle
  const handleChatToggle = () => {
    setChatOpen(!chatOpen);
    if (!chatOpen) {
      setAnalysisOpen(false);
    }
  };

  // Handle analysis toggle
  const handleAnalysisToggle = () => {
    setAnalysisOpen(!analysisOpen);
    if (!analysisOpen) {
      setChatOpen(false);
    }
  };

  return (
    <div
      className="chess-game"
      style={{ gap: 8, paddingTop: 12, paddingBottom: 0, minHeight: 'unset' }}
    >
      <h1 style={{ marginBottom: 8, marginTop: 8 }}>♟️ Chess Game with AI</h1>

      <div
        style={{ display: 'flex', gap: '2rem', justifyContent: 'center', alignItems: 'flex-start' }}
      >
        <Chessboard gameMode={gameMode} aiColor={aiColor} />
        <MoveHistory />
      </div>

      <div
        className="chess-controls"
        style={{ marginTop: 16, marginBottom: 0, justifyContent: 'center', gap: '16px' }}
      >
        <GameModeSelector
          onModeChange={handleGameModeChange}
          currentMode={gameMode}
          currentAIColor={aiColor}
        />
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

      {/* AI Features */}
      <div className="controls-container">
        <div className="control-buttons">
          <button
            onClick={handleChatToggle}
            className={`control-button ${chatOpen ? 'active' : ''}`}
          >
            💬 {chatOpen ? 'Hide Chat' : 'Show Chat'}
          </button>

          <button
            onClick={handleAnalysisToggle}
            className={`control-button ${analysisOpen ? 'active' : ''}`}
          >
            🔍 {analysisOpen ? 'Hide Analysis' : 'Show Analysis'}
          </button>

          <button
            onClick={() => setShowStrategySelector(!showStrategySelector)}
            className={`control-button ${showStrategySelector ? 'active' : ''}`}
          >
            ⚙️ {showStrategySelector ? 'Hide AI Config' : 'AI Config'}
          </button>
        </div>

        {showStrategySelector && <AIStrategySelector />}

        {chatOpen && <ChatInterface isOpen={chatOpen} onToggle={handleChatToggle} />}

        {analysisOpen && <AIAnalysis isOpen={analysisOpen} onToggle={handleAnalysisToggle} />}
      </div>
    </div>
  );
}

export default App;
