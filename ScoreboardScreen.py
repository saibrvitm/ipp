import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Settings import Settings

class ScoreboardScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = Settings()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("High Scores")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Scoreboard container
        scoreboard_container = QWidget()
        scoreboard_container.setObjectName("scoreboard_container")
        scoreboard_layout = QVBoxLayout(scoreboard_container)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Rank", "Player Name", "Moves", "Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setShowGrid(True)
        self.table.setAlternatingRowColors(True)
        scoreboard_layout.addWidget(self.table)

        layout.addWidget(scoreboard_container)

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self.parent.stacked_widget.setCurrentWidget(self.parent.main_menu))
        layout.addWidget(back_btn)

        # Load scores
        self.load_scores()

    def load_scores(self):
        scores = self.settings.get_scores()
        self.table.setRowCount(len(scores))
        
        for i, score in enumerate(scores):
            # Rank
            rank_item = QTableWidgetItem(f"#{i+1}")
            rank_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, rank_item)
            
            # Player Name
            name_item = QTableWidgetItem(str(score['name']))
            name_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, name_item)
            
            # Moves
            moves_item = QTableWidgetItem(str(score['moves']))
            moves_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 2, moves_item)
            
            # Time
            time_item = QTableWidgetItem(self.format_time(score['time']))
            time_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, time_item)

    def update_scores(self, player_name: str, moves: int, time: int):
        self.settings.add_score(player_name, moves, time)
        self.load_scores()

    def format_time(self, seconds):
        """Format seconds into MM:SS format."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def on_clear_scores(self):
        """Clear all scores and update the table."""
        self.settings.clear_scores()
        self.load_scores()

    def on_back(self):
        if self.parent:
            self.parent.stacked_widget.setCurrentWidget(self.parent.main_menu) 