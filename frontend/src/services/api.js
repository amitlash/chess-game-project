export async function getBoard() {
    const res = await fetch("http://localhost:8000/board");
    return res.json();
  }
  
  export async function makeMove(from, to) {
    const res = await fetch("http://localhost:8000/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ from_pos: from, to_pos: to })
    });
    return res.json();
  }
  
  export async function resetGame() {
    const res = await fetch("http://localhost:8000/reset", {
      method: "POST"
    });
    return res.json();
  }