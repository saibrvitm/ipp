import random
from typing import List, Tuple
import pygame

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