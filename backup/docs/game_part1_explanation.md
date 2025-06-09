# Understanding game.py (Part 1) - Game Initialization and State Management

## Overview
This part of `game.py` handles the game's initialization and state management. It's responsible for setting up the game and maintaining its current state.

## Key Components

### MemoryGame Class
```python
class MemoryGame:
    def __init__(self):
        self.ui = UI()
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state."""
        self.cards = generate_cards()
        self.flipped = [False] * len(self.cards)
        self.moves = 0
        self.first_card: Optional[int] = None
        self.second_card: Optional[int] = None
        self.game_over = False
```

## State Management

### Game State Variables
1. `self.cards`: List of card values
   - Generated using `utils.generate_cards()`
   - Contains pairs of numbers
   - Never changes during gameplay

2. `self.flipped`: List of boolean values
   - Tracks which cards are face-up
   - Same length as `self.cards`
   - Changes when cards are flipped

3. `self.moves`: Integer counter
   - Tracks number of moves made
   - Increments when two cards are flipped
   - Used for scoring

4. `self.first_card` and `self.second_card`: Optional integers
   - Track currently selected cards
   - Reset after each pair check
   - Used for matching logic

5. `self.game_over`: Boolean flag
   - Indicates if game is complete
   - Set when all pairs are matched

## How It Connects to Other Files

### Connection to utils.py
- Uses `generate_cards()` for initial card setup
- Relies on constants like `GRID_SIZE` and `TOTAL_PAIRS`

### Connection to ui.py
- Creates UI instance in `__init__`
- Uses UI for rendering and input handling

## Key Points to Explain
1. The game state is completely reset when starting a new game
2. Card values never change during gameplay
3. The flipped state tracks what the player sees
4. Move counting is based on pairs flipped, not individual cards

## Common Questions and Answers

### 1. "How does the game know when to reset?"
The game resets in two scenarios:
1. When first started: The `__init__` method calls `reset_game()`
2. During gameplay: When the player presses SPACE (handled in game.py Part 2)
   
The `reset_game()` method:
- Generates new card pairs using `utils.generate_cards()`
- Resets all cards to face-down state
- Clears the move counter
- Resets card selection tracking
- Sets game_over to False

### 2. "Why do we need both first_card and second_card?"
We need both variables to implement the memory game mechanics:
- `first_card`: Stores the index of the first card flipped
- `second_card`: Stores the index of the second card flipped

This separation allows us to:
- Track the two-card selection process
- Compare the values of both cards
- Handle the matching logic properly
- Reset the selection after each pair check

### 3. "How are moves counted?"
Moves are counted in the following way:
- Each move represents a pair of cards being flipped
- The counter increments only when the second card is flipped
- Individual card flips don't count as moves
- The counter is reset to 0 when starting a new game
- The final move count is displayed on the game over screen

### 4. "What happens when the game is over?"
When the game is over:
1. The `game_over` flag is set to True
2. This triggers the UI to show the game over screen
3. The screen displays:
   - A "Game Over" message
   - The total number of moves made
   - Instructions to restart
4. The game remains in this state until:
   - The player presses SPACE to restart
   - The player closes the window 