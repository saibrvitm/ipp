# Memory Game Documentation

## Navigation Guide
1. [Developer Guide](#developer-guide)
   - Architecture Overview
   - Module Interactions
   - User Interaction Flows
   - Data Flow
   - UI Component Map
   - Quick Reference
   - Common Tasks
   - Module Documentation

2. [Game Documentation](#game-documentation)
   - Part 1: Core Game Logic
   - Part 2: Game Mechanics
   - Game Components
   - Game State Management

3. [UI Documentation](#ui-documentation)
   - UI Components
   - Screen Management
   - Theme System
   - User Interface Flow

4. [Utils Documentation](#utils-documentation)
   - Utility Functions
   - Helper Classes
   - Common Operations

---

## Developer Guide
[Previous content from Developer_Guide.md]

---

## Game Documentation

### Part 1: Core Game Logic
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

### Part 2: Game Mechanics
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

---

## UI Documentation
# Understanding ui.py - The Game's Visual Interface

## Overview
`ui.py` handles all visual aspects of the memory game, including rendering the game board, handling user input, and managing the Pygame window. It's the bridge between the game logic and the player.

## Key Components

### UI Class Initialization
```python
class UI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Memory Game")
        self.font = pygame.font.Font(None, 36)
```
This sets up the game window and prepares the rendering environment.

## Core Functions

### 1. Card Rendering
```python
def draw_card(self, pos: Tuple[int, int], value: Optional[int], is_flipped: bool):
    """Draw a single card on the screen."""
    x, y = pos
    if is_flipped:
        # Draw flipped card (blue background with number)
        pygame.draw.rect(self.screen, BLUE, (x, y, CARD_SIZE, CARD_SIZE))
        if value is not None:
            text = self.font.render(str(value), True, WHITE)
            text_rect = text.get_rect(center=(x + CARD_SIZE//2, y + CARD_SIZE//2))
            self.screen.blit(text, text_rect)
    else:
        # Draw unflipped card (gray background)
        pygame.draw.rect(self.screen, GRAY, (x, y, CARD_SIZE, CARD_SIZE))
    
    # Draw card border
    pygame.draw.rect(self.screen, BLACK, (x, y, CARD_SIZE, CARD_SIZE), 2)
```
- Renders individual cards
- Handles both flipped and unflipped states
- Centers numbers on flipped cards
- Adds consistent borders

### 2. Board Rendering
```python
def draw_board(self, cards: List[int], flipped: List[bool]):
    """Draw the entire game board."""
    self.screen.fill(WHITE)
    for i, (value, is_flipped) in enumerate(zip(cards, flipped)):
        pos = get_card_position(i)
        self.draw_card(pos, value, is_flipped)
    pygame.display.flip()
```
- Manages the complete game board
- Uses card positions from utils.py
- Updates the display efficiently

### 3. Game Over Screen
```python
def draw_game_over(self, moves: int):
    """Draw the game over screen."""
    self.screen.fill(WHITE)
    text = self.font.render(f"Game Over! Moves: {moves}", True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    self.screen.blit(text, text_rect)
    
    restart_text = self.font.render("Press SPACE to restart", True, BLACK)
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
    self.screen.blit(restart_text, restart_rect)
    pygame.display.flip()
```
- Displays game completion
- Shows final score
- Provides restart instructions

### 4. Event Handling
```python
def handle_events(self) -> Tuple[bool, Optional[int]]:
    """Handle pygame events and return (quit_game, clicked_card_index)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i in range(GRID_SIZE * GRID_SIZE):
                card_pos = get_card_position(i)
                if is_click_on_card(pos, card_pos):
                    return False, i
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return False, -1  # Signal to restart game
    return False, None
```
- Processes all user input
- Handles window events
- Manages card clicks
- Controls game restart

## How It Connects to Other Files

### Connection to utils.py
- Uses visual constants (colors, dimensions)
- Relies on positioning functions
- Implements click detection

### Connection to game.py
- Provides visual feedback
- Reports user actions
- Manages game state display

## Rendering Pipeline

1. Event Processing
   - Capture user input
   - Detect card clicks
   - Handle window events

2. State Display
   - Clear screen
   - Draw game board
   - Update display

3. Game Over Handling
   - Show completion screen
   - Display statistics
   - Provide restart option

## Key Points to Explain
1. The UI is completely separate from game logic
2. All rendering is handled through Pygame
3. Event handling is non-blocking
4. The display is updated efficiently

## Common Questions to Be Ready For
1. "How does the UI know where to draw the cards?"
2. "What happens when I click a card?"
3. "How is the game over screen displayed?"
4. "Why do we need to flip the display?"

## Performance Considerations
1. Screen updates are minimized
2. Event handling is efficient
3. Text rendering is optimized
4. Display updates are synchronized

### Main Menu
The main menu serves as the entry point to the game, providing navigation to different game modes and settings.

#### Structure
- **Title**: "Memory Game" displayed at the top
- **Buttons**:
  - Start Game: Launches the main game
  - Settings: Opens settings menu
  - Scoreboard: Shows high scores
  - Quit: Exits the application

#### Navigation Flow
1. **Start Game** → `MemoryGame` class
2. **Settings** → `SettingsScreen` class
3. **Scoreboard** → `ScoreboardScreen` class
4. **Quit** → Application exit

#### Styling
- Consistent button styling
- Responsive layout
- Theme-aware design

### Scoreboard Screen
The scoreboard displays player achievements and high scores in a tabular format.

#### Components
- **Title**: "High Scores"
- **Table Structure**:
  - Rank
  - Player Name
  - Moves
  - Time (MM:SS format)

#### Features
- **Score Management**:
  - Automatic sorting
  - Persistent storage
  - Clear functionality
- **UI Elements**:
  - Sortable columns
  - Alternating row colors
  - Responsive layout

### Settings Screen
The settings screen allows players to customize their game experience.

#### Configuration Options
- **Grid Size**:
  - 4x4 (default)
  - 6x6
- **Theme**:
  - Light mode
  - Dark mode

#### Implementation
- **Settings Storage**:
  - Persistent configuration
  - Default values
  - Real-time updates
- **UI Components**:
  - Dropdown menus
  - Checkboxes
  - Group boxes

### Particle Effects
The particle system provides visual feedback for game events.

#### System Components
- **Particle Class**:
  - Position (x, y)
  - Velocity (vx, vy)
  - Color
  - Size
  - Life span
- **Effect Manager**:
  - Particle creation
  - Animation control
  - Cleanup

#### Visual Effects
- **Match Effects**:
  - Particle bursts
  - Color matching
  - Fade out
- **Performance**:
  - Particle pooling
  - Automatic cleanup
  - Frame rate optimization

#### Usage
```python
# Example: Creating a match effect
particle_effect.emit(x, y, color, count=40)
```

---

## Utils Documentation
# Understanding utils.py - The Game's Foundation

## Overview
`utils.py` serves as the foundation of our memory game, providing essential constants and utility functions that other parts of the codebase rely on. Think of it as the game's configuration and helper module. This module is designed to be the single source of truth for game configuration and provides pure, well-typed utility functions.

## Key Components

### Constants
```python
# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Card dimensions
CARD_SIZE = 100  # Square cards
CARD_MARGIN = 15  # Reduced margin

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Game settings
GRID_SIZE = 4  # 4x4 grid
TOTAL_PAIRS = (GRID_SIZE * GRID_SIZE) // 2
FLIP_DELAY = 1000  # milliseconds
```
These constants define the game's visual appearance and behavior. They're used throughout the codebase to maintain consistency and can be easily modified to change the game's appearance or difficulty.

### Core Functions

1. `generate_cards() -> List[int]`
   - Creates the initial set of cards for the game
   - Generates pairs of numbers (1 to TOTAL_PAIRS)
   - Randomly shuffles the cards
   - Used by `game.py` during game initialization
   - Returns a list of integers representing card values

2. `get_card_position(index: int) -> Tuple[int, int]`
   - Calculates the screen position for any card based on its index
   - Used by `ui.py` to draw cards in the correct positions
   - Ensures cards are evenly spaced in a grid
   - Centers the grid in the window
   - Returns a tuple of (x, y) coordinates

3. `is_click_on_card(pos: Tuple[int, int], card_pos: Tuple[int, int]) -> bool`
   - Determines if a mouse click occurred on a specific card
   - Used by `ui.py` to handle user input
   - Essential for game interaction
   - Performs boundary checking
   - Returns True if click is within card bounds

## How It Connects to Other Files

### Connection to game.py
- `generate_cards()` is called during game initialization
- Constants like `GRID_SIZE` and `TOTAL_PAIRS` determine game structure
- `FLIP_DELAY` controls game timing
- Provides the foundation for game state management

### Connection to ui.py
- All visual constants (dimensions, colors) are used for rendering
- `get_card_position()` is used for card placement
- `is_click_on_card()` is used for click detection
- Defines the visual appearance of the game

## Key Points to Explain
1. The module provides a single source of truth for game configuration
2. All functions are pure (no side effects) and well-typed
3. The module is designed to be imported and used by other parts of the game
4. Constants can be easily modified to change game appearance/behavior
5. Functions are focused and have a single responsibility
6. The module is independent and doesn't rely on other game components

## Common Questions and Answers

### 1. "Why are the cards square instead of rectangular?"
The cards are square for several important reasons:
1. Visual Balance:
   - Square cards create a more balanced grid
   - Easier to arrange in a perfect grid
   - More pleasing to the eye

2. Technical Benefits:
   - Simpler positioning calculations
   - Consistent dimensions for both width and height
   - Easier to center numbers on cards

3. Game Design:
   - Square cards are more traditional for memory games
   - Better for displaying numbers
   - More space-efficient in the grid layout

### 2. "How does the card positioning work?"
The card positioning system is carefully designed:
1. Grid Calculation:
   ```python
   total_width = GRID_SIZE * (CARD_SIZE + CARD_MARGIN) - CARD_MARGIN
   total_height = GRID_SIZE * (CARD_SIZE + CARD_MARGIN) - CARD_MARGIN
   ```
   - Calculates total space needed for the grid
   - Accounts for card size and margins
   - Subtracts one margin to avoid extra space

2. Position Calculation:
   ```python
   x = (WINDOW_WIDTH - total_width) // 2 + col * (CARD_SIZE + CARD_MARGIN)
   y = (WINDOW_HEIGHT - total_height) // 2 + row * (CARD_SIZE + CARD_MARGIN)
   ```
   - Centers the grid in the window
   - Uses row and column to calculate position
   - Maintains consistent spacing

### 3. "What happens if we change GRID_SIZE?"
Changing `GRID_SIZE` affects multiple aspects of the game:
1. Game Structure:
   - Changes the number of cards (GRID_SIZE²)
   - Automatically updates TOTAL_PAIRS
   - Affects the grid layout

2. Visual Impact:
   - Adjusts the grid dimensions
   - Changes the number of rows and columns
   - May require window size adjustment

3. Game Difficulty:
   - More cards = harder game
   - More pairs to remember
   - Longer gameplay

### 4. "How are the card pairs generated?"
The card generation process is simple but effective:
1. Pair Creation:
   ```python
   cards = list(range(1, TOTAL_PAIRS + 1)) * 2
   ```
   - Creates numbers from 1 to TOTAL_PAIRS
   - Duplicates each number to create pairs
   - Results in a list of matching pairs

2. Randomization:
   ```python
   random.shuffle(cards)
   ```
   - Randomly arranges all cards
   - Ensures fair distribution
   - Creates unique game layouts

3. Implementation Details:
   - Uses Python's built-in random module
   - Creates a new arrangement each game
   - Maintains perfect pairing

## Code
```python
import random
from typing import List, Tuple

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Card dimensions
CARD_SIZE = 100  # Square cards
CARD_MARGIN = 15  # Reduced margin

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Game settings
GRID_SIZE = 4  # 4x4 grid
TOTAL_PAIRS = (GRID_SIZE * GRID_SIZE) // 2
FLIP_DELAY = 1000  # milliseconds

def generate_cards() -> List[int]:
    """Generate a list of card values for the game."""
    # Create pairs of numbers (1 to TOTAL_PAIRS)
    cards = list(range(1, TOTAL_PAIRS + 1)) * 2
    random.shuffle(cards)
    return cards

def get_card_position(index: int) -> Tuple[int, int]:
    """Calculate the screen position for a card based on its index."""
    row = index // GRID_SIZE
    col = index % GRID_SIZE
    
    total_width = GRID_SIZE * (CARD_SIZE + CARD_MARGIN) - CARD_MARGIN
    total_height = GRID_SIZE * (CARD_SIZE + CARD_MARGIN) - CARD_MARGIN
    
    x = (WINDOW_WIDTH - total_width) // 2 + col * (CARD_SIZE + CARD_MARGIN)
    y = (WINDOW_HEIGHT - total_height) // 2 + row * (CARD_SIZE + CARD_MARGIN)
    
    return (x, y)

def is_click_on_card(pos: Tuple[int, int], card_pos: Tuple[int, int]) -> bool:
    """Check if a click position is within a card's bounds."""
    x, y = pos
    card_x, card_y = card_pos
    return (card_x <= x <= card_x + CARD_SIZE and 
            card_y <= y <= card_y + CARD_SIZE)
```