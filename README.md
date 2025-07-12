# ♟️ Chess Game Project with AI Integration

A **fullstack chess application** built with FastAPI backend and React TypeScript frontend, featuring advanced AI integration for an enhanced chess experience. The application includes conversational AI assistance, AI opponent gameplay, and intelligent position analysis.

---

## 🚀 Features

### 🧠 Chess Engine
* **Basic chess logic** with all piece movement rules
* **Turn-based gameplay** with enforced player alternation
* **Move history tracking** with algebraic notation
* **Game over detection** (when a king is captured)
* **Move validation** and error handling
* **Unit-tested** game logic

### 🤖 AI Integration
* **Conversational AI Assistant** - Chat with an AI about chess strategies, rules, and tips
* **AI Chess Opponent** - Play against an intelligent AI that analyzes positions and makes strategic moves
* **Position Analysis** - Get AI-powered insights about the current board position
* **Multiple Game Modes** - Choose between Human vs Human or Human vs AI gameplay
* **Configurable AI Color** - Set whether the AI plays as white or black

### 🛠 Backend (FastAPI)
* **RESTful API** with OpenAPI documentation
* **Modular architecture** with clear separation of concerns
* **AI Service Integration** using Groq API for intelligent responses
* **Error handling** and validation
* **CORS support** for frontend integration
* **Logging** capabilities
* **Test suite** with pytest

### 💻 Frontend (React + TypeScript)
* **Interactive chessboard** with piece selection and movement
* **Game state synchronization** with backend via API calls
* **Move history display** with turn-by-turn breakdown
* **Modern UI** with chess piece visualization
* **AI Chat Interface** - Floating chat window for chess assistance
* **AI Analysis Panel** - Dedicated panel for position analysis
* **Game Mode Selector** - Easy switching between game modes
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
│   │   │   └── routes.py              # API endpoints (including AI routes)
│   │   ├── core/
│   │   │   ├── game_engine.py         # Chess logic engine
│   │   │   └── ai_service.py          # AI integration service
│   │   ├── main.py                    # FastAPI application
│   │   └── tests/
│   │       ├── test_api.py            # API integration tests
│   │       ├── test_game_engine.py    # Game logic tests
│   │       ├── test_ai_service.py     # AI service tests
│   │       └── test_integration_server.py # End-to-end tests
│   └── requirements.txt               # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chessboard.tsx         # Interactive chessboard
│   │   │   ├── MoveHistory.tsx        # Move history display
│   │   │   ├── Piece.tsx              # Chess piece component
│   │   │   ├── ChatInterface.tsx      # AI chat interface
│   │   │   ├── GameModeSelector.tsx   # Game mode selection
│   │   │   └── AIAnalysis.tsx         # Position analysis panel
│   │   ├── services/
│   │   │   └── api.ts                 # Backend API client (with AI endpoints)
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
* **Groq API Key** (for AI features)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd chess_game
```

### 2. Environment Setup
Create a `.env` file in the backend directory:
```bash
cd backend
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 3. Backend Setup
```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Run the server
cd app
uvicorn main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

### 5. Access the Application
* **Frontend**: http://localhost:5173
* **Backend API**: http://localhost:8000
* **API Documentation**: http://localhost:8000/docs

---

## 🤖 AI Features Guide

### Chat with AI Assistant
1. Click the **💬** button in the bottom-right corner
2. Ask questions about chess rules, strategies, or get tips
3. The AI will provide helpful, contextual responses
4. Chat history is maintained during your session

### Play Against AI
1. Use the **Game Mode Selector** to choose "Human vs AI"
2. Select whether the AI plays as White or Black
3. Make your moves normally - the AI will automatically respond
4. The AI analyzes positions and makes strategic decisions

### Get Position Analysis
1. Click the **🔍** button in the bottom-right corner
2. Click "Analyze Position" to get AI insights
3. Review material balance, tactical opportunities, and strategic recommendations
4. Request new analysis at any time during the game

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

### AI Endpoints

#### `POST /chat`
Chat with AI assistant
```json
{
  "message": "What's the best opening for beginners?",
  "message_history": [...]
}
```

#### `POST /ai-move`
Get AI move suggestion
```json
{
  "board": { "e2": "P", "e4": ".", ... },
  "turn": "white",
  "move_history": [...]
}
```

#### `GET /analyze`
Get position analysis
```json
{
  "analysis": "This position shows equal material...",
  "board": { "e2": "P", "e4": ".", ... },
  "turn": "white"
}
```

#### `POST /game-mode`
Set game mode
```json
{
  "mode": "human_vs_ai",
  "ai_color": "black"
}
```

#### `POST /ai-play`
Make AI move in current game
```json
{
  "success": true,
  "ai_move": {"from_pos": "e7", "to_pos": "e5"},
  "board": { "e2": "P", "e4": ".", ... },
  "game_over": false,
  "turn": "white",
  "move_history": [...]
}
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend/app
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest tests/test_ai_service.py  # Run AI service tests
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
* **TypeScript** for type safety
* **Comprehensive testing** for all AI features

---

## 🎯 AI Integration Architecture

### Backend AI Service
The AI integration is built around a modular `AIService` class that:
- Manages Groq API communication
- Converts chess positions to FEN notation
- Generates legal moves for AI analysis
- Provides conversational chess assistance
- Analyzes board positions strategically

### Frontend AI Components
The frontend includes specialized components for AI interaction:
- **ChatInterface**: Floating chat window for chess assistance
- **AIAnalysis**: Dedicated panel for position analysis
- **GameModeSelector**: Easy switching between game modes
- **Enhanced Chessboard**: AI move handling and turn management

### AI Features
1. **Conversational AI**: Context-aware chess assistance
2. **Strategic Play**: AI opponent with position evaluation
3. **Position Analysis**: Real-time board assessment
4. **Move Generation**: Intelligent move selection
5. **Error Handling**: Graceful fallbacks when AI is unavailable

---

## 🔒 Security & Configuration

### API Key Management
- Store your Groq API key in a `.env` file
- Never commit API keys to version control
- The application gracefully handles missing API keys

### Error Handling
- Comprehensive error handling for AI service failures
- Fallback mechanisms when AI is unavailable
- User-friendly error messages

---

## 🚀 Future Enhancements

### Planned AI Features
- **Multiple AI Difficulty Levels**
- **Opening Book Integration**
- **Endgame Tablebase Support**
- **Move Time Control**
- **AI Training Mode**

### Technical Improvements
- **WebSocket Integration** for real-time AI responses
- **Caching Layer** for AI responses
- **Advanced Position Evaluation**
- **Multiplayer AI Support**

---

*This project demonstrates advanced AI integration in a chess application, following professional development standards and best practices.*
