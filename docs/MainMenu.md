# MainMenu.py Documentation

## Overview
`MainMenu.py` implements the main menu screen through the `MainMenu` class. It provides the primary navigation interface for the game, including buttons for starting the game, accessing settings, viewing scores, and quitting.

## Class Structure
```python
class MainMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
```

## Core Components

### 1. Menu Layout
**Location**: `MainMenu.py` - `setup_ui()`
```python
def setup_ui(self):
    layout = QVBoxLayout(self)
    layout.setSpacing(20)
    layout.setContentsMargins(40, 40, 40, 40)

    # Title
    title = QLabel("Memory Game")
    title.setProperty("class", "title")
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)

    layout.addStretch()  # Push title to top, buttons to center
```
- Creates vertical layout
- Sets spacing and margins
- Adds title label
- Centers content

### 2. Menu Buttons
**Location**: `MainMenu.py` - `setup_ui()`

#### 2.1 Start Game Button
```python
start_btn = QPushButton("Start Game")
start_btn.setFixedSize(button_width, button_height)
start_btn.clicked.connect(self.start_game)
layout.addWidget(start_btn, alignment=Qt.AlignCenter)
```
- Fixed size: 250x60 pixels
- Connected to `start_game()`
- Centered in layout

#### 2.2 Settings Button
```python
settings_btn = QPushButton("Settings")
settings_btn.setFixedSize(button_width, button_height)
settings_btn.clicked.connect(self.show_settings)
layout.addWidget(settings_btn, alignment=Qt.AlignCenter)
```
- Same size as Start Game
- Connected to `show_settings()`
- Centered in layout

#### 2.3 Scoreboard Button
```python
scoreboard_btn = QPushButton("Scoreboard")
scoreboard_btn.setFixedSize(button_width, button_height)
scoreboard_btn.clicked.connect(self.show_scoreboard)
layout.addWidget(scoreboard_btn, alignment=Qt.AlignCenter)
```
- Same size as other buttons
- Connected to `show_scoreboard()`
- Centered in layout

#### 2.4 Quit Button
```python
quit_btn = QPushButton("Quit")
quit_btn.setFont(QFont('Arial', 16))
quit_btn.setFixedSize(button_width, button_height)
quit_btn.setStyleSheet("""
    QPushButton {
        background-color: #e74c3c;
        color: white;
    }
""")
quit_btn.clicked.connect(self.quit_game)
layout.addWidget(quit_btn, alignment=Qt.AlignCenter)
```
- Red styling
- Connected to `quit_game()`
- Centered in layout

### 3. Button Styling
**Location**: `MainMenu.py` - `__init__()`
```python
self.setStyleSheet("""
    * {
        font-size: 45px;               
    }
    QWidget {
        background-color: transparent;
    }
    QPushButton {
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 16px;
        color: white;
        font-weight: bold;
    }
    QPushButton:hover {
        opacity: 0.9;
    }
    QPushButton:pressed {
        opacity: 0.8;
    }
""")
```
- Sets global font size
- Styles all buttons
- Adds hover effects
- Adds press effects

## Navigation Methods

### 1. Start Game
**Location**: `MainMenu.py` - `start_game()`
```python
def start_game(self):
    self.parent.reset_game()
    self.parent.stacked_widget.setCurrentWidget(self.parent.game_screen)
```
- Resets game state
- Shows game screen

### 2. Show Settings
**Location**: `MainMenu.py` - `show_settings()`
```python
def show_settings(self):
    self.parent.stacked_widget.setCurrentWidget(self.parent.settings_screen)
```
- Shows settings screen

### 3. Show Scoreboard
**Location**: `MainMenu.py` - `show_scoreboard()`
```python
def show_scoreboard(self):
    self.parent.stacked_widget.setCurrentWidget(self.parent.scoreboard_screen)
```
- Shows scoreboard screen

### 4. Quit Game
**Location**: `MainMenu.py` - `quit_game()`
```python
def quit_game(self):
    sys.exit()
```
- Exits application

## Cross-References

### UI Navigation
1. **Game Screen**
   - Button: Start Game
   - Method: `start_game()`
   - Target: `game_screen`

2. **Settings Screen**
   - Button: Settings
   - Method: `show_settings()`
   - Target: `settings_screen`

3. **Scoreboard Screen**
   - Button: Scoreboard
   - Method: `show_scoreboard()`
   - Target: `scoreboard_screen`

### Parent Window Integration
1. **Screen Management**
   - Uses parent's `stacked_widget`
   - Controls screen transitions
   - Maintains navigation state

2. **Game Control**
   - Accesses parent's game reset
   - Manages game state
   - Controls game flow

## Event Flow

### 1. Button Click Sequence
1. User clicks button
2. Corresponding method called
3. Parent window notified
4. Screen transition occurs

### 2. Screen Transition
1. Current screen identified
2. Target screen selected
3. Transition executed
4. New screen displayed

## Layout Management

### 1. Vertical Layout
- Title at top
- Buttons in center
- Spacing between elements
- Margins around content

### 2. Button Alignment
- All buttons centered
- Fixed width and height
- Consistent spacing
- Visual hierarchy

### 3. Responsive Design
- Adapts to window size
- Maintains proportions
- Preserves spacing
- Centers content 