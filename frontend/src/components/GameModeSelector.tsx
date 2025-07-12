import { useState } from 'react';
import { setGameMode } from '../services/api';
import type { GameModeRequest } from '../services/api';
import './GameModeSelector.css';

interface GameModeSelectorProps {
  onModeChange: (mode: string, aiColor: string) => void;
  currentMode?: string;
  currentAIColor?: string;
}

export default function GameModeSelector({
  onModeChange,
  currentMode = 'human_vs_human',
  currentAIColor = 'black',
}: GameModeSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedMode, setSelectedMode] = useState(currentMode);
  const [selectedAIColor, setSelectedAIColor] = useState(currentAIColor);
  const [isLoading, setIsLoading] = useState(false);

  const handleModeChange = async (mode: string, aiColor: string = 'black') => {
    setIsLoading(true);
    try {
      const request: GameModeRequest = {
        mode: mode as 'human_vs_human' | 'human_vs_ai',
        ai_color: aiColor as 'white' | 'black',
      };

      await setGameMode(request);
      setSelectedMode(mode);
      setSelectedAIColor(aiColor);
      onModeChange(mode, aiColor);
      setIsOpen(false);
    } catch (error) {
      console.error('Failed to set game mode:', error);
      alert('Failed to set game mode. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getModeDisplayName = (mode: string) => {
    switch (mode) {
      case 'human_vs_human':
        return '👥 Human vs Human';
      case 'human_vs_ai':
        return '🤖 Human vs AI';
      default:
        return mode;
    }
  };

  const getColorDisplayName = (color: string) => {
    return color === 'white' ? '⚪ White' : '⚫ Black';
  };

  return (
    <div className="game-mode-selector">
      <button
        className="mode-selector-button"
        onClick={() => setIsOpen(!isOpen)}
        disabled={isLoading}
      >
        <span className="mode-icon">{selectedMode === 'human_vs_human' ? '👥' : '🤖'}</span>
        <span className="mode-text">
          {getModeDisplayName(selectedMode)}
          {selectedMode === 'human_vs_ai' && (
            <span className="ai-color"> ({getColorDisplayName(selectedAIColor)})</span>
          )}
        </span>
        <span className="dropdown-arrow">▼</span>
      </button>

      {isOpen && (
        <div className="mode-dropdown">
          <div className="mode-options">
            <button
              className={`mode-option ${selectedMode === 'human_vs_human' ? 'selected' : ''}`}
              onClick={() => handleModeChange('human_vs_human')}
            >
              <span className="mode-icon">👥</span>
              <div className="mode-details">
                <div className="mode-name">Human vs Human</div>
                <div className="mode-description">Play against another person</div>
              </div>
            </button>

            <button
              className={`mode-option ${selectedMode === 'human_vs_ai' ? 'selected' : ''}`}
              onClick={() => handleModeChange('human_vs_ai', selectedAIColor)}
            >
              <span className="mode-icon">🤖</span>
              <div className="mode-details">
                <div className="mode-name">Human vs AI</div>
                <div className="mode-description">Play against the AI assistant</div>
              </div>
            </button>
          </div>

          {selectedMode === 'human_vs_ai' && (
            <div className="ai-color-selector">
              <div className="color-label">AI plays as:</div>
              <div className="color-options">
                <button
                  className={`color-option ${selectedAIColor === 'black' ? 'selected' : ''}`}
                  onClick={() => handleModeChange('human_vs_ai', 'black')}
                >
                  ⚫ Black (AI plays second)
                </button>
                <button
                  className={`color-option ${selectedAIColor === 'white' ? 'selected' : ''}`}
                  onClick={() => handleModeChange('human_vs_ai', 'white')}
                >
                  ⚪ White (AI plays first)
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
