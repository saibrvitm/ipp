from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
import random
import math

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(4, 12)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 4)  # Reduced speed for slower movement
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0  # Full life
        self.decay = random.uniform(0.005, 0.015)  # Slower decay for longer life

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
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # Show without taking focus
        
        # Animation for fade out
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
        # Clear existing particles and create new ones
        self.particles = [Particle(x, y, color) for _ in range(count)]
        self._opacity = 1.0  # Reset opacity
        self.show()
        self.raise_()
        self.update()  # Force immediate update
        
        # Start fade out after a delay
        QTimer.singleShot(2000, self.start_fade_out)

    def clear_particles(self):
        """Clear all particles."""
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

        # Update and draw particles
        self.particles = [p for p in self.particles if p.update()]
        for particle in self.particles:
            particle.draw(painter)

        # Request another update if we still have particles
        if self.particles:
            self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.parent():
            self.setGeometry(0, 0, self.parent().width(), self.parent().height()) 