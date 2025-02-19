import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 0)
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(self.position.x), int(self.position.y)),
                         self.radius)
    
    def update(self, dt):
        self.position += self.velocity * dt
        
        # Destroy shot if it goes off screen
        if (self.position.x < 0 or self.position.x > SCREEN_WIDTH or
            self.position.y < 0 or self.position.y > SCREEN_HEIGHT):
            self.kill()
