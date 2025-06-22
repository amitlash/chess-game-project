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
* Unit-tested with `unittest` and `TestClient`

### 💻 Frontend (React)

* Calls backend APIs to display and update game state
* Organized with modular components and API service file
* React + Vite setup

---

## 🧪 Limitations

* No check/checkmate logic — the game ends when a king is removed
* No special rules (castling, en passant, promotion)
* No multiplayer or AI
* Minimal UI — currently functional, not styled

---

## 📁 Project Structure

```
my-chess-app/
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
│   └── requirements.txt
│
├── frontend/                       # Not yet implemented
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/api.js         # Frontend API calls to backend
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
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

*Not yet implemented.*

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

* `GET /api/board` — fetch current board and state
* `POST /api/move` — submit a move `{ from_pos, to_pos }`
* `POST /api/reset` — reset the game to initial state

---

## 🧪 Run Tests

### Backend Unit Tests:

```bash
cd backend/app
python -m unittest discover
```

(Or use `pytest`)

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
