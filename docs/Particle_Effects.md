# Particle Effects Documentation

## Overview
The particle effects system provides visual feedback for game events through animated particles. It's implemented through the `ParticleEffect` class and used throughout the game for various animations.

## Class Structure
```python
class ParticleEffect(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_particles)
```

## Core Components

### 1. Particle Definition
**Location**: `ParticleEffect.py` - `Particle` class
```python
class Particle:
    def __init__(self, x, y, color, velocity, size, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.size = size
        self.lifetime = lifetime
        self.age = 0
```
- Position coordinates
- Color and size
- Movement velocity
- Lifetime management

### 2. Effect Types

#### 2.1 Match Effect
```python
def create_match_effect(self, x, y):
    for _ in range(20):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
        particle = Particle(
            x, y,
            QColor(255, 215, 0),  # Gold color
            velocity,
            random.uniform(2, 4),
            random.uniform(30, 60)
        )
        self.particles.append(particle)
```
- Creates burst of particles
- Random directions
- Gold color scheme
- Variable lifetimes

#### 2.2 Card Flip Effect
```python
def create_flip_effect(self, x, y):
    for _ in range(10):
        angle = random.uniform(-math.pi/4, math.pi/4)
        speed = random.uniform(1, 3)
        velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
        particle = Particle(
            x, y,
            QColor(255, 255, 255),  # White color
            velocity,
            random.uniform(1, 3),
            random.uniform(20, 40)
        )
        self.particles.append(particle)
```
- Subtle particle spread
- White color scheme
- Shorter lifetime
- Limited angle range

### 3. Animation System

#### 3.1 Particle Update
```python
def update_particles(self):
    for particle in self.particles[:]:
        particle.x += particle.velocity[0]
        particle.y += particle.velocity[1]
        particle.age += 1
        
        if particle.age >= particle.lifetime:
            self.particles.remove(particle)
    
    self.update()
```
- Updates particle positions
- Manages particle lifetimes
- Triggers repaint
- Removes expired particles

#### 3.2 Particle Rendering
```python
def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    
    for particle in self.particles:
        alpha = 255 * (1 - particle.age / particle.lifetime)
        color = QColor(particle.color)
        color.setAlpha(alpha)
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(
            int(particle.x - particle.size/2),
            int(particle.y - particle.size/2),
            int(particle.size),
            int(particle.size)
        )
```
- Smooth rendering
- Alpha fade-out
- Circular particles
- Anti-aliased drawing

## Usage Examples

### 1. Card Match
```python
def on_card_match(self, card1, card2):
    if self.settings.get_setting("particle_effects"):
        effect = ParticleEffect(self)
        effect.create_match_effect(
            (card1.x() + card2.x()) / 2,
            (card1.y() + card2.y()) / 2
        )
        effect.start_animation()
```
- Creates effect between matched cards
- Respects settings
- Centers effect
- Starts animation

### 2. Card Flip
```python
def on_card_flip(self, card):
    if self.settings.get_setting("particle_effects"):
        effect = ParticleEffect(self)
        effect.create_flip_effect(card.x(), card.y())
        effect.start_animation()
```
- Creates effect at card position
- Settings check
- Starts animation
- Visual feedback

## Performance Considerations

### 1. Particle Limits
```python
def create_effect(self, x, y, count=20):
    if len(self.particles) > 1000:  # Maximum particle limit
        return
    # Create particles...
```
- Prevents overload
- Maintains performance
- Limits total particles
- Graceful degradation

### 2. Animation Control
```python
def start_animation(self):
    if not self.animation_timer.isActive():
        self.animation_timer.start(16)  # ~60 FPS

def stop_animation(self):
    self.animation_timer.stop()
    self.particles.clear()
```
- Controls frame rate
- Manages resources
- Cleans up particles
- Efficient animation

## Cross-References

### 1. Game Integration
- Card matching
- Card flipping
- Game events
- Settings system

### 2. UI Components
- Card widgets
- Game screen
- Settings screen
- Visual feedback

### 3. Performance
- Frame rate management
- Particle limits
- Resource cleanup
- Animation control

## Event Flow

### 1. Effect Creation
1. Game event occurs
2. Settings checked
3. Effect created
4. Particles initialized
5. Animation started

### 2. Effect Lifecycle
1. Particles created
2. Animation updates
3. Particles move
4. Particles fade
5. Particles removed

## Customization

### 1. Effect Parameters
```python
EFFECT_PARAMS = {
    "match": {
        "count": 20,
        "colors": [(255, 215, 0), (255, 165, 0)],
        "size_range": (2, 4),
        "speed_range": (2, 5),
        "lifetime_range": (30, 60)
    },
    "flip": {
        "count": 10,
        "colors": [(255, 255, 255)],
        "size_range": (1, 3),
        "speed_range": (1, 3),
        "lifetime_range": (20, 40)
    }
}
```
- Configurable parameters
- Effect presets
- Easy customization
- Consistent effects

### 2. Theme Integration
```python
def get_effect_colors(self, effect_type):
    theme = self.settings.get_setting("theme")
    return THEME_EFFECT_COLORS.get(theme, {}).get(effect_type, DEFAULT_COLORS)
```
- Theme-based colors
- Consistent styling
- Fallback colors
- Easy theme changes 