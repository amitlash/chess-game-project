Here’s a **professional README** for your chess project that reflects its current features, structure, and usage:

---

## ♟️ Simple Chess in Python

A minimalist terminal-based chess game written in Python. This project allows two players to take turns playing chess via standard input, with basic piece movement and win condition detection.

---

### 🚀 Features

* Fully initialized 8x8 chessboard with standard starting positions
* Supports all basic piece types: pawn, rook, knight, bishop, queen, king
* Turn-based movement with alternating white/black turns
* Capture announcements with piece name and location
* Game-over logic when a king is captured
* Input validation and simple error messages
* Testable architecture with an included test suite (`test_chess.py`)
* CLI test runner support using `python chessboard.py test`

---

### 🧠 Limitations

* No special rules: no castling, en passant, or pawn promotion
* No check/checkmate logic — the game ends when a king is missing
* No AI or multiplayer over network
* Movement rules are enforced but simplified

---

### 📂 Project Structure

```
.
├── chessboard.py      # Main game logic and CLI interface
├── test_chess.py      # Unit tests for the game logic
└── README.md          # Project documentation
```

---

### ▶️ Usage

#### To Play:

```bash
python chessboard.py
```

Follow the prompt and enter moves like:

```
e2 e4
g8 f6
```

#### To Run Tests:

```bash
python chessboard.py test
```

---

### 🧪 Sample Output

```
Welcome to Simple Chess!
White's move (e.g. e2 e4): e2 e4
Black's move (e.g. e7 e5): e7 e5
White captures black pawn on e5!
...
Black wins! White's king is missing.
Game over.
```

---

### ✅ Requirements

* Python 3.7+

No external dependencies are required.

---

### 📌 Todo (Optional Improvements)

* Add check/checkmate and stalemate logic
* Implement castling, en passant, and promotion
* Add board annotation and move history
* Build a GUI or online version
* Add a computer opponent

---

### 📄 License

This project is open source and licensed under the MIT License.

---