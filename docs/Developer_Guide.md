# Memory Game Developer Guide

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Module Interactions](#module-interactions)
3. [User Interaction Flows](#user-interaction-flows)
4. [Data Flow](#data-flow)
5. [UI Component Map](#ui-component-map)
6. [Quick Reference](#quick-reference)
7. [Common Tasks](#common-tasks)
8. [Module Documentation](#module-documentation)

## Architecture Overview

### Core Components
```
Memory Game
├── UI Layer
│   ├── MainMenu (MainMenu.py)
│   ├── Game Screen (Game.py)
│   ├── Settings Screen (Settings.py)
│   └── Scoreboard Screen (Scoreboard.py)
├── Game Logic
│   ├── Card System (Game.py)
│   ├── Scoring System (Scoreboard.py)
│   └── Timer System (Game.py)
├── Visual Effects
│   ├── Particle System (Particle_Effects.py)
│   └── Card Animations (Game.py)
└── Data Management
    ├── Settings Storage (Settings.py)
    └── Score Storage (Scoreboard.py)
```

### Module Roles

1. **MainMenu.py**
   - Entry point UI
   - Navigation hub
   - Screen transitions

2. **Game.py**
   - Core game logic
   - Card management
   - Game state
   - Timer control

3. **Settings.py**
   - User preferences
   - Theme management
   - Configuration storage

4. **Scoreboard.py**
   - Score tracking
   - High score management
   - Statistics

5. **Particle_Effects.py**
   - Visual feedback
   - Animation system
   - Effect management

## Module Interactions

### Data Flow
```
Settings.py ←→ Game.py
    ↑           ↑
    ↓           ↓
Scoreboard.py ←→ UI Components
```

### Event Flow
```
User Action → UI Component → Game Logic → State Update → UI Update
```

### State Management
- **Game State**: Held in `Game.py`
- **User Settings**: Managed by `Settings.py`
- **Scores**: Stored by `Scoreboard.py`
- **UI State**: Distributed across UI components

## User Interaction Flows

### 1. Game Start Flow
```
User clicks "Start Game" → MainMenu.start_game() → Game.reset_game() → Game Screen display
```

### 2. Card Interaction Flow
```
User clicks card → Game.on_card_clicked() → Game.handle_card_click() → 
    Card flip animation → Game.check_match() → 
    If match: Particle effect + Score update
    If no match: Card flip back
```

### 3. Settings Change Flow
```
User changes setting → SettingsScreen.update_setting() → 
    Settings.save_settings() → Game.apply_setting() → UI update
```

### 4. Score Submission Flow
```
Game completion → Game.calculate_score() → 
    Scoreboard.add_score() → Scoreboard.save_scores() → 
    ScoreboardScreen update
```

## Data Flow

### Persistent Data
1. **Settings** (`settings.json`)
   - Theme preferences
   - Sound settings
   - Difficulty level
   - Card back design

2. **Scores** (`scores.json`)
   - High scores by difficulty
   - Game statistics
   - Timestamps

### Runtime Data
1. **Game State**
   - Current cards
   - Timer value
   - Move count
   - Match status

2. **UI State**
   - Active screen
   - Animation states
   - Particle effects

## UI Component Map

### Main Menu
```python
# MainMenu.py
start_btn = QPushButton("Start Game")      # → start_game()
settings_btn = QPushButton("Settings")     # → show_settings()
scoreboard_btn = QPushButton("Scoreboard") # → show_scoreboard()
quit_btn = QPushButton("Quit")            # → quit_game()
```

### Game Screen
```python
# Game.py
card_grid = QGridLayout()                  # → Card placement
timer_label = QLabel()                     # → Time display
moves_label = QLabel()                     # → Move counter
score_label = QLabel()                     # → Score display
```

### Settings Screen
```python
# Settings.py
theme_combo = QComboBox()                  # → update_theme()
sound_checkbox = QCheckBox()               # → toggle_sound()
difficulty_combo = QComboBox()             # → update_difficulty()
```

### Scoreboard Screen
```python
# Scoreboard.py
tab_widget = QTabWidget()                  # → Difficulty tabs
score_table = QTableWidget()               # → Score display
```

## Quick Reference

### Key Components Location

1. **Card System**
   - Card class: `Game.py`
   - Card grid: `Game.setup_card_grid()`
   - Card flipping: `Game.flip_card()`

2. **Scoring System**
   - Score calculation: `Scoreboard.calculate_score()`
   - Score storage: `Scoreboard.add_score()`
   - Score display: `ScoreboardScreen.create_score_table()`

3. **Settings System**
   - Settings storage: `Settings.save_settings()`
   - Theme management: `Settings.apply_theme()`
   - Settings UI: `SettingsScreen.setup_ui()`

4. **Particle Effects**
   - Effect creation: `ParticleEffect.create_effect()`
   - Animation: `ParticleEffect.update_particles()`
   - Rendering: `ParticleEffect.paintEvent()`

## Common Tasks

### 1. Adding a New Card Animation
```python
# In Game.py
def add_card_animation(self, card):
    # 1. Create animation
    animation = QPropertyAnimation(card, b"geometry")
    
    # 2. Set animation properties
    animation.setDuration(300)
    animation.setEasingCurve(QEasingCurve.OutBounce)
    
    # 3. Connect to card
    card.animation = animation
```

### 2. Modifying Themes
```python
# In Settings.py
THEMES = {
    "new_theme": {
        "background": "#your_color",
        "text": "#your_color",
        "button": "#your_color"
    }
}

# Add to theme selector
self.theme_combo.addItem("new_theme")
```

### 3. Adding Difficulty Levels
```python
# In Settings.py
DIFFICULTY_SETTINGS = {
    "new_difficulty": {
        "grid_size": (6, 6),
        "time_limit": 300,
        "score_multiplier": 2.5
    }
}

# In Game.py
def setup_difficulty(self, difficulty):
    settings = DIFFICULTY_SETTINGS[difficulty]
    self.grid_size = settings["grid_size"]
    self.time_limit = settings["time_limit"]
```

### 4. Adding New Particle Effects
```python
# In Particle_Effects.py
def create_new_effect(self, x, y):
    for _ in range(self.effect_count):
        particle = Particle(
            x, y,
            self.effect_color,
            self.calculate_velocity(),
            self.effect_size,
            self.effect_lifetime
        )
        self.particles.append(particle)
```

## Module Documentation

[Previous documentation for each module remains unchanged, but is now organized under this section]

### Game.py
[Previous Game.md content]

### MainMenu.py
[Previous MainMenu.md content]

### Settings.py
[Previous Settings.md content]

### Scoreboard.py
[Previous Scoreboard.md content]

### Particle_Effects.py
[Previous Particle_Effects.md content] 