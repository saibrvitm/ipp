from typing import List, Optional, Tuple
from Utils import create_card_pairs, get_card_position
from PyQt5.QtCore import QTimer
from ParticleEffect import ParticleEffect
from Settings import Settings
import random

class MemoryGame:
    def __init__(self, ui_callback):
        self.ui_callback = ui_callback
        self.settings = Settings()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.time = 0
        self.particle_effect = ParticleEffect(self.ui_callback.game_widget)
        self.reset_game()

    def reset_game(self) -> None:
        """Reset the game state."""
        # Reload settings to ensure we have the latest values
        self.settings = Settings()
        self.cards = create_card_pairs()
        self.flipped_cards: List[int] = []
        self.matched_pairs: List[int] = []
        self.moves = 0
        self.score = 0
        self.time = 0
        self.is_processing = False
        self.particle_effect.clear_particles()  # Clear any existing particles
        self.ui_callback.update_score(self.score)
        self.ui_callback.update_moves(self.moves)
        self.ui_callback.reset_cards()
        self.timer.start(1000)  # Update every second

    def handle_card_click(self, index: int) -> None:
        """Handle a card click event."""
        if self.is_processing or index in self.flipped_cards or index in self.matched_pairs:
            return

        # Start timer on first card click
        if not self.flipped_cards:
            self.timer.start(1000)

        # Flip the clicked card
        self.flipped_cards.append(index)
        self.ui_callback.flip_card(index, self.cards[index], True)

        # If this is the second card
        if len(self.flipped_cards) == 2:
            self.moves += 1
            self.ui_callback.update_moves(self.moves)
            self.is_processing = True

            # Check for a match
            if self.cards[self.flipped_cards[0]] == self.cards[self.flipped_cards[1]]:
                self.matched_pairs.extend(self.flipped_cards)
                self.score += 10
                self.ui_callback.update_score(self.score)
                
                # Emit particles for matched cards
                for card_index in self.flipped_cards:
                    pos = self.ui_callback.get_card_position(card_index)
                    card = self.ui_callback.cards[card_index]
                    # Use the card's center position
                    center_x = pos.x() + card.width() // 2
                    center_y = pos.y() + card.height() // 2
                    # Force immediate particle effect
                    self.particle_effect.clear_particles()  # Clear any existing particles
                    self.particle_effect.emit(center_x, center_y, "#4CAF50", 50)
                    self.particle_effect.update()  # Force immediate update
                
                self.flipped_cards = []
                self.is_processing = False

                # Check for game completion
                if len(self.matched_pairs) == len(self.cards):
                    self.timer.stop()
                    # Emit celebration particles
                    for _ in range(8):
                        x = random.randint(0, self.ui_callback.game_widget.width())
                        y = random.randint(0, self.ui_callback.game_widget.height())
                        self.particle_effect.emit(x, y, "#FFD700", 60)
                    self.ui_callback.show_game_complete()
            else:
                # Schedule card flip back
                self.ui_callback.schedule_card_flip_back(self.flipped_cards)

    def flip_cards_back(self) -> None:
        """Flip unmatched cards back."""
        for index in self.flipped_cards:
            self.ui_callback.flip_card(index, self.cards[index], False)
        self.flipped_cards = []
        self.is_processing = False

    def update_time(self) -> None:
        """Update the game timer."""
        self.time += 1

    def get_card_symbol(self, index: int) -> str:
        """Get the symbol for a card at the given index."""
        return self.cards[index]

    def is_card_matched(self, index: int) -> bool:
        """Check if a card is part of a matched pair."""
        return index in self.matched_pairs 