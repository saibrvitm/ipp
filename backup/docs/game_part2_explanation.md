# Understanding game.py (Part 2) - Game Logic and Main Loop

## Overview
This part of `game.py` handles the core game logic and main game loop. It's responsible for processing player actions and managing the game flow.

## Key Components

### Card Click Handler
```python
def handle_card_click(self, card_index: int):
    """Handle a card click event."""
    if self.game_over or self.flipped[card_index]:
        return
    
    if self.first_card is None:
        self.first_card = card_index
        self.flipped[card_index] = True
    elif self.second_card is None:
        self.second_card = card_index
        self.flipped[card_index] = True
        self.moves += 1
        
        # Check for match
        if self.cards[self.first_card] == self.cards[self.second_card]:
            self.first_card = None
            self.second_card = None
            # Check if game is over
            if all(self.flipped):
                self.game_over = True
        else:
            # Wait and flip back
            pygame.time.wait(FLIP_DELAY)
            self.flipped[self.first_card] = False
            self.flipped[self.second_card] = False
            self.first_card = None
            self.second_card = None
```

### Main Game Loop
```python
def run(self):
    """Main game loop."""
    running = True
    while running:
        quit_game, clicked_card = self.ui.handle_events()
        
        if quit_game:
            running = False
        elif clicked_card == -1:  # Restart game
            self.reset_game()
        elif clicked_card is not None:
            self.handle_card_click(clicked_card)
        
        if self.game_over:
            self.ui.draw_game_over(self.moves)
        else:
            self.ui.draw_board(self.cards, self.flipped)
        
        pygame.time.wait(50)  # Cap at 20 FPS
```

## Game Logic Flow

### Card Click Processing
1. First Card Selection
   - Stores card index
   - Flips card face-up
   - Waits for second card

2. Second Card Selection
   - Stores card index
   - Flips card face-up
   - Increments move counter
   - Checks for match

3. Match Checking
   - If match found:
     - Cards stay face-up
     - Check for game completion
   - If no match:
     - Wait for FLIP_DELAY
     - Flip cards back
     - Reset selection

### Main Loop Flow
1. Event Handling
   - Process user input
   - Handle quit/restart
   - Process card clicks

2. State Updates
   - Update game state
   - Process matches
   - Track moves

3. Rendering
   - Show game board
   - Display game over screen
   - Maintain 20 FPS

## How It Connects to Other Files

### Connection to utils.py
- Uses `FLIP_DELAY` for timing
- Relies on game constants

### Connection to ui.py
- Calls UI methods for rendering
- Processes UI events
- Manages game state display

## Key Points to Explain
1. The game loop runs continuously until quit
2. Card matching logic is state-based
3. Game over is determined by all cards being matched
4. The FPS cap ensures smooth gameplay

## Common Questions and Answers

### 1. "How does the card matching work?"
The card matching process works in several steps:
1. First Card Selection:
   - Player clicks a face-down card
   - Card index is stored in `first_card`
   - Card is flipped face-up

2. Second Card Selection:
   - Player clicks another face-down card
   - Card index is stored in `second_card`
   - Card is flipped face-up
   - Move counter increments

3. Match Check:
   - Game compares values at `cards[first_card]` and `cards[second_card]`
   - If values match:
     - Cards stay face-up
     - Selection is reset
     - Game checks if all pairs are found
   - If values don't match:
     - Game waits for `FLIP_DELAY` milliseconds
     - Both cards flip back face-down
     - Selection is reset

### 2. "Why do we need a delay when cards don't match?"
The delay serves several important purposes:
1. Player Experience:
   - Gives players time to see and remember the cards
   - Makes the game more engaging
   - Helps players learn card positions

2. Game Mechanics:
   - Prevents players from clicking too quickly
   - Makes the game more challenging
   - Creates a natural rhythm to gameplay

3. Technical Implementation:
   - Uses `pygame.time.wait(FLIP_DELAY)`
   - `FLIP_DELAY` is set to 1000ms (1 second)
   - Can be adjusted in `utils.py` to change game difficulty

### 3. "How does the game know when to end?"
The game ends through a specific sequence:
1. Match Detection:
   - When a pair is matched, cards stay face-up
   - The `flipped` list tracks all face-up cards

2. Game Over Check:
   - After each successful match, `all(self.flipped)` is checked
   - If all cards are face-up (`True`), `game_over` is set to `True`

3. End Game Display:
   - Main loop detects `game_over` is `True`
   - Switches to game over screen
   - Shows final move count
   - Waits for restart or quit

### 4. "What happens if I click a card that's already flipped?"
The game handles already-flipped cards through a safety check:
1. Initial Check:
   ```python
   if self.game_over or self.flipped[card_index]:
       return
   ```
   - Prevents clicking face-up cards
   - Prevents clicking during game over

2. This prevents:
   - Re-flipping matched pairs
   - Clicking the same card twice
   - Interfering with the current pair selection
   - Breaking the game's state management

3. User Experience:
   - Makes the game more intuitive
   - Prevents accidental moves
   - Maintains game integrity 