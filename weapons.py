import pygame
from shot import Shot
import math

class Weapon:
    def __init__(self, damage=1, fire_rate=1.0):
        self.damage = damage
        self.fire_rate = fire_rate
        self.level = 1
        
    def upgrade(self):
        self.level += 1
        self.damage *= 1.2
        self.fire_rate *= 1.2

class SingleShot(Weapon):
    def fire(self, position, direction, speed):
        shot = Shot(position.x, position.y)
        shot.velocity = direction * speed
        shot.damage = self.damage
        return [shot]

class TripleShot(Weapon):
    def fire(self, position, direction, speed):
        shots = []
        angles = [-15, 0, 15]  # Spread angles
        
        for angle in angles:
            shot = Shot(position.x, position.y)
            shot_direction = pygame.Vector2(direction).rotate(angle)
            shot.velocity = shot_direction * speed
            shot.damage = self.damage
            shots.append(shot)
            
        return shots

class SpreadShot(Weapon):
    def fire(self, position, direction, speed):
        shots = []
        num_shots = 9
        spread = 90  # Total spread angle
        
        for i in range(num_shots):
            angle = -spread/2 + (spread/(num_shots-1)) * i
            shot = Shot(position.x, position.y)
            shot_direction = pygame.Vector2(direction).rotate(angle)
            shot.velocity = shot_direction * speed
            shot.damage = self.damage
            shots.append(shot)
            
        return shots

class Missile(Shot):
    def __init__(self, x, y, target=None):
        super().__init__(x, y)
        self.target = target
        self.turn_speed = 200  # Degrees per second
        self.damage = 3
        self.color = (255, 100, 100)  # Reddish color for missiles
        
    def update(self, dt):
        if self.target and self.target.alive():
            # Calculate angle to target
            to_target = self.target.position - self.position
            target_angle = math.degrees(math.atan2(to_target.y, to_target.x))
            current_angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))
            
            # Calculate shortest angle difference
            angle_diff = (target_angle - current_angle + 180) % 360 - 180
            
            # Turn towards target
            turn_amount = min(abs(angle_diff), self.turn_speed * dt)
            if angle_diff < 0:
                turn_amount = -turn_amount
                
            # Update velocity direction
            self.velocity.rotate_ip(turn_amount)
            
        super().update(dt)
        
    def draw(self, screen):
        # Draw missile with a trail
        end_pos = self.position - self.velocity.normalize() * self.radius * 2
        pygame.draw.line(screen, self.color, self.position, end_pos, 3)
        pygame.draw.circle(screen, self.color, self.position, self.radius)

class MissileLauncher(Weapon):
    def __init__(self):
        super().__init__(damage=3, fire_rate=0.5)
        self.cooldown = 5.0  # Base cooldown in seconds
        self.cooldown_timer = 0
        
    def fire(self, position, direction, speed, target=None):
        if self.cooldown_timer <= 0:
            missile = Missile(position.x, position.y, target)
            missile.velocity = direction * speed
            self.cooldown_timer = self.cooldown / self.fire_rate
            return [missile]
        return []
        
    def update(self, dt):
        self.cooldown_timer = max(0, self.cooldown_timer - dt)
        
    def upgrade(self):
        super().upgrade()
        self.cooldown *= 0.9  # Reduce cooldown by 10% per upgrade
