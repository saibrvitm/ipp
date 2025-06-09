import pygame
import random
from typing import List, Tuple, Optional
from utils import *

class MemoryGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Memory Game")
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        
    def reset_game(self):
        """Reset the game state."""
        self.cards = list(range(1, (GRID_SIZE * GRID_SIZE) // 2 + 1)) * 2
        random.shuffle(self.cards)
        self.flipped = [False] * len(self.cards)
        self.moves = 0
        self.game_over = False
        self.first_card = None
        self.second_card = None
        self.waiting_for_second = False
        self.wait_time = 0
        
    def handle_card_click(self, card_index: int):
        """Handle a card click event."""
        if self.waiting_for_second or self.flipped[card_index]:
            return
            
        self.flipped[card_index] = True
        
        if self.first_card is None:
            self.first_card = card_index
        else:
            self.second_card = card_index
            self.moves += 1
            self.waiting_for_second = True
            self.wait_time = pygame.time.get_ticks()
            
            # Check for match
            if self.cards[self.first_card] == self.cards[self.second_card]:
                self.first_card = None
                self.second_card = None
                self.waiting_for_second = False
                
                # Check for game over
                if all(self.flipped):
                    self.game_over = True
            else:
                # Wait before flipping back
                self.wait_time = pygame.time.get_ticks()
    
    def update(self):
        """Update game state."""
        current_time = pygame.time.get_ticks()
        
        # Handle card flipping animation
        if self.waiting_for_second and current_time - self.wait_time > 500:
            self.flipped[self.first_card] = False
            self.flipped[self.second_card] = False
            self.first_card = None
            self.second_card = None
            self.waiting_for_second = False
    
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
    
    def draw_board(self):
        """Draw the entire game board."""
        self.screen.fill(WHITE)
        
        # Draw cards
        for i, (value, is_flipped) in enumerate(zip(self.cards, self.flipped)):
            pos = get_card_position(i)
            self.draw_card(pos, value, is_flipped)
        
        # Draw moves counter
        moves_text = self.font.render(f"Moves: {self.moves}", True, BLACK)
        self.screen.blit(moves_text, (10, 10))
        
        # Draw game over message with overlay
        if self.game_over:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.fill(WHITE)
            overlay.set_alpha(200)  # Semi-transparent
            self.screen.blit(overlay, (0, 0))
            
            # Draw game over text
            font = pygame.font.Font(None, 48)
            text = font.render(f"Game Over! Moves: {self.moves}", True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(text, text_rect)
            
            # Draw restart button
            restart_text = self.font.render("Press SPACE to restart", True, BLACK)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = pygame.mouse.get_pos()
                    for i in range(GRID_SIZE * GRID_SIZE):
                        card_pos = get_card_position(i)
                        if is_click_on_card(pos, card_pos):
                            self.handle_card_click(i)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()
            
            self.update()
            self.draw_board()
            pygame.time.delay(10)  # Cap at 100 FPS
        
        pygame.quit()

if __name__ == "__main__":
    game = MemoryGame()
    game.run() 