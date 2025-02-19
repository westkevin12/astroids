import pygame
from circleshape import CircleShape
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class PowerUp(CircleShape):
    TYPES = ['fire_rate', 'damage', 'triple_shot', 'spread_shot', 'missile', 'shield', 'force_field']
    COLORS = {
        'fire_rate': (255, 165, 0),     # Orange
        'damage': (255, 0, 0),          # Red
        'triple_shot': (0, 255, 0),     # Green
        'spread_shot': (0, 255, 255),   # Cyan
        'missile': (255, 0, 255),       # Magenta
        'shield': (0, 0, 255),          # Blue
        'force_field': (255, 255, 0)    # Yellow
    }
    
    def __init__(self, x, y, powerup_type=None):
        super().__init__(x, y, 15)  # 15 pixel radius for power-ups
        self.type = powerup_type if powerup_type else random.choice(self.TYPES)
        self.color = self.COLORS[self.type]
        self.velocity = pygame.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        
    def update(self, dt):
        new_pos = self.position + self.velocity * dt
        
        # Bounce off screen edges
        if new_pos.x - self.radius <= 0 or new_pos.x + self.radius >= SCREEN_WIDTH:
            self.velocity.x *= -1
        if new_pos.y - self.radius <= 0 or new_pos.y + self.radius >= SCREEN_HEIGHT:
            self.velocity.y *= -1
            
        self.position += self.velocity * dt
