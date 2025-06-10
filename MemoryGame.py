import sys
import json
import os
import random
import math
from typing import List, Tuple, Dict, Any
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QMessageBox, QInputDialog, QStackedWidget,
    QComboBox, QCheckBox, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import (
    Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal
)
from PyQt5.QtGui import (
    QFont, QColor, QPainter, QPen
)
from ParticleEffect import ParticleEffect
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(4, 12)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 4)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.decay = random.uniform(0.005, 0.015)
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        return self.life > 0
    def draw(self, painter):
        alpha = int(self.life * 255)
        color = QColor(self.color)
        color.setAlpha(alpha)
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(int(self.x), int(self.y), self.size, self.size)
class ParticleEffect(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self._opacity = 1.0
        self.fade_animation = QPropertyAnimation(self, b"opacity")
        self.fade_animation.setDuration(1500)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.finished.connect(self.hide)
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
    def emit(self, x, y, color, count=40):
        self.particles = [Particle(x, y, color) for _ in range(count)]
        self._opacity = 1.0
        self.show()
        self.raise_()
        self.update()
        QTimer.singleShot(2000, self.start_fade_out)
    def clear_particles(self):
        self.particles = []
        self.update()
    def start_fade_out(self):
        self.fade_animation.start()
    def paintEvent(self, event):
        if not self.particles:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self._opacity)
        self.particles = [p for p in self.particles if p.update()]
        for particle in self.particles:
            particle.draw(painter)
        if self.particles:
            self.update()
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height())
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
        title = QLabel("High Scores")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        scoreboard_container = QWidget()
        scoreboard_container.setObjectName("scoreboard_container")
        scoreboard_layout = QVBoxLayout(scoreboard_container)
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
        back_btn = QPushButton("Back to Menu")
        back_btn.clicked.connect(lambda: self.parent.stacked_widget.setCurrentWidget(self.parent.main_menu))
        layout.addWidget(back_btn)
        self.load_scores()
    def load_scores(self):
        scores = self.settings.get_scores()
        self.table.setRowCount(len(scores))
        for i, score in enumerate(scores):
            rank_item = QTableWidgetItem(f"#{i+1}")
            rank_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, rank_item)
            name_item = QTableWidgetItem(str(score['name']))
            name_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, name_item)
            moves_item = QTableWidgetItem(str(score['moves']))
            moves_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 2, moves_item)
            time_item = QTableWidgetItem(self.format_time(score['time']))
            time_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, time_item)
    def update_scores(self, player_name: str, moves: int, time: int):
        self.settings.add_score(player_name, moves, time)
        self.load_scores()
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    def on_clear_scores(self):
        self.settings.clear_scores()
        self.load_scores()
    def on_back(self):
        if self.parent:
            self.parent.stacked_widget.setCurrentWidget(self.parent.main_menu)
class SettingsScreen(QWidget):
    settings_changed = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()
        self.parent = parent
        self.setup_ui()
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        title = QLabel("Settings")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        self.settings_container = QWidget()
        self.update_container_style()
        settings_layout = QVBoxLayout(self.settings_container)
        settings_layout.setSpacing(20)
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
        self.update_container_style()
        self.settings_changed.emit()
class AnimatedElement(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 0.0
        self._y_offset = 50
    def setup_animation(self, delay):
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.slide_anim = QPropertyAnimation(self, b"y_offset")
        self.slide_anim.setDuration(800)
        self.slide_anim.setStartValue(50.0)
        self.slide_anim.setEndValue(0.0)
        self.slide_anim.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(delay, self.start_animation)
    def start_animation(self):
        self.fade_anim.start()
        self.slide_anim.start()
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
    @pyqtProperty(float)
    def y_offset(self):
        return self._y_offset
    @y_offset.setter
    def y_offset(self, value):
        self._y_offset = value
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        super().paintEvent(event)
class AnimatedLabel(QLabel):
    def __init__(self, text, font_size=24, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont('Arial', font_size))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: white;")
        self._opacity = 0.0
        self._y_offset = 50
    def setup_animation(self, delay):
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.slide_anim = QPropertyAnimation(self, b"y_offset")
        self.slide_anim.setDuration(800)
        self.slide_anim.setStartValue(50.0)
        self.slide_anim.setEndValue(0.0)
        self.slide_anim.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(delay, self.start_animation)
    def start_animation(self):
        self.fade_anim.start()
        self.slide_anim.start()
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
    @pyqtProperty(float)
    def y_offset(self):
        return self._y_offset
    @y_offset.setter
    def y_offset(self, value):
        self._y_offset = value
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        super().paintEvent(event)
class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont('Arial', 14))
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self._opacity = 0.0
        self._y_offset = 50
    def setup_animation(self, delay):
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.slide_anim = QPropertyAnimation(self, b"y_offset")
        self.slide_anim.setDuration(800)
        self.slide_anim.setStartValue(50.0)
        self.slide_anim.setEndValue(0.0)
        self.slide_anim.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(delay, self.start_animation)
    def start_animation(self):
        self.fade_anim.start()
        self.slide_anim.start()
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
    @pyqtProperty(float)
    def y_offset(self):
        return self._y_offset
    @y_offset.setter
    def y_offset(self, value):
        self._y_offset = value
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        super().paintEvent(event)
class AnimatedCard(QWidget):
    def __init__(self, symbol, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.symbol = symbol
        self._is_flipped = False
        self._opacity = 0.0
        self._rotation_angle = 0
        self.setStyleSheet("""
            QWidget {
                background-color: #3498db;
                border-radius: 8px;
                border: 2px solid #2980b9;
            }
        """)
    def setup_animation(self, fade_delay, flip_front_delay, flip_back_delay):
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(fade_delay, self.fade_anim.start)
        self.flip_anim_front = QPropertyAnimation(self, b"rotation_angle")
        self.flip_anim_front.setDuration(500)
        self.flip_anim_front.setStartValue(0)
        self.flip_anim_front.setEndValue(180)
        self.flip_anim_front.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(flip_front_delay, self.flip_anim_front.start)
        self.flip_anim_back = QPropertyAnimation(self, b"rotation_angle")
        self.flip_anim_back.setDuration(500)
        self.flip_anim_back.setStartValue(180)
        self.flip_anim_back.setEndValue(360)
        self.flip_anim_back.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(flip_back_delay, self.flip_anim_back.start)
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
    @pyqtProperty(int)
    def rotation_angle(self):
        return self._rotation_angle
    @rotation_angle.setter
    def rotation_angle(self, value):
        self._rotation_angle = value
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self._opacity)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._rotation_angle)
        painter.translate(-self.width() / 2, -self.height() / 2)
        painter.setBrush(QColor("#3498db"))
        painter.setPen(QPen(QColor("#2980b9"), 2))
        painter.drawRoundedRect(self.rect(), 8, 8)
        if self._rotation_angle > 90 and self._rotation_angle < 270:
            painter.setPen(QPen(QColor("white")))
            font = QFont('Arial', 36, QFont.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, self.symbol)
        else:
            painter.setPen(QPen(QColor("white")))
            font = QFont('Arial', 36, QFont.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, "?")
class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._opacity = 1.0  # Initialize opacity
        self._y_offset = 0.0  # Initialize y_offset
        self.setup_ui()
        self.setup_animation()
        if parent:
            parent_geometry = parent.geometry()
            self.setFixedSize(parent_geometry.width(), parent_geometry.height())
            self.move(parent_geometry.x(), parent_geometry.y())
        else:
            screen = QApplication.primaryScreen().geometry()
            self.setFixedSize(1000, 800)
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
            self.move(x, y)
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addStretch()
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(30)  # Add some space between elements
        self.card_grid_layout = QHBoxLayout()
        self.card_grid_layout.setAlignment(Qt.AlignCenter)
        self.card_grid_layout.setSpacing(20)  # Add space between cards
        content_layout.addLayout(self.card_grid_layout)
        self.animated_cards = []
        symbols = ['😀', '😂', '😎', '👍']
        for i, symbol in enumerate(symbols):
            card = AnimatedCard(symbol)
            self.card_grid_layout.addWidget(card)
            self.animated_cards.append(card)
        main_layout.addWidget(content_widget)
        main_layout.addStretch()
    def setup_animation(self):
        base_delay = 500
        for i, card in enumerate(self.animated_cards):
            fade_delay = base_delay + i * 150
            flip_front_delay = fade_delay + 500
            flip_back_delay = flip_front_delay + 500
            card.setup_animation(fade_delay, flip_front_delay, flip_back_delay)
        total_animation_duration = base_delay + 150 * len(self.animated_cards) + 1000
        self.fade_out_anim = QPropertyAnimation(self, b"opacity")
        self.fade_out_anim.setDuration(500)  # 500ms fade out
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.setEasingCurve(QEasingCurve.InOutCubic)
        QTimer.singleShot(total_animation_duration, self.start_fade_out)
    def start_fade_out(self):
        self.fade_out_anim.start()
        QTimer.singleShot(500, self.on_animation_finished)
    def on_animation_finished(self):
        main_window = self.window()
        if main_window and hasattr(main_window, 'show_menu'):
            main_window.show_menu()
            self.hide()
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self._opacity)
        super().paintEvent(event) 
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
        title = QLabel("Memory Game")
        title.setProperty("class", "title")  # Use the title class for styling
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addStretch() # Push title to top, buttons to center
        button_width = 250  # Slightly wider buttons
        button_height = 60
        start_btn = QPushButton("Start Game")
        start_btn.setFixedSize(button_width, button_height)
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        settings_btn = QPushButton("Settings")
        settings_btn.setFixedSize(button_width, button_height)
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn, alignment=Qt.AlignCenter)
        scoreboard_btn = QPushButton("Scoreboard")
        scoreboard_btn.setFixedSize(button_width, button_height)
        scoreboard_btn.clicked.connect(self.show_scoreboard)
        layout.addWidget(scoreboard_btn, alignment=Qt.AlignCenter)
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
class Settings:
    def __init__(self):
        self.settings_file = 'settings.json'
        self.default_settings = {
            'grid_size': 4,
            'sound_enabled': True,
            'dark_mode': False,
            'scores': []
        }
        self.settings = self.load_settings()
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    for key, value in self.default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
            except (json.JSONDecodeError, IOError):
                return self.default_settings.copy()
        else:
            self.save_settings(self.default_settings)
            return self.default_settings.copy()
    def save_settings(self, settings):
        try:
            f = open(self.settings_file, 'w')
            json.dump(settings, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
            f.close()
        except IOError:
            pass  # Handle file write errors silently
    def get_setting(self, key, default=None):
        settings = self.load_settings()
        return settings.get(key, default)
    def set_setting(self, key, value):
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)
        self.settings = settings
    def reset_settings(self):
        self.settings = self.default_settings.copy()
        self.save_settings(self.settings)
    def add_score(self, name: str, moves: int, time: int) -> None:
        scores = self.settings.get('scores', [])
        scores.append({
            'name': name,
            'moves': moves,
            'time': time
        })
        scores.sort(key=lambda x: (x['moves'], x['time']))
        self.settings['scores'] = scores[:10]
        self.save_settings(self.settings)
    def clear_scores(self) -> None:
        self.settings['scores'] = []
        self.save_settings(self.settings)
    def get_scores(self) -> list:
        return self.settings.get('scores', []) 
CARD_SYMBOLS = ['🎮', '🎲', '🎯', '🎨', '🎭', '🎪', '🎫', '🎪', '🎭', '🎪', '🎫', '🎪', 
                '🎮', '🎲', '🎯', '🎨', '🎭', '🎪', '🎫', '🎪', '🎭', '🎪', '🎫', '🎪']
CARD_BACK_COLOR = '#4a90e2'  # Nice blue color
CARD_FRONT_COLOR = '#ffffff'  # White
CARD_SIZE = 100
ANIMATION_DURATION = 500  # milliseconds
def get_grid_size() -> int:
    settings = Settings()
    return settings.get_setting('grid_size', 4)
def create_card_pairs() -> List[str]:
    settings = Settings()
    grid_size = settings.get_setting('grid_size', 4)
    total_cards = grid_size * grid_size
    pairs_needed = total_cards // 2
    if pairs_needed > len(CARD_SYMBOLS):
        symbols = CARD_SYMBOLS * (pairs_needed // len(CARD_SYMBOLS) + 1)
    else:
        symbols = CARD_SYMBOLS
    selected_symbols = random.sample(symbols, pairs_needed)
    cards = selected_symbols * 2
    random.shuffle(cards)
    return cards
def get_card_position(index: int) -> Tuple[int, int]:
    grid_size = get_grid_size()
    row = index // grid_size
    col = index % grid_size
    return (row, col)
def create_card_button(symbol: str) -> QPushButton:
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
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}" 
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
        if self.is_processing or index in self.flipped_cards or index in self.matched_pairs:
            return
        if not self.flipped_cards:
            self.timer.start(1000)
        self.flipped_cards.append(index)
        self.ui_callback.flip_card(index, self.cards[index], True)
        if len(self.flipped_cards) == 2:
            self.moves += 1
            self.ui_callback.update_moves(self.moves)
            self.is_processing = True
            if self.cards[self.flipped_cards[0]] == self.cards[self.flipped_cards[1]]:
                self.matched_pairs.extend(self.flipped_cards)
                self.score += 10
                self.ui_callback.update_score(self.score)
                for card_index in self.flipped_cards:
                    pos = self.ui_callback.get_card_position(card_index)
                    card = self.ui_callback.cards[card_index]
                    center_x = pos.x() + card.width() // 2
                    center_y = pos.y() + card.height() // 2
                    self.particle_effect.clear_particles()  # Clear any existing particles
                    self.particle_effect.emit(center_x, center_y, "#4CAF50", 50)
                    self.particle_effect.update()  # Force immediate update
                self.flipped_cards = []
                self.is_processing = False
                if len(self.matched_pairs) == len(self.cards):
                    self.timer.stop()
                    for _ in range(8):
                        x = random.randint(0, self.ui_callback.game_widget.width())
                        y = random.randint(0, self.ui_callback.game_widget.height())
                        self.particle_effect.emit(x, y, "#FFD700", 60)
                    self.ui_callback.show_game_complete()
            else:
                self.ui_callback.schedule_card_flip_back(self.flipped_cards)
    def flip_cards_back(self) -> None:
        for index in self.flipped_cards:
            self.ui_callback.flip_card(index, self.cards[index], False)
        self.flipped_cards = []
        self.is_processing = False
    def update_time(self) -> None:
        self.time += 1
    def get_card_symbol(self, index: int) -> str:
        return self.cards[index]
    def is_card_matched(self, index: int) -> bool:
        return index in self.matched_pairs 
class MemoryGameUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.setWindowTitle("Memory Game")
        self.setMinimumSize(1000, 800)
        self.cards = []
        self.card_grid = None
        self.game = None
        self.game_screen = None
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background-color: transparent;
                border: none;
            }
        """)
        self.setCentralWidget(self.stacked_widget)
        self.splash_screen = SplashScreen(self)
        self.main_menu = MainMenu(self)
        self.settings_screen = SettingsScreen(self)
        self.scoreboard_screen = ScoreboardScreen(self)
        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.settings_screen)
        self.stacked_widget.addWidget(self.scoreboard_screen)
        self.stacked_widget.setCurrentWidget(self.splash_screen)
        self.apply_theme()
        self.settings_screen.settings_changed.connect(self.on_settings_changed)
        QTimer.singleShot(2000, self.show_main_menu)  # Show main menu after 2 seconds
    @property
    def game_widget(self):
        return self.game_screen
    def get_card_position(self, index: int) -> QPoint:
        if 0 <= index < len(self.cards):
            card = self.cards[index]
            return card.mapTo(self.game_screen, QPoint(0, 0))
        return QPoint(0, 0)
    def setup_game_screen(self):
        if self.game_screen is None:
            self.game_screen = QWidget()
            self.stacked_widget.addWidget(self.game_screen)
            layout = QVBoxLayout(self.game_screen)
            layout.setSpacing(20)
            layout.setContentsMargins(40, 40, 40, 40)
            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(0)  # Remove spacing between items
            header_layout.addStretch()
            self.score_label = QLabel("Score: 0")
            self.score_label.setProperty("class", "subtitle")
            header_layout.addWidget(self.score_label)
            header_layout.addStretch()
            self.moves_label = QLabel("Moves: 0")
            self.moves_label.setProperty("class", "subtitle")
            header_layout.addWidget(self.moves_label)
            header_layout.addStretch()
            layout.addWidget(header)
            grid_container = QWidget()
            grid_container.setObjectName("grid_container")
            self.card_grid = QGridLayout(grid_container)
            self.card_grid.setSpacing(10)
            layout.addWidget(grid_container)
            back_btn = QPushButton("Back to Menu")
            back_btn.clicked.connect(self.show_main_menu)
            layout.addWidget(back_btn)
            self.game = MemoryGame(self)
            self.create_cards()
    def create_cards(self):
        if self.cards:
            for card in self.cards:
                self.card_grid.removeWidget(card)
                card.deleteLater()
            self.cards.clear()
        grid_size = self.settings.get_setting('grid_size', 4)
        card_size = min(100, 1000 // (grid_size + 1))
        for i in range(grid_size * grid_size):
            row, col = divmod(i, grid_size)
            card = create_card_button('?')
            card.setFixedSize(card_size, card_size)
            card.setFont(QFont('Arial', card_size // 2))
            card.clicked.connect(lambda checked, idx=i: self.on_card_clicked(idx))
            self.card_grid.addWidget(card, row, col)
            self.cards.append(card)
    def reset_game(self):
        if not self.game_screen:
            self.setup_game_screen()
        self.create_cards()
        if self.game:
            self.game.reset_game()
        self.stacked_widget.setCurrentWidget(self.game_screen)
    def on_card_clicked(self, index):
        self.game.handle_card_click(index)
    def flip_card(self, index: int, symbol: str, is_front: bool):
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
        self.score_label.setText(f'Score: {score}')
    def update_moves(self, moves: int):
        self.moves_label.setText(f'Moves: {moves}')
    def reset_cards(self):
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
        QTimer.singleShot(ANIMATION_DURATION, self.game.flip_cards_back)
    def show_game_complete(self):
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
        is_dark_mode = self.settings.get_setting('dark_mode', False)
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
        fonts = {
            'title': '72px',
            'heading': '24px',
            'subheading': '20px',
            'body': '16px',
            'subtitle': '24px',
            'small': '14px',
            'button': '16px'
        }
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
            QLabel[class="subtitle"] {{
                font-size: {fonts['subtitle']};
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
            QComboBox::item {{
                color: {colors['text']};
                background-color: {colors['surface']};
                padding: 4px;
                font-size: {fonts['body']};
            }}
            QComboBox::item:selected {{
                background-color: {colors['primary']};
                color: white;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {colors['surface']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                selection-background-color: {colors['primary']};
                selection-color: white;
                font-size: {fonts['body']};
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
        self.setStyleSheet(base_style)
        self.stacked_widget.setStyleSheet("QStackedWidget { background-color: transparent; }")
        if hasattr(self, 'settings_screen'):
            self.settings_screen.setStyleSheet("")
        if hasattr(self, 'scoreboard_screen'):
            self.scoreboard_screen.setStyleSheet("")
        if hasattr(self, 'main_menu'):
            self.main_menu.setStyleSheet("")
        if self.game_screen is not None:
            for widget in self.game_screen.findChildren(QWidget):
                if widget.objectName() == "grid_container":
                    widget.setStyleSheet(f"""
                        QWidget {{
                            background-color: {colors['surface']};
                            border-radius: 8px;
                            padding: 20px;
                        }}
                    """)
            if hasattr(self, 'score_label'):
                self.score_label.setStyleSheet(f"color: {colors['text']}; font-size: {fonts['body']};")
            if hasattr(self, 'moves_label'):
                self.moves_label.setStyleSheet(f"color: {colors['text']}; font-size: {fonts['body']};")
        for widget in self.findChildren(QWidget):
            widget.update()
    def on_settings_changed(self):
        self.settings = Settings()
        self.apply_settings()
        if self.game_screen and self.stacked_widget.currentWidget() == self.game_screen:
            self.reset_game()
    def apply_settings(self):
        self.apply_theme()
        if self.game_screen and self.stacked_widget.currentWidget() == self.game_screen:
            self.create_cards()
            if self.game:
                self.game.reset_game()
        for widget in self.findChildren(QWidget):
            widget.update()
    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        self.main_menu.setFocus()
    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_screen)
        self.settings_screen.setFocus()
    def show_scoreboard(self):
        self.scoreboard_screen.load_scores()
        self.stacked_widget.setCurrentWidget(self.scoreboard_screen)
        self.scoreboard_screen.setFocus()
    def show_game(self):
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