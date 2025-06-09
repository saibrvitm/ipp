import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                            QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
                            QMessageBox, QInputDialog, QStackedWidget, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor
from Game import MemoryGame
from Utils import create_card_button, get_grid_size, ANIMATION_DURATION, CARD_BACK_COLOR, CARD_FRONT_COLOR
from Settings import Settings
from SplashScreen import SplashScreen
from MainMenu import MainMenu
from SettingsScreen import SettingsScreen
from ScoreboardScreen import ScoreboardScreen

class MemoryGameUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.setWindowTitle("Memory Game")
        self.setMinimumSize(1000, 800)
        
        # Initialize game-related attributes
        self.cards = []
        self.card_grid = None
        self.game = None
        self.game_screen = None
        
        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background-color: transparent;
                border: none;
            }
        """)
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize screens
        self.splash_screen = SplashScreen(self)
        self.main_menu = MainMenu(self)
        self.settings_screen = SettingsScreen(self)
        self.scoreboard_screen = ScoreboardScreen(self)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.settings_screen)
        self.stacked_widget.addWidget(self.scoreboard_screen)
        
        # Show splash screen first
        self.stacked_widget.setCurrentWidget(self.splash_screen)
        
        # Apply theme immediately after initialization
        self.apply_theme()
        
        # Connect settings screen signals
        self.settings_screen.settings_changed.connect(self.on_settings_changed)
        
        # Start splash screen timer
        QTimer.singleShot(2000, self.show_main_menu)  # Show main menu after 2 seconds

    @property
    def game_widget(self):
        """Return the game screen widget for particle effects."""
        return self.game_screen

    def get_card_position(self, index: int) -> QPoint:
        """Get the position of a card in the game window."""
        if 0 <= index < len(self.cards):
            card = self.cards[index]
            return card.mapTo(self.game_screen, QPoint(0, 0))
        return QPoint(0, 0)

    def setup_game_screen(self):
        """Setup the game screen with current settings."""
        if self.game_screen is None:
            self.game_screen = QWidget()
            self.stacked_widget.addWidget(self.game_screen)
            
            # Create main layout
            layout = QVBoxLayout(self.game_screen)
            layout.setSpacing(20)
            layout.setContentsMargins(40, 40, 40, 40)
            
            # Create header with score and moves
            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(0, 0, 0, 0)
            
            self.score_label = QLabel("Score: 0")
            self.score_label.setProperty("class", "subtitle")
            header_layout.addWidget(self.score_label)
            
            self.moves_label = QLabel("Moves: 0")
            self.moves_label.setProperty("class", "subtitle")
            header_layout.addWidget(self.moves_label)
            
            layout.addWidget(header)
            
            # Create grid container
            grid_container = QWidget()
            grid_container.setObjectName("grid_container")
            self.card_grid = QGridLayout(grid_container)
            self.card_grid.setSpacing(10)
            layout.addWidget(grid_container)
            
            # Create back button
            back_btn = QPushButton("Back to Menu")
            back_btn.clicked.connect(self.show_main_menu)
            layout.addWidget(back_btn)
            
            # Initialize game
            self.game = MemoryGame(self)
            
            # Create initial cards
            self.create_cards()

    def create_cards(self):
        """Create cards based on current grid size."""
        # Clear existing cards
        if self.cards:
            for card in self.cards:
                self.card_grid.removeWidget(card)
                card.deleteLater()
            self.cards.clear()
        
        # Get current grid size
        grid_size = self.settings.get_setting('grid_size', 4)
        card_size = min(100, 1000 // (grid_size + 1))
        
        # Create new cards
        for i in range(grid_size * grid_size):
            row, col = divmod(i, grid_size)
            card = create_card_button('?')
            card.setFixedSize(card_size, card_size)
            card.setFont(QFont('Arial', card_size // 2))
            card.clicked.connect(lambda checked, idx=i: self.on_card_clicked(idx))
            self.card_grid.addWidget(card, row, col)
            self.cards.append(card)

    def reset_game(self):
        """Reset the game state."""
        if not self.game_screen:
            self.setup_game_screen()
        self.create_cards()
        if self.game:
            self.game.reset_game()
        self.stacked_widget.setCurrentWidget(self.game_screen)

    def on_card_clicked(self, index):
        """Handle card click events."""
        self.game.handle_card_click(index)

    def flip_card(self, index: int, symbol: str, is_front: bool):
        """Flip a card to show or hide its symbol."""
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
        else:
            card.setText('?')
            card.setStyleSheet(f"""
                QPushButton {{
                    background-color: {CARD_BACK_COLOR};
                    color: white;
                    border-radius: 8px;
                    border: none;
                    font-size: {card.height() // 2}px;
                }}
                QPushButton:hover {{
                    background-color: #357abd;
                }}
            """)

    def update_score(self, score: int):
        """Update the score display."""
        self.score_label.setText(f'Score: {score}')

    def update_moves(self, moves: int):
        """Update the moves counter."""
        self.moves_label.setText(f'Moves: {moves}')

    def reset_cards(self):
        """Reset all cards to their initial state."""
        for card in self.cards:
            card.setText('?')
            card.setStyleSheet(f"""
                QPushButton {{
                    background-color: {CARD_BACK_COLOR};
                    color: white;
                    border-radius: 8px;
                    border: none;
                    font-size: {card.height() // 2}px;
                }}
                QPushButton:hover {{
                    background-color: #357abd;
                }}
            """)

    def schedule_card_flip_back(self, card_indices):
        """Schedule cards to flip back after a delay."""
        QTimer.singleShot(ANIMATION_DURATION, self.game.flip_cards_back)

    def show_game_complete(self):
        """Show game completion message and prompt for name."""
        name, ok = QInputDialog.getText(
            self, 'Game Complete!',
            'Enter your name for the scoreboard:',
            text='Player'
        )
        
        if ok and name:
            self.settings.add_score(name, self.game.moves, self.game.time)
            self.scoreboard_screen.update_scores(name, self.game.moves, self.game.time)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Congratulations!")
            msg.setText(f"You completed the game in {self.game.moves} moves!\n"
                       f"Final score: {self.game.score}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def apply_theme(self):
        """Apply the current theme to the application."""
        is_dark_mode = self.settings.get_setting('dark_mode', False)
        
        # Define theme colors
        if is_dark_mode:
            colors = {
                'background': '#2c2c2c',
                'surface': '#404040',
                'primary': '#4CAF50',
                'primary_hover': '#45a049',
                'text': '#ffffff',
                'text_secondary': '#b3b3b3',
                'border': '#505050',
                'disabled': '#303030',
                'disabled_text': '#666666',
                'error': '#ff5252',
                'success': '#4CAF50',
                'warning': '#ffc107'
            }
        else:
            colors = {
                'background': '#f0f2f5',
                'surface': '#ffffff',
                'primary': '#4CAF50',
                'primary_hover': '#45a049',
                'text': '#1a1a1a',
                'text_secondary': '#666666',
                'border': '#dddddd',
                'disabled': '#cccccc',
                'disabled_text': '#999999',
                'error': '#ff5252',
                'success': '#4CAF50',
                'warning': '#ffc107'
            }
        
        # Define font sizes
        fonts = {
            'title': '72px',
            'heading': '24px',
            'subheading': '20px',
            'body': '16px',
            'small': '14px',
            'button': '16px'
        }
        
        # Base styles for all widgets
        base_style = f"""
            QMainWindow, QWidget {{
                background-color: {colors['background']};
            }}
            
            QLabel {{
                color: {colors['text']};
                font-size: {fonts['body']};
            }}
            
            QLabel[class="title"] {{
                font-size: {fonts['title']};
                font-weight: bold;
            }}
            
            QLabel[class="heading"] {{
                font-size: {fonts['heading']};
                font-weight: bold;
            }}
            
            QLabel[class="subheading"] {{
                font-size: {fonts['subheading']};
                font-weight: bold;
            }}
            
            QLabel[class="small"] {{
                font-size: {fonts['small']};
            }}
            
            QPushButton {{
                background-color: {colors['primary']};
                color: {colors['text']};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: {fonts['button']};
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {colors['primary_hover']};
            }}
            
            QPushButton:disabled {{
                background-color: {colors['disabled']};
                color: {colors['disabled_text']};
            }}
            
            QGroupBox {{
                background-color: {colors['surface']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 1em;
                font-size: {fonts['subheading']};
            }}
            
            QComboBox {{
                background-color: {colors['surface']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 4px;
                font-size: {fonts['body']};
            }}
            
            QComboBox::drop-down {{
                border: none;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            
            QCheckBox {{
                color: {colors['text']};
                font-size: {fonts['body']};
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {colors['border']};
                border-radius: 3px;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {colors['primary']};
                border-color: {colors['primary']};
            }}
            
            QTableWidget {{
                background-color: {colors['surface']};
                color: {colors['text']};
                gridline-color: {colors['border']};
                font-size: {fonts['body']};
                border: none;
            }}
            
            QTableWidget::item {{
                color: {colors['text']};
                padding: 10px;
            }}
            
            QHeaderView::section {{
                background-color: {colors['surface']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                padding: 10px;
                font-weight: bold;
            }}

            QWidget#scoreboard_container {{
                background-color: {colors['surface']};
                border-radius: 8px;
                padding: 20px;
            }}

            QTableWidget::item:selected {{
                background-color: {colors['primary']};
                color: white;
            }}

            QTableWidget::item:alternate {{
                background-color: {colors['surface']};
            }}

            QScrollBar:vertical {{
                background-color: {colors['surface']};
                width: 12px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {colors['border']};
                min-height: 20px;
                border-radius: 6px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background-color: {colors['surface']};
                height: 12px;
                margin: 0px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {colors['border']};
                min-width: 20px;
                border-radius: 6px;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """
        
        # Apply the style to the main window and all its children
        self.setStyleSheet(base_style)
        self.stacked_widget.setStyleSheet("QStackedWidget { background-color: transparent; }")
        
        # Update specific screens
        if hasattr(self, 'settings_screen'):
            self.settings_screen.setStyleSheet("")
        if hasattr(self, 'scoreboard_screen'):
            self.scoreboard_screen.setStyleSheet("")
        if hasattr(self, 'main_menu'):
            self.main_menu.setStyleSheet("")
            
        # Update game screen if it exists
        if self.game_screen is not None:
            # Update grid container
            for widget in self.game_screen.findChildren(QWidget):
                if widget.objectName() == "grid_container":
                    widget.setStyleSheet(f"""
                        QWidget {{
                            background-color: {colors['surface']};
                            border-radius: 8px;
                            padding: 20px;
                        }}
                    """)
            
            # Update score and moves labels
            if hasattr(self, 'score_label'):
                self.score_label.setStyleSheet(f"color: {colors['text']}; font-size: {fonts['body']};")
            if hasattr(self, 'moves_label'):
                self.moves_label.setStyleSheet(f"color: {colors['text']}; font-size: {fonts['body']};")
        
        # Force update of all child widgets
        for widget in self.findChildren(QWidget):
            widget.update()

    def on_settings_changed(self):
        """Handle settings changes."""
        # Reload settings from file
        self.settings = Settings()
        
        # Apply updated settings
        self.apply_settings()
        
        # If game is running, update it
        if self.game_screen and self.stacked_widget.currentWidget() == self.game_screen:
            self.reset_game()

    def apply_settings(self):
        """Apply all settings from the settings file."""
        # Apply theme first
        self.apply_theme()
        
        # Apply grid size if game is running
        if self.game_screen and self.stacked_widget.currentWidget() == self.game_screen:
            self.create_cards()
            if self.game:
                self.game.reset_game()
        
        # Force update of all widgets
        for widget in self.findChildren(QWidget):
            widget.update()

    def show_main_menu(self):
        """Show the main menu screen."""
        self.stacked_widget.setCurrentWidget(self.main_menu)
        self.main_menu.setFocus()

    def show_settings(self):
        """Show the settings screen."""
        self.stacked_widget.setCurrentWidget(self.settings_screen)
        self.settings_screen.setFocus()

    def show_scoreboard(self):
        """Show the scoreboard screen."""
        self.scoreboard_screen.load_scores()
        self.stacked_widget.setCurrentWidget(self.scoreboard_screen)
        self.scoreboard_screen.setFocus()

    def show_game(self):
        """Show the game screen and reset the game."""
        self.reset_game()
        self.stacked_widget.setCurrentWidget(self.game_screen)
        self.game_screen.setFocus()

def main():
    app = QApplication(sys.argv)
    window = MemoryGameUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 