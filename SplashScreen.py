from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup
from PyQt5.QtGui import QFont, QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication

class AnimatedElement(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 0.0
        self._y_offset = 50  # Start 50 pixels below final position

    def setup_animation(self, delay):
        """Set up the element's animation."""
        # Fade in animation
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Slide up animation
        self.slide_anim = QPropertyAnimation(self, b"y_offset")
        self.slide_anim.setDuration(800)
        self.slide_anim.setStartValue(50.0)
        self.slide_anim.setEndValue(0.0)
        self.slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Start animations with delay
        QTimer.singleShot(delay, self.start_animation)

    def start_animation(self):
        """Start both animations."""
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
        """Set up the element's animation."""
        # Fade in animation
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Slide up animation
        self.slide_anim = QPropertyAnimation(self, b"y_offset")
        self.slide_anim.setDuration(800)
        self.slide_anim.setStartValue(50.0)
        self.slide_anim.setEndValue(0.0)
        self.slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Start animations with delay
        QTimer.singleShot(delay, self.start_animation)

    def start_animation(self):
        """Start both animations."""
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
        """Set up the element's animation."""
        # Fade in animation
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Slide up animation
        self.slide_anim = QPropertyAnimation(self, b"y_offset")
        self.slide_anim.setDuration(800)
        self.slide_anim.setStartValue(50.0)
        self.slide_anim.setEndValue(0.0)
        self.slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Start animations with delay
        QTimer.singleShot(delay, self.start_animation)

    def start_animation(self):
        """Start both animations."""
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
        # Fade in animation
        self.fade_anim = QPropertyAnimation(self, b"opacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(fade_delay, self.fade_anim.start)

        # Flip animation (front)
        self.flip_anim_front = QPropertyAnimation(self, b"rotation_angle")
        self.flip_anim_front.setDuration(500)
        self.flip_anim_front.setStartValue(0)
        self.flip_anim_front.setEndValue(180)
        self.flip_anim_front.setEasingCurve(QEasingCurve.OutCubic)
        QTimer.singleShot(flip_front_delay, self.flip_anim_front.start)

        # Flip animation (back)
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

        # Apply rotation
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._rotation_angle)
        painter.translate(-self.width() / 2, -self.height() / 2)

        # Draw card background
        painter.setBrush(QColor("#3498db"))
        painter.setPen(QPen(QColor("#2980b9"), 2))
        painter.drawRoundedRect(self.rect(), 8, 8)

        # Draw symbol or back
        if self._rotation_angle > 90 and self._rotation_angle < 270:
            # Show symbol (flipped side)
            painter.setPen(QPen(QColor("white")))
            font = QFont('Arial', 36, QFont.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, self.symbol)
        else:
            # Show card back (front side)
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
        
        # Center the splash screen on the screen
        if parent:
            # Get the parent's geometry
            parent_geometry = parent.geometry()
            # Set size to match parent
            self.setFixedSize(parent_geometry.width(), parent_geometry.height())
            # Move to parent's position
            self.move(parent_geometry.x(), parent_geometry.y())
        else:
            # Get the screen geometry
            screen = QApplication.primaryScreen().geometry()
            # Set a reasonable size
            self.setFixedSize(1000, 800)
            # Calculate center position
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
            self.move(x, y)

    def setup_ui(self):
        """Set up the splash screen UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add top spacer to push content down
        main_layout.addStretch()
        
        # Content container
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(30)  # Add some space between elements

        # Card grid
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
        
        # Add the content widget to main layout
        main_layout.addWidget(content_widget)
        
        # Add bottom spacer to push content up
        main_layout.addStretch()

    def setup_animation(self):
        """Set up the splash screen animation sequence."""
        # Cards animation (staggered)
        base_delay = 500
        for i, card in enumerate(self.animated_cards):
            fade_delay = base_delay + i * 150
            flip_front_delay = fade_delay + 500
            flip_back_delay = flip_front_delay + 500
            card.setup_animation(fade_delay, flip_front_delay, flip_back_delay)

        # Overall splash screen duration and transition
        total_animation_duration = base_delay + 150 * len(self.animated_cards) + 1000
        
        # Create fade out animation
        self.fade_out_anim = QPropertyAnimation(self, b"opacity")
        self.fade_out_anim.setDuration(500)  # 500ms fade out
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.setEasingCurve(QEasingCurve.InOutCubic)
        
        # Schedule the fade out and transition
        QTimer.singleShot(total_animation_duration, self.start_fade_out)

    def start_fade_out(self):
        """Start the fade out animation."""
        self.fade_out_anim.start()
        # Wait for fade out to complete before showing menu
        QTimer.singleShot(500, self.on_animation_finished)

    def on_animation_finished(self):
        """Called when all splash screen animations are finished."""
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