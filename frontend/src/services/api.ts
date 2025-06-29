const API_BASE = 'http://localhost:8000';

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
