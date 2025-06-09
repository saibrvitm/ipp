# Settings.py Documentation

## Overview
`Settings.py` implements the settings management system through the `Settings` class. It handles game configuration, theme management, and user preferences persistence.

## Class Structure
```python
class Settings:
    def __init__(self):
        self.load_settings()
```

## Core Components

### 1. Settings Storage
**Location**: `Settings.py` - `__init__()`
```python
def __init__(self):
    self.settings_file = "settings.json"
    self.default_settings = {
        "theme": "dark",
        "sound_enabled": True,
        "difficulty": "medium",
        "card_back": "default",
        "particle_effects": True
    }
    self.settings = self.default_settings.copy()
    self.load_settings()
```
- Defines settings file path
- Sets default configuration
- Initializes settings dictionary
- Loads saved settings

### 2. Settings Management Methods

#### 2.1 Load Settings
**Location**: `Settings.py` - `load_settings()`
```python
def load_settings(self):
    try:
        with open(self.settings_file, 'r') as f:
            self.settings = json.load(f)
    except FileNotFoundError:
        self.save_settings()
```
- Attempts to load settings from file
- Creates default file if not found
- Handles file reading errors

#### 2.2 Save Settings
**Location**: `Settings.py` - `save_settings()`
```python
def save_settings(self):
    with open(self.settings_file, 'w') as f:
        json.dump(self.settings, f, indent=4)
```
- Writes settings to file
- Uses JSON format
- Includes indentation for readability

#### 2.3 Get Setting
**Location**: `Settings.py` - `get_setting()`
```python
def get_setting(self, key):
    return self.settings.get(key, self.default_settings.get(key))
```
- Retrieves setting value
- Falls back to default if not found
- Handles missing keys gracefully

#### 2.4 Update Setting
**Location**: `Settings.py` - `update_setting()`
```python
def update_setting(self, key, value):
    self.settings[key] = value
    self.save_settings()
```
- Updates single setting
- Saves changes immediately
- Maintains settings persistence

## Settings Screen Implementation

### 1. Settings UI
**Location**: `Settings.py` - `SettingsScreen` class
```python
class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = Settings()
        self.setup_ui()
```

### 2. UI Components

#### 2.1 Theme Selection
```python
def setup_theme_selector(self):
    theme_layout = QHBoxLayout()
    theme_label = QLabel("Theme:")
    self.theme_combo = QComboBox()
    self.theme_combo.addItems(["dark", "light", "blue"])
    self.theme_combo.currentTextChanged.connect(self.update_theme)
    theme_layout.addWidget(theme_label)
    theme_layout.addWidget(self.theme_combo)
```
- Dropdown for theme selection
- Real-time theme updates
- Horizontal layout for label and selector

#### 2.2 Sound Toggle
```python
def setup_sound_toggle(self):
    sound_layout = QHBoxLayout()
    sound_label = QLabel("Sound:")
    self.sound_checkbox = QCheckBox()
    self.sound_checkbox.setChecked(self.settings.get_setting("sound_enabled"))
    self.sound_checkbox.stateChanged.connect(self.toggle_sound)
    sound_layout.addWidget(sound_label)
    sound_layout.addWidget(self.sound_checkbox)
```
- Checkbox for sound control
- State persistence
- Event handling for changes

#### 2.3 Difficulty Selection
```python
def setup_difficulty_selector(self):
    diff_layout = QHBoxLayout()
    diff_label = QLabel("Difficulty:")
    self.diff_combo = QComboBox()
    self.diff_combo.addItems(["easy", "medium", "hard"])
    self.diff_combo.currentTextChanged.connect(self.update_difficulty)
    diff_layout.addWidget(diff_label)
    diff_layout.addWidget(self.diff_combo)
```
- Difficulty level selection
- Affects game parameters
- Updates game configuration

### 3. Settings Application

#### 3.1 Theme Application
```python
def update_theme(self, theme):
    self.settings.update_setting("theme", theme)
    self.parent.apply_theme(theme)
```
- Updates theme setting
- Applies theme to UI
- Persists change

#### 3.2 Sound Control
```python
def toggle_sound(self, state):
    self.settings.update_setting("sound_enabled", bool(state))
    self.parent.update_sound_state(bool(state))
```
- Toggles sound state
- Updates game audio
- Saves preference

#### 3.3 Difficulty Update
```python
def update_difficulty(self, difficulty):
    self.settings.update_setting("difficulty", difficulty)
    self.parent.update_difficulty(difficulty)
```
- Changes difficulty level
- Updates game parameters
- Persists setting

## Cross-References

### 1. Game Integration
- Theme affects game appearance
- Sound settings control game audio
- Difficulty impacts game mechanics

### 2. UI Components
- Settings screen layout
- Control elements
- Theme application

### 3. Data Persistence
- JSON file storage
- Settings loading/saving
- Default values management

## Event Flow

### 1. Settings Change
1. User modifies setting
2. Change event triggered
3. Setting updated in memory
4. Change saved to file
5. UI updated accordingly

### 2. Settings Load
1. Application starts
2. Settings file checked
3. Settings loaded or defaults used
4. UI initialized with settings

## Theme System

### 1. Theme Definition
```python
THEMES = {
    "dark": {
        "background": "#2c3e50",
        "text": "#ecf0f1",
        "button": "#34495e"
    },
    "light": {
        "background": "#f5f6fa",
        "text": "#2c3e50",
        "button": "#dcdde1"
    },
    "blue": {
        "background": "#1e3799",
        "text": "#f1f2f6",
        "button": "#4a69bd"
    }
}
```
- Theme color schemes
- Consistent styling
- Easy theme switching

### 2. Theme Application
```python
def apply_theme(self, theme_name):
    theme = THEMES.get(theme_name, THEMES["dark"])
    self.setStyleSheet(f"""
        QWidget {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        QPushButton {{
            background-color: {theme['button']};
            color: {theme['text']};
        }}
    """)
```
- Dynamic style application
- Consistent theming
- Fallback handling 