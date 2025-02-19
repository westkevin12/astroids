import pygame
from circleshape import CircleShape
from constants import (PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, 
                      PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN,
                      SCREEN_WIDTH, SCREEN_HEIGHT)
from weapons import SingleShot, TripleShot, SpreadShot, MissileLauncher

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.shield = 0
        self.force_field = 0
        
        # Weapon system
        self.weapons = {
            'single': SingleShot(),
            'triple': TripleShot(),
            'spread': SpreadShot(),
            'missile': MissileLauncher()
        }
        self.current_weapon = 'single'

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Draw force field if active
        if self.force_field > 0:
            pygame.draw.circle(screen, (100, 100, 255), self.position, self.radius * 1.5, 2)
        
        # Draw shield if active
        if self.shield > 0:
            shield_color = (0, 0, 255)  # Blue shield
            for i in range(self.shield):
                pygame.draw.circle(screen, shield_color, self.position, 
                                 self.radius + (i + 1) * 5, 1)
        
        # Draw ship
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        
        # Draw weapon indicator
        weapon_colors = {
            'single': (255, 255, 255),  # White
            'triple': (0, 255, 0),      # Green
            'spread': (0, 255, 255),    # Cyan
            'missile': (255, 100, 100)  # Red
        }
        indicator_pos = (self.position.x, self.position.y + self.radius * 2)
        pygame.draw.circle(screen, weapon_colors[self.current_weapon], indicator_pos, 3)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        new_pos = self.position + forward * PLAYER_SPEED * dt
        
        # Check screen boundaries
        if (0 <= new_pos.x <= SCREEN_WIDTH and 
            0 <= new_pos.y <= SCREEN_HEIGHT):
            self.position = new_pos
            
    def apply_powerup(self, powerup):
        if powerup.type == 'fire_rate':
            self.weapons[self.current_weapon].fire_rate *= 1.2
        elif powerup.type == 'damage':
            self.weapons[self.current_weapon].damage *= 1.2
        elif powerup.type == 'triple_shot':
            self.current_weapon = 'triple'
        elif powerup.type == 'spread_shot':
            self.current_weapon = 'spread'
        elif powerup.type == 'missile':
            self.current_weapon = 'missile'
        elif powerup.type == 'shield':
            self.shield = min(self.shield + 1, 3)  # Max 3 shield levels
        elif powerup.type == 'force_field':
            self.force_field = 10.0  # Force field duration in seconds
        
    def shoot(self, target=None):
        if self.shoot_timer <= 0:
            direction = pygame.Vector2(0, 1).rotate(self.rotation)
            weapon = self.weapons[self.current_weapon]
            
            if self.current_weapon == 'missile':
                shots = weapon.fire(self.position, direction, PLAYER_SHOOT_SPEED, target)
            else:
                shots = weapon.fire(self.position, direction, PLAYER_SHOOT_SPEED)
                
            if shots:  # If any shots were fired
                self.shoot_timer = PLAYER_SHOOT_COOLDOWN / weapon.fire_rate
                return shots
        return []

    def take_damage(self):
        if self.force_field > 0:
            return False  # No damage taken
        if self.shield > 0:
            self.shield -= 1
            return False  # No damage taken
        return True  # Damage taken

    def update(self, dt):
        self.shoot_timer = max(0, self.shoot_timer - dt)
        
        # Update force field
        if self.force_field > 0:
            self.force_field = max(0, self.force_field - dt)
            
        # Update missile launcher cooldown
        if self.current_weapon == 'missile':
            self.weapons['missile'].update(dt)
            
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
            
        # Weapon switching
        if keys[pygame.K_1]:
            self.current_weapon = 'single'
        elif keys[pygame.K_2]:
            self.current_weapon = 'triple'
        elif keys[pygame.K_3]:
            self.current_weapon = 'spread'
        elif keys[pygame.K_4]:
            self.current_weapon = 'missile'
