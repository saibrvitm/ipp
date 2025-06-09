# Game.py Documentation

## Overview
`Game.py` implements the core game logic through the `MemoryGame` class. It manages game state, card matching, scoring, and coordinates with the UI for visual updates.

## Class Structure
```python
class MemoryGame:
    def __init__(self, ui_callback):
        self.ui_callback = ui_callback
        self.settings = Settings()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.time = 0
        self.particle_effect = ParticleEffect(self.ui_callback.game_widget)
        self.reset_game()
```

## Core Components

### 1. Game State Management
**Location**: `Game.py` - `reset_game()`
```python
def reset_game(self) -> None:
    self.settings = Settings()
    self.cards = create_card_pairs()
    self.flipped_cards: List[int] = []
    self.matched_pairs: List[int] = []
    self.moves = 0
    self.score = 0
    self.time = 0
    self.is_processing = False
    self.particle_effect.clear_particles()
    self.ui_callback.update_score(self.score)
    self.ui_callback.update_moves(self.moves)
    self.ui_callback.reset_cards()
    self.timer.start(1000)
```
- Initializes all game state variables
- Creates new card pairs
- Resets UI elements
- Starts game timer

### 2. Card Click Handling
**Location**: `Game.py` - `handle_card_click()`
```python
def handle_card_click(self, index: int) -> None:
    if self.is_processing or index in self.flipped_cards or index in self.matched_pairs:
        return

    if not self.flipped_cards:
        self.timer.start(1000)

    self.flipped_cards.append(index)
    self.ui_callback.flip_card(index, self.cards[index], True)

    if len(self.flipped_cards) == 2:
        self.moves += 1
        self.ui_callback.update_moves(self.moves)
        self.is_processing = True

        if self.cards[self.flipped_cards[0]] == self.cards[self.flipped_cards[1]]:
            self.handle_match()
        else:
            self.ui_callback.schedule_card_flip_back(self.flipped_cards)
```
- Validates card click
- Manages card flipping
- Handles matching logic
- Updates game state

### 3. Match Handling
**Location**: `Game.py` - `handle_card_click()` (match section)
```python
if self.cards[self.flipped_cards[0]] == self.cards[self.flipped_cards[1]]:
    self.matched_pairs.extend(self.flipped_cards)
    self.score += 10
    self.ui_callback.update_score(self.score)
    
    for card_index in self.flipped_cards:
        pos = self.ui_callback.get_card_position(card_index)
        card = self.ui_callback.cards[card_index]
        center_x = pos.x() + card.width() // 2
        center_y = pos.y() + card.height() // 2
        self.particle_effect.clear_particles()
        self.particle_effect.emit(center_x, center_y, "#4CAF50", 50)
        self.particle_effect.update()
```
- Updates matched pairs
- Increases score
- Triggers particle effects
- Updates UI

### 4. Timer Management
**Location**: `Game.py` - `update_time()`
```python
def update_time(self) -> None:
    self.time += 1
```
- Increments game time
- Called every second
- Used for score tracking

### 5. Card State Management
**Location**: `Game.py` - `flip_cards_back()`
```python
def flip_cards_back(self) -> None:
    for index in self.flipped_cards:
        self.ui_callback.flip_card(index, self.cards[index], False)
    self.flipped_cards = []
    self.is_processing = False
```
- Resets unmatched cards
- Clears flipped cards list
- Updates UI state

## Game State Variables

### 1. Card Management
```python
self.cards = create_card_pairs()  # List of card symbols
self.flipped_cards: List[int] = []  # Currently flipped cards
self.matched_pairs: List[int] = []  # Successfully matched pairs
```
- Tracks all cards
- Manages card states
- Records matches

### 2. Game Progress
```python
self.moves = 0  # Number of card flips
self.score = 0  # Current score
self.time = 0   # Game duration
```
- Tracks game progress
- Used for scoring
- Monitors performance

### 3. Game State
```python
self.is_processing = False  # Prevents multiple card flips
self.timer = QTimer()      # Game timer
```
- Controls game flow
- Manages timing

## Cross-References

### UI Interactions
1. **Card Flipping**
   - Game: `handle_card_click()`
   - UI: `flip_card()`
   - Effect: Updates card appearance

2. **Score Updates**
   - Game: Score calculation
   - UI: `update_score()`
   - Effect: Updates score display

3. **Move Counting**
   - Game: Move tracking
   - UI: `update_moves()`
   - Effect: Updates moves display

### Particle Effects
1. **Match Effects**
   - Game: `handle_card_click()`
   - ParticleEffect: `emit()`
   - Effect: Visual feedback

2. **Game Completion**
   - Game: Completion check
   - ParticleEffect: Multiple emissions
   - Effect: Celebration animation

## Event Flow

### 1. Card Click Sequence
1. User clicks card
2. `handle_card_click()` validates
3. Card flips via UI
4. If second card:
   - Check for match
   - Update score/moves
   - Show effects
   - Check game completion

### 2. Match Sequence
1. Cards match
2. Update matched pairs
3. Increase score
4. Show particle effects
5. Check for game completion

### 3. Game Completion
1. All pairs matched
2. Stop timer
3. Show celebration effects
4. Prompt for player name
5. Update scoreboard

## Helper Methods

### 1. Card Symbol Access
```python
def get_card_symbol(self, index: int) -> str:
    return self.cards[index]
```
- Returns card symbol
- Used for matching

### 2. Match Checking
```python
def is_card_matched(self, index: int) -> bool:
    return index in self.matched_pairs
```
- Checks card state
- Used for validation 