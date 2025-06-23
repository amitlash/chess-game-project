Here’s an **updated and professional `README.md`** tailored to the current state of your project — now a fullstack web app with a FastAPI backend and a React frontend:

---

# ♟️ Simple Chess Web App

A fullstack Python & React chess web application. Built with a FastAPI backend serving a basic turn-based chess engine, and a React frontend for interactive play. This project emphasizes simplicity, modularity, and testable architecture.

---

## 🚀 Features

### 🧠 Chess Engine

* Fully initialized 8x8 board with standard starting positions
* Piece movement rules: pawn, rook, knight, bishop, queen, king
* Turn-based logic with enforced player alternation
* Capture announcements (via logs)
* Game over when a king is missing
* Structured and unit-tested game logic

### 🛠 Backend (FastAPI)

* REST API endpoints for:

  * Fetching board state
  * Making a move
  * Resetting the game
* Logging and error handling
* Modular structure for scalability
* Unit-tested with `pytest` and `TestClient`

### 💻 Frontend (React)

* API service file for backend communication (`src/services/api.js`)
* (UI components not yet implemented)

---

## 🧪 Limitations

* No check/checkmate logic — the game ends when a king is removed
* No special rules (castling, en passant, promotion)
* No multiplayer or AI
* Minimal UI — currently functional, not styled

---

## 📁 Project Structure

```
chess_game/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py           # API routes (GET /board, POST /move)
│   │   ├── core/
│   │   │   └── game_engine.py      # Main chess logic with logging
│   │   ├── main.py                 # FastAPI entrypoint
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_game_engine.py # Unit tests for core logic
│   │       └── test_api.py         # Unit tests for API
│   └── requirements.txt            # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   └── services/api.js         # Frontend API calls to backend
│
├── README.md
└── run_all.sh                      # Optional: run frontend & backend together
```

---

## ▶️ Usage

### 🐍 Backend (FastAPI)

#### Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

#### Run the server:

```bash
cd app
uvicorn main:app --reload
```

* Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🌐 Frontend (React)

*Not yet implemented beyond API service.*

#### Install dependencies:

```bash
cd frontend
npm install
```

#### Start the React dev server:

```bash
npm run dev
```

---

### 📬 API Endpoints

* `GET /board` — fetch current board and state
* `POST /move` — submit a move with JSON body: `{ "from_pos": "e2", "to_pos": "e4" }`
* `POST /reset` — reset the game to initial state

---

## 🧪 Run Tests

### Backend Unit & API Tests (Recommended: pytest):

```bash
cd backend/app
pytest
```

Or run a specific test file:

```bash
pytest tests/test_game_engine.py
pytest tests/test_api.py
```

> **Note:**
> - Run tests from the `backend/app` directory. The test imports expect this as the working directory.
> - If you see `ModuleNotFoundError: No module named 'app'` or `No module named 'core'`, check your working directory and ensure you are running the test commands from `backend/app`.
> - For API tests, the `/move` endpoint expects a JSON body: `{ "from_pos": "e2", "to_pos": "e4" }`.
> - If `pytest` is not installed, run `pip install pytest` inside your virtual environment.

---

## 📌 Todo / Improvements

* Implement check, checkmate, and stalemate detection
* Support castling, en passant, and promotion
* Add multiplayer and authentication
* Add move history and PGN export
* Style the frontend board with piece images
* Add AI opponent
* Add AI chat helper / tutor

---

## ✅ Requirements

* Python 3.8+
* Node.js 16+

---

## 📄 License

Licensed under the MIT License.

---
