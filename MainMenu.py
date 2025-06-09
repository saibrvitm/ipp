import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
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
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("Memory Game")
        title.setProperty("class", "title")  # Use the title class for styling
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addStretch() # Push title to top, buttons to center

        # Menu buttons
        button_width = 250  # Slightly wider buttons
        button_height = 60

        # Start Game button
        start_btn = QPushButton("Start Game")
        start_btn.setFixedSize(button_width, button_height)
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)

        # Settings button
        settings_btn = QPushButton("Settings")
        settings_btn.setFixedSize(button_width, button_height)
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn, alignment=Qt.AlignCenter)

        # Scoreboard button
        scoreboard_btn = QPushButton("Scoreboard")
        scoreboard_btn.setFixedSize(button_width, button_height)
        scoreboard_btn.clicked.connect(self.show_scoreboard)
        layout.addWidget(scoreboard_btn, alignment=Qt.AlignCenter)

        # Quit button - Red
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

        layout.addStretch() # Push buttons to center, and leave space at bottom

    def start_game(self):
        self.parent.reset_game()
        self.parent.stacked_widget.setCurrentWidget(self.parent.game_screen)

    def show_settings(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.settings_screen)

    def show_scoreboard(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.scoreboard_screen)

    def quit_game(self):
        sys.exit() 