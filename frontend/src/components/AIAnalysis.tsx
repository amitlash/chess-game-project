import { useState } from 'react';
import { analyzePosition } from '../services/api';
import type { AnalysisResponse } from '../services/api';
import './AIAnalysis.css';

interface AIAnalysisProps {
  isOpen: boolean;
  onToggle: () => void;
}

export default function AIAnalysis({ isOpen, onToggle }: AIAnalysisProps) {
  const [analysis, setAnalysis] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleAnalyze = async () => {
    setIsLoading(true);
    setError('');

    try {
      const response: AnalysisResponse = await analyzePosition();
      setAnalysis(response.analysis);
    } catch (err) {
      console.error('Analysis error:', err);
      setError('Failed to analyze position. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const clearAnalysis = () => {
    setAnalysis('');
    setError('');
  };

  if (!isOpen) {
    return (
      <button className="analysis-toggle-button" onClick={onToggle} title="AI Position Analysis">
        🔍
      </button>
    );
  }

  return (
    <div className="ai-analysis">
      <div className="analysis-header">
        <h3>🔍 AI Position Analysis</h3>
        <div className="analysis-controls">
          <button
            className="clear-analysis-button"
            onClick={clearAnalysis}
            title="Clear analysis"
            disabled={!analysis && !error}
          >
            🗑️
          </button>
          <button className="close-analysis-button" onClick={onToggle} title="Close analysis">
            ✕
          </button>
        </div>
      </div>

      <div className="analysis-content">
        {!analysis && !error && (
          <div className="analysis-welcome">
            <p>Get AI insights about the current position:</p>
            <ul>
              <li>📊 Material balance</li>
              <li>🎯 Tactical opportunities</li>
              <li>🏗️ Positional strengths</li>
              <li>💡 Strategic recommendations</li>
            </ul>
            <button className="analyze-button" onClick={handleAnalyze} disabled={isLoading}>
              {isLoading ? 'Analyzing...' : 'Analyze Position'}
            </button>
          </div>
        )}

        {isLoading && (
          <div className="analysis-loading">
            <div className="loading-spinner"></div>
            <p>AI is analyzing the position...</p>
          </div>
        )}

        {error && (
          <div className="analysis-error">
            <p>❌ {error}</p>
            <button className="retry-button" onClick={handleAnalyze} disabled={isLoading}>
              Try Again
            </button>
          </div>
        )}

        {analysis && !isLoading && (
          <div className="analysis-result">
            <div className="analysis-text">
              {analysis.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
            <button className="new-analysis-button" onClick={handleAnalyze} disabled={isLoading}>
              {isLoading ? 'Analyzing...' : 'New Analysis'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
