import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QComboBox, QCheckBox, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from Settings import Settings

class SettingsScreen(QWidget):
    settings_changed = pyqtSignal()  # Signal to notify when settings change
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("Settings")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Settings container
        self.settings_container = QWidget()
        self.update_container_style()  # Set initial style
        settings_layout = QVBoxLayout(self.settings_container)
        settings_layout.setSpacing(20)

        # Grid size settings
        grid_group = QGroupBox("Grid Size")
        grid_group.setFont(QFont('Arial', 16))
        grid_layout = QVBoxLayout()
        
        grid_label = QLabel("Select grid size:")
        grid_label.setFont(QFont('Arial', 14))
        self.grid_size_combo = QComboBox()
        self.grid_size_combo.setFont(QFont('Arial', 14))
        self.grid_size_combo.addItems(['4x4', '6x6'])
        self.grid_size_combo.setCurrentText(f"{self.settings.get_setting('grid_size', 4)}x{self.settings.get_setting('grid_size', 4)}")
        self.grid_size_combo.currentTextChanged.connect(self.on_grid_size_changed)
        
        grid_layout.addWidget(grid_label)
        grid_layout.addWidget(self.grid_size_combo)
        grid_group.setLayout(grid_layout)
        settings_layout.addWidget(grid_group)

        # Theme settings
        theme_group = QGroupBox("Theme")
        theme_group.setFont(QFont('Arial', 16))
        theme_layout = QVBoxLayout()
        
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setFont(QFont('Arial', 14))
        self.dark_mode_checkbox.setChecked(self.settings.get_setting('dark_mode', False))
        self.dark_mode_checkbox.stateChanged.connect(self.on_theme_changed)
        
        theme_layout.addWidget(self.dark_mode_checkbox)
        theme_group.setLayout(theme_layout)
        settings_layout.addWidget(theme_group)

        layout.addWidget(self.settings_container)

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setFont(QFont('Arial', 16))
        back_btn.clicked.connect(lambda: self.parent.stacked_widget.setCurrentWidget(self.parent.main_menu))
        layout.addWidget(back_btn)

    def update_container_style(self):
        is_dark_mode = self.settings.get_setting('dark_mode', False)
        bg_color = '#404040' if is_dark_mode else '#ffffff'
        self.settings_container.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 8px;
                padding: 20px;
            }}
        """)

    def on_grid_size_changed(self, value):
        size = int(value.split('x')[0])
        self.settings.set_setting('grid_size', size)
        self.settings_changed.emit()

    def on_theme_changed(self, state):
        self.settings.set_setting('dark_mode', bool(state))
        self.update_container_style()  # Update style on theme change
        self.settings_changed.emit() 