# ♟️ Chess Game Project

A **fullstack chess application** built with FastAPI backend and React TypeScript frontend. Features basic chess gameplay with modern development practices, testing, and automated quality gates.

---

## 🚀 Features

### 🧠 Chess Engine
* **Basic chess logic** with all piece movement rules
* **Turn-based gameplay** with enforced player alternation
* **Move history tracking** with algebraic notation
* **Game over detection** (when a king is captured)
* **Move validation** and error handling
* **Unit-tested** game logic

### 🛠 Backend (FastAPI)
* **RESTful API** with OpenAPI documentation
* **Modular architecture** with clear separation of concerns
* **Error handling** and validation
* **CORS support** for frontend integration
* **Logging** capabilities
* **Test suite** with pytest

### 💻 Frontend (React + TypeScript)
* **Interactive chessboard** with piece selection and movement
* **Game state synchronization** with backend via API calls
* **Move history display** with turn-by-turn breakdown
* **Modern UI** with chess piece visualization
* **State management** with Zustand
* **TypeScript** for type safety

### 🔧 Development Quality
* **Pre-commit hooks** for automated code quality
* **Professional Git workflow** with branching strategy
* **Automated linting** (ESLint, Prettier, Black, Flake8)
* **Type checking** (mypy, TypeScript)
* **Security scanning** (Bandit)
* **Conventional commits** enforcement

---

## 📁 Project Structure

```
chess_game/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py              # API endpoints
│   │   ├── core/
│   │   │   └── game_engine.py         # Chess logic engine
│   │   ├── main.py                    # FastAPI application
│   │   └── tests/
│   │       ├── test_api.py            # API integration tests
│   │       ├── test_game_engine.py    # Game logic tests
│   │       └── test_integration_server.py # End-to-end tests
│   └── requirements.txt               # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chessboard.tsx         # Interactive chessboard
│   │   │   ├── MoveHistory.tsx        # Move history display
│   │   │   └── Piece.tsx              # Chess piece component
│   │   ├── services/
│   │   │   └── api.ts                 # Backend API client
│   │   ├── store.ts                   # State management
│   │   └── App.tsx                    # Main application
│   ├── package.json                   # Node.js dependencies
│   └── vite.config.ts                 # Build configuration
│
├── .pre-commit-config.yaml            # Quality gates configuration
├── GIT_WORKFLOW.md                    # Professional Git workflow
├── ROADMAP.md                         # Project roadmap and phases
├── README.md                          # This file
└── start.sh                           # Development startup script
```

---

## 🚀 Quick Start

### Prerequisites
* **Python 3.9+**
* **Node.js 18+**
* **Git**

### 1. Clone and Setup
```bash
git clone <repository-url>
cd chess_game
```

### 2. Backend Setup
```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Run the server
cd app
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

### 4. Access the Application
* **Frontend**: http://localhost:5173
* **Backend API**: http://localhost:8000
* **API Documentation**: http://localhost:8000/docs

---

## 🧪 Testing

### Backend Tests
```bash
cd backend/app
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest tests/test_api.py         # Run specific test file
pytest --cov=app                 # With coverage report
```

### Frontend Tests
```bash
cd frontend
npm run test                     # Run unit tests
npm run test:coverage            # With coverage report
```

### Quality Gates
```bash
# Run pre-commit hooks manually
pre-commit run --all-files

# Install pre-commit hooks (automatic on commit)
pre-commit install
```

---

## 📬 API Reference

### Core Endpoints

#### `GET /board`
Fetch current game state
```json
{
  "board": { "e2": "P", "e4": ".", ... },
  "turn": "white",
  "game_over": false,
  "move_history": [...]
}
```

#### `POST /move`
Make a chess move
```json
{
  "from_pos": "e2",
  "to_pos": "e4"
}
```

#### `POST /reset`
Reset game to initial state
```json
{
  "message": "Game reset",
  "move_history": []
}
```

---

## 🔧 Development Workflow

### Git Workflow
This project follows a **professional Git workflow**:

1. **Feature branches**: `feat/feature-name`
2. **Development branches**: `dev/backend`, `dev/frontend`
3. **Quality gates**: Pre-commit hooks enforce code quality
4. **Conventional commits**: Structured commit messages

See [GIT_WORKFLOW.md](./GIT_WORKFLOW.md) for detailed workflow.

### Code Quality
* **Pre-commit hooks** run automatically on every commit
* **ESLint + Prettier** for frontend code
* **Black + isort + flake8** for Python code
* **TypeScript + mypy** for type safety
* **Bandit** for security scanning

### Adding Features
1. Create feature branch from appropriate dev branch
2. Implement feature with tests
3. Ensure all quality gates pass
4. Create pull request
5. Code review and merge

---

## 🎯 Current Status

### ✅ Implemented
* Basic chess game logic with piece movement
* Interactive frontend with React
* RESTful API with FastAPI
* Testing suite for backend
* Professional Git workflow
* Automated quality gates
* Move history tracking
* Game over detection (king capture)

### 🚧 In Progress
* Enhanced UI/UX improvements
* Additional chess features

### 📋 Planned
* Check and checkmate detection
* Castling, en passant, and pawn promotion
* Multiplayer support
* AI opponent
* Game analysis tools
* Tournament mode
* Mobile responsiveness

---

## ⚠️ Limitations

* **No check detection** - moves that put your own king in check are allowed
* **No checkmate detection** - game only ends when a king is captured
* **No stalemate detection** - game continues even in stalemate positions
* **No special moves** - castling, en passant, and pawn promotion not implemented
* **Basic UI** - functional but minimal styling

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feat/amazing-feature`)
3. **Follow** the Git workflow and quality standards
4. **Test** your changes thoroughly
5. **Commit** with conventional commit format
6. **Push** to your branch (`git push origin feat/amazing-feature`)
7. **Open** a Pull Request

### Development Standards
* Follow the established Git workflow
* Ensure all pre-commit hooks pass
* Write tests for new features
* Update documentation as needed
* Use conventional commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

* Built with modern web technologies
* Follows development best practices
* Emphasizes code quality and maintainability
* Designed for learning and extension
