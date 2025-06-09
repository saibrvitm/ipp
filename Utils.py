import random
from typing import List, Tuple
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Settings import Settings

# Game constants
CARD_SYMBOLS = ['🎮', '🎲', '🎯', '🎨', '🎭', '🎪', '🎫', '🎪', '🎭', '🎪', '🎫', '🎪', 
                '🎮', '🎲', '🎯', '🎨', '🎭', '🎪', '🎫', '🎪', '🎭', '🎪', '🎫', '🎪']
CARD_BACK_COLOR = '#4a90e2'  # Nice blue color
CARD_FRONT_COLOR = '#ffffff'  # White
CARD_SIZE = 100
ANIMATION_DURATION = 500  # milliseconds

def get_grid_size() -> int:
    """Get the current grid size from settings."""
    settings = Settings()
    return settings.get_setting('grid_size', 4)

def create_card_pairs() -> List[str]:
    """Create pairs of card symbols based on grid size."""
    settings = Settings()
    grid_size = settings.get_setting('grid_size', 4)
    total_cards = grid_size * grid_size
    pairs_needed = total_cards // 2
    
    # Ensure we have enough symbols
    if pairs_needed > len(CARD_SYMBOLS):
        # If we need more symbols than available, repeat the symbols
        symbols = CARD_SYMBOLS * (pairs_needed // len(CARD_SYMBOLS) + 1)
    else:
        symbols = CARD_SYMBOLS
    
    # Get random symbols for pairs
    selected_symbols = random.sample(symbols, pairs_needed)
    
    # Create pairs
    cards = selected_symbols * 2
    
    # Shuffle the cards
    random.shuffle(cards)
    
    return cards

def get_card_position(index: int) -> Tuple[int, int]:
    """Convert a linear index to grid coordinates."""
    grid_size = get_grid_size()
    row = index // grid_size
    col = index % grid_size
    return (row, col)

def create_card_button(symbol: str) -> QPushButton:
    """Create a styled card button."""
    button = QPushButton('?')
    button.setFixedSize(CARD_SIZE, CARD_SIZE)
    button.setFont(QFont('Arial', 24))
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {CARD_BACK_COLOR};
            color: white;
            border-radius: 8px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: #357abd;
        }}
    """)
    return button

def format_time(seconds: int) -> str:
    """Format seconds into MM:SS format."""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}" 