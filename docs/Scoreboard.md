# Scoreboard Documentation

## Overview
The scoreboard system manages player scores, high scores, and score display through the `Scoreboard` class. It provides persistent storage of scores and a user interface for viewing score history.

## Class Structure
```python
class Scoreboard:
    def __init__(self):
        self.scores_file = "scores.json"
        self.scores = self.load_scores()
```

## Core Components

### 1. Score Storage
**Location**: `Scoreboard.py` - `__init__()`
```python
def __init__(self):
    self.scores_file = "scores.json"
    self.scores = {
        "easy": [],
        "medium": [],
        "hard": []
    }
    self.load_scores()
```
- Defines scores file path
- Initializes score categories
- Loads saved scores
- Maintains score history

### 2. Score Management Methods

#### 2.1 Load Scores
**Location**: `Scoreboard.py` - `load_scores()`
```python
def load_scores(self):
    try:
        with open(self.scores_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "easy": [],
            "medium": [],
            "hard": []
        }
```
- Attempts to load scores
- Creates default structure if not found
- Handles file reading errors
- Returns score dictionary

#### 2.2 Save Scores
**Location**: `Scoreboard.py` - `save_scores()`
```python
def save_scores(self):
    with open(self.scores_file, 'w') as f:
        json.dump(self.scores, f, indent=4)
```
- Writes scores to file
- Uses JSON format
- Includes indentation
- Maintains persistence

#### 2.3 Add Score
**Location**: `Scoreboard.py` - `add_score()`
```python
def add_score(self, difficulty, score, time, moves):
    score_entry = {
        "score": score,
        "time": time,
        "moves": moves,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    self.scores[difficulty].append(score_entry)
    self.scores[difficulty].sort(key=lambda x: x["score"], reverse=True)
    self.scores[difficulty] = self.scores[difficulty][:10]  # Keep top 10
    self.save_scores()
```
- Creates score entry
- Adds timestamp
- Sorts by score
- Limits to top 10
- Saves changes

### 3. Scoreboard UI

#### 3.1 UI Setup
**Location**: `Scoreboard.py` - `ScoreboardScreen` class
```python
class ScoreboardScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.scoreboard = Scoreboard()
        self.setup_ui()
```
- Initializes screen
- Creates scoreboard instance
- Sets up UI components

#### 3.2 Difficulty Tabs
```python
def setup_difficulty_tabs(self):
    self.tab_widget = QTabWidget()
    self.tab_widget.addTab(self.create_score_table("easy"), "Easy")
    self.tab_widget.addTab(self.create_score_table("medium"), "Medium")
    self.tab_widget.addTab(self.create_score_table("hard"), "Hard")
```
- Creates tab interface
- Separates by difficulty
- Organizes scores
- Easy navigation

#### 3.3 Score Table
```python
def create_score_table(self, difficulty):
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Rank", "Score", "Time", "Moves"])
    
    scores = self.scoreboard.get_scores(difficulty)
    table.setRowCount(len(scores))
    
    for i, score in enumerate(scores):
        table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
        table.setItem(i, 1, QTableWidgetItem(str(score["score"])))
        table.setItem(i, 2, QTableWidgetItem(score["time"]))
        table.setItem(i, 3, QTableWidgetItem(str(score["moves"])))
```
- Creates score table
- Sets column headers
- Populates with scores
- Displays rank

## Score Calculation

### 1. Base Score
```python
def calculate_base_score(self, time, moves):
    base_score = 1000
    time_penalty = time * 2
    move_penalty = moves * 5
    return max(0, base_score - time_penalty - move_penalty)
```
- Starts with 1000 points
- Applies time penalty
- Applies move penalty
- Ensures non-negative

### 2. Difficulty Multiplier
```python
DIFFICULTY_MULTIPLIERS = {
    "easy": 1.0,
    "medium": 1.5,
    "hard": 2.0
}

def calculate_final_score(self, base_score, difficulty):
    return int(base_score * DIFFICULTY_MULTIPLIERS[difficulty])
```
- Applies difficulty bonus
- Rounds to integer
- Scales score appropriately
- Maintains fairness

## Cross-References

### 1. Game Integration
- Score tracking
- Difficulty levels
- Game completion
- Score submission

### 2. UI Components
- Score display
- High score table
- Difficulty tabs
- Score formatting

### 3. Data Persistence
- JSON file storage
- Score loading/saving
- History management
- Top scores

## Event Flow

### 1. Score Submission
1. Game completed
2. Score calculated
3. Score added to board
4. Scores sorted
5. Changes saved

### 2. Score Display
1. Scoreboard opened
2. Scores loaded
3. Tables populated
4. UI updated

## Scoreboard Features

### 1. Score Sorting
```python
def sort_scores(self, difficulty):
    self.scores[difficulty].sort(key=lambda x: (
        x["score"],
        -x["time"],  # Negative for ascending time
        x["moves"]
    ), reverse=True)
```
- Primary: Score
- Secondary: Time
- Tertiary: Moves
- Descending order

### 2. Score Filtering
```python
def get_top_scores(self, difficulty, limit=10):
    return self.scores[difficulty][:limit]

def get_recent_scores(self, difficulty, limit=5):
    return sorted(
        self.scores[difficulty],
        key=lambda x: x["date"],
        reverse=True
    )[:limit]
```
- Top scores
- Recent scores
- Configurable limits
- Multiple views

### 3. Score Statistics
```python
def get_statistics(self, difficulty):
    scores = self.scores[difficulty]
    if not scores:
        return None
    
    return {
        "average": sum(s["score"] for s in scores) / len(scores),
        "highest": max(s["score"] for s in scores),
        "lowest": min(s["score"] for s in scores),
        "total_games": len(scores)
    }
```
- Average score
- Highest score
- Lowest score
- Game count 