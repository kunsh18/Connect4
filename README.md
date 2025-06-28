# Connect4 Game with AI

A Python implementation of the classic Connect4 game featuring an AI opponent with multiple difficulty levels.

## Features
- AI opponent with three difficulty levels:
  - Easy: Uses Hill Climbing algorithm
  - Medium: Uses Simulated Annealing algorithm
  - Hard: Uses Minimax algorithm with Alpha-Beta pruning
- Option to choose who makes the first move
- A* inspired heuristic evaluation for AI decision making

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arbitcoper/Connect4.git
```

2. Install the required packages:
```bash
pip install pygame numpy
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Select difficulty level:
   - Press 1 for Easy
   - Press 2 for Medium
   - Press 3 for Hard

3. Choose who makes the first move:
   - Press A for AI to move first
   - Press S for Human to move first

4. Game Controls:
   - Click on a column to drop your piece
   - Press R to restart the game
   - Close window to quit

## AI Implementation

The AI uses different algorithms based on the selected difficulty level:

### Easy Mode (Hill Climbing)
- Uses local search to find good moves
- Makes decisions based on immediate board evaluation
- Less optimal but faster decision making

### Medium Mode (Simulated Annealing)
- Uses probabilistic approach to explore the solution space
- Can accept worse moves to escape local optima
- Balanced between optimality and speed

### Hard Mode (Minimax with Alpha-Beta Pruning)
- Uses complete game tree search
- Implements alpha-beta pruning for efficiency
- Makes the most optimal moves possible within its depth limit

### Heuristic Evaluation
The AI uses an A* inspired heuristic function that considers:
- Center control (weight: 3)
- Winning potential (weight: 10)
- Opponent blocking (weight: 8)
- Piece connectivity (weight: 5)

## Project Structure

- `main.py`: Main game loop and GUI implementation
- `board.py`: Board logic and game rules
- `ai_agent.py`: AI implementation with different strategies
