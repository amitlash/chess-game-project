const API_BASE = 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  message_history: ChatMessage[];
}

export interface ChatResponse {
  response: string;
  message_history: ChatMessage[];
}

export interface AIMove {
  from_pos: string;
  to_pos: string;
  piece: string;
  color: string;
  captured_piece?: string | null;
  is_capture: boolean;
  algebraic_notation: string;
  turn_number: number;
}

export interface AIMoveRequest {
  board: Record<string, string>;
  turn: string;
  move_history: AIMove[];
}

export interface AIMoveResponse {
  success: boolean;
  from_pos?: string;
  to_pos?: string;
  move?: string;
  message?: string;
}

export interface GameModeRequest {
  mode: 'human_vs_human' | 'human_vs_ai';
  ai_color?: 'white' | 'black';
}

export interface GameModeResponse {
  message: string;
  mode: string;
  ai_color: string;
}

export interface AnalysisResponse {
  analysis: string;
  board: Record<string, string>;
  turn: string;
}

export interface AIPlayResponse {
  success: boolean;
  ai_move: { from_pos: string; to_pos: string };
  board: Record<string, string>;
  game_over: boolean;
  turn: string;
  move_history: AIMove[];
}

export async function getBoard() {
  const res = await fetch(`${API_BASE}/board`);
  if (!res.ok) throw new Error('Failed to fetch board');
  return res.json();
}

export async function makeMove(from_pos: string, to_pos: string) {
  const res = await fetch(`${API_BASE}/move`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ from_pos, to_pos }),
  });
  if (!res.ok) throw new Error('Failed to make move');
  return res.json();
}

export async function resetGame() {
  const res = await fetch(`${API_BASE}/reset`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to reset game');
  return res.json();
}

export async function chatWithAI(request: ChatRequest): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error('Failed to chat with AI');
  return res.json();
}

export async function getAIMove(request: AIMoveRequest): Promise<AIMoveResponse> {
  const res = await fetch(`${API_BASE}/ai-move`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error('Failed to get AI move');
  return res.json();
}

export async function analyzePosition(): Promise<AnalysisResponse> {
  const res = await fetch(`${API_BASE}/analyze`);
  if (!res.ok) throw new Error('Failed to analyze position');
  return res.json();
}

export async function setGameMode(request: GameModeRequest): Promise<GameModeResponse> {
  const res = await fetch(`${API_BASE}/game-mode`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error('Failed to set game mode');
  return res.json();
}

export async function aiPlayMove(): Promise<AIPlayResponse> {
  const res = await fetch(`${API_BASE}/ai-play`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) throw new Error('Failed to make AI move');
  return res.json();
}

export const setAIStrategy = async (strategy: {
  use_multi_move_cache: boolean;
  cache_size: number;
}) => {
  const response = await fetch(`${API_BASE}/ai-strategy`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(strategy),
  });

  if (!response.ok) {
    throw new Error(`Failed to set AI strategy: ${response.statusText}`);
  }

  return response.json();
};

export const getAIConfig = async () => {
  const response = await fetch(`${API_BASE}/ai-config`);

  if (!response.ok) {
    throw new Error(`Failed to get AI config: ${response.statusText}`);
  }

  return response.json();
};
