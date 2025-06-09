# UI.py Documentation

## Overview
`UI.py` is the main entry point of the Memory Game application. It implements the `MemoryGameUI` class which inherits from `QMainWindow` and manages all screens, game state, and UI components.

## Class Structure
```python
class MemoryGameUI(QMainWindow):
    def __init__(self):
        # Initialization code
```

## Core Components

### 1. Main Window Setup
**Location**: `UI.py` - `MemoryGameUI.__init__()`
```python
def __init__(self):
    super().__init__()
    self.settings = Settings()
    self.setWindowTitle("Memory Game")
    self.setMinimumSize(1000, 800)
```
- Sets window title and minimum dimensions
- Initializes settings manager
- Creates main window container

### 2. Screen Management System
**Location**: `UI.py` - `MemoryGameUI.__init__()`
```python
self.stacked_widget = QStackedWidget()
self.stacked_widget.setStyleSheet("""
    QStackedWidget {
        background-color: transparent;
        border: none;
    }
""")
```
- Uses `QStackedWidget` for screen management
- Each screen is a separate widget
- Only one screen visible at a time
- Screens:
  - `SplashScreen`: Initial loading screen
  - `MainMenu`: Main menu interface
  - `SettingsScreen`: Game settings
  - `ScoreboardScreen`: High scores display
  - `game_screen`: Dynamic game board

### 3. Game Screen Components
**Location**: `UI.py` - `setup_game_screen()`

#### 3.1 Header Section
```python
header = QWidget()
header_layout = QHBoxLayout(header)
self.score_label = QLabel("Score: 0")
self.moves_label = QLabel("Moves: 0")
```
- Horizontal layout containing:
  - Score display
  - Moves counter
- Updates through `update_score()` and `update_moves()`

#### 3.2 Card Grid
```python
grid_container = QWidget()
grid_container.setObjectName("grid_container")
self.card_grid = QGridLayout(grid_container)
```
- Dynamic grid layout
- Size based on settings
- Created in `create_cards()`
- Cards are `QPushButton` instances

#### 3.3 Back Button
```python
back_btn = QPushButton("Back to Menu")
back_btn.clicked.connect(self.show_main_menu)
```
- Returns to main menu
- Connected to `show_main_menu()`

### 4. Card Management
**Location**: `UI.py` - `create_cards()`

#### 4.1 Card Creation
```python
card = create_card_button('?')
card.setFixedSize(card_size, card_size)
card.setFont(QFont('Arial', card_size // 2))
card.clicked.connect(lambda checked, idx=i: self.on_card_clicked(idx))
```
- Creates card buttons
- Sets size based on grid
- Connects click events
- Uses `Utils.create_card_button()`

#### 4.2 Card Flipping
**Location**: `UI.py` - `flip_card()`
```python
def flip_card(self, index: int, symbol: str, is_front: bool):
    card = self.cards[index]
    if is_front:
        card.setText(symbol)
        card.setStyleSheet(f"""
            QPushButton {{
                background-color: {CARD_FRONT_COLOR};
                color: black;
                border-radius: 8px;
                border: none;
                font-size: {card.height() // 2}px;
            }}
        """)
```
- Handles card state changes
- Updates card appearance
- Manages card symbols

### 5. Theme System
**Location**: `UI.py` - `apply_theme()`

#### 5.1 Theme Colors
```python
colors = {
    'background': '#2c2c2c' if is_dark_mode else '#f0f2f5',
    'surface': '#404040' if is_dark_mode else '#ffffff',
    'primary': '#4CAF50',
    'text': '#ffffff' if is_dark_mode else '#1a1a1a'
}
```
- Defines color schemes
- Supports light/dark modes
- Applied to all UI elements

#### 5.2 Style Application
```python
base_style = f"""
    QMainWindow, QWidget {{
        background-color: {colors['background']};
    }}
    QLabel {{
        color: {colors['text']};
        font-size: {fonts['body']};
    }}
"""
```
- Applies styles to all widgets
- Updates on theme change
- Maintains consistency

### 6. Event Handlers

#### 6.1 Card Click Handler
**Location**: `UI.py` - `on_card_clicked()`
```python
def on_card_clicked(self, index):
    self.game.handle_card_click(index)
```
- Delegates to game logic
- Triggers card flip
- Updates game state

#### 6.2 Settings Change Handler
**Location**: `UI.py` - `on_settings_changed()`
```python
def on_settings_changed(self):
    self.settings = Settings()
    self.apply_settings()
    if self.game_screen and self.stacked_widget.currentWidget() == self.game_screen:
        self.reset_game()
```
- Reloads settings
- Updates UI
- Resets game if needed

### 7. Screen Navigation
**Location**: `UI.py` - Various methods

#### 7.1 Screen Switching Methods
```python
def show_main_menu(self):
    self.stacked_widget.setCurrentWidget(self.main_menu)

def show_settings(self):
    self.stacked_widget.setCurrentWidget(self.settings_screen)

def show_scoreboard(self):
    self.scoreboard_screen.load_scores()
    self.stacked_widget.setCurrentWidget(self.scoreboard_screen)

def show_game(self):
    self.reset_game()
    self.stacked_widget.setCurrentWidget(self.game_screen)
```
- Manages screen transitions
- Updates current screen
- Handles screen-specific setup

## Cross-References

### UI Elements to Code
1. **Main Menu**
   - Defined in: `MainMenu.py`
   - Connected in: `UI.py` - `__init__()`
   - Navigation: `show_main_menu()`

2. **Game Board**
   - Created in: `setup_game_screen()`
   - Cards in: `create_cards()`
   - Logic in: `Game.py`

3. **Settings Screen**
   - Defined in: `SettingsScreen.py`
   - Connected in: `UI.py` - `__init__()`
   - Updates in: `on_settings_changed()`

4. **Scoreboard**
   - Defined in: `ScoreboardScreen.py`
   - Connected in: `UI.py` - `__init__()`
   - Updates in: `show_game_complete()`

### Event Flow
1. **Card Click**
   - UI: `on_card_clicked()`
   - Game: `handle_card_click()`
   - UI Update: `flip_card()`

2. **Settings Change**
   - Settings Screen: `settings_changed` signal
   - UI: `on_settings_changed()`
   - Theme: `apply_theme()`

3. **Game Completion**
   - Game: Completion check
   - UI: `show_game_complete()`
   - Scoreboard: `update_scores()` 