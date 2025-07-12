import React, { useState, useEffect } from 'react';
import { getAIConfig, setAIStrategy } from '../services/api';
import './AIStrategySelector.css';

interface AIConfig {
  strategy: string;
  use_multi_move_cache: boolean;
  cache_size: number;
  cached_moves_count: number;
}

const AIStrategySelector: React.FC = () => {
  const [config, setConfig] = useState<AIConfig | null>(null);
  const [loading, setLoading] = useState(false);
  const [useMultiMoveCache, setUseMultiMoveCache] = useState(true);
  const [cacheSize, setCacheSize] = useState(5);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await getAIConfig();
      setConfig(response);
      setUseMultiMoveCache(response.use_multi_move_cache);
      setCacheSize(response.cache_size);
    } catch (error) {
      console.error('Error fetching AI config:', error);
    }
  };

  const handleStrategyChange = async () => {
    setLoading(true);
    try {
      await setAIStrategy({
        use_multi_move_cache: useMultiMoveCache,
        cache_size: cacheSize,
      });
      await fetchConfig();
    } catch (error) {
      console.error('Error setting AI strategy:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!config) {
    return <div>Loading AI configuration...</div>;
  }

  return (
    <div className="ai-strategy-selector">
      <h3>🤖 AI Strategy Configuration</h3>

      <div className="strategy-section">
        <h4>Current Strategy: {config.strategy}</h4>
        <p>Cached moves: {config.cached_moves_count}</p>
      </div>

      <div className="controls-section">
        <div className="control-group">
          <label>
            <input
              type="checkbox"
              checked={useMultiMoveCache}
              onChange={(e) => setUseMultiMoveCache(e.target.checked)}
            />
            Use Multi-Move Caching
          </label>
          <p className="description">
            Generate multiple moves ahead to reduce API calls and improve strategy. Better for cost
            efficiency and planning.
          </p>
        </div>

        {useMultiMoveCache && (
          <div className="control-group">
            <label>
              Cache Size:
              <input
                type="number"
                min="1"
                max="10"
                value={cacheSize}
                onChange={(e) => setCacheSize(parseInt(e.target.value))}
              />
            </label>
            <p className="description">
              Number of moves to generate and cache ahead (1-10). Higher values = more API calls but
              better planning.
            </p>
          </div>
        )}

        <div className="control-group">
          <label>
            <input
              type="checkbox"
              checked={!useMultiMoveCache}
              onChange={(e) => setUseMultiMoveCache(!e.target.checked)}
            />
            Single-Move Full Analysis
          </label>
          <p className="description">
            Analyze the full board for each move without restrictions. Better for creative play but
            more expensive.
          </p>
        </div>

        <button onClick={handleStrategyChange} disabled={loading} className="strategy-button">
          {loading ? 'Updating...' : 'Update Strategy'}
        </button>
      </div>

      <div className="info-section">
        <h4>Strategy Comparison:</h4>
        <div className="comparison-grid">
          <div className="comparison-item">
            <strong>Multi-Move Caching:</strong>
            <ul>
              <li>✅ Lower API costs</li>
              <li>✅ Better planning</li>
              <li>✅ Faster responses</li>
              <li>❌ May miss tactical opportunities</li>
            </ul>
          </div>
          <div className="comparison-item">
            <strong>Full Analysis:</strong>
            <ul>
              <li>✅ More creative play</li>
              <li>✅ Better tactical awareness</li>
              <li>✅ Adapts to unexpected moves</li>
              <li>❌ Higher API costs</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIStrategySelector;
