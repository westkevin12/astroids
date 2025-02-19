import pygame
import sys
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import PowerUp
from titlescreen import TitleScreen

class GameState:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.respawn_timer = 0
        self.respawn_immunity = 0
        
def main():
    pygame.init()
    pygame.font.init()
    print(f"Starting asteroids!\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 30)
    
    # Game states
    title_screen = TitleScreen()
    game_state = GameState()
    current_screen = 'title'
    
    while True:
        dt = clock.tick(60) / 1000
        
        if current_screen == 'title':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                result = title_screen.handle_input(event)
                if result == 'start_game':
                    current_screen = 'game'
                    # Initialize game objects
                    game_state.reset()
                    updatable = pygame.sprite.Group()
                    drawable = pygame.sprite.Group()
                    asteroids = pygame.sprite.Group()
                    shots = pygame.sprite.Group()
                    powerups = pygame.sprite.Group()

                    Asteroid.containers = (asteroids, updatable, drawable)
                    AsteroidField.containers = (updatable,)
                    Shot.containers = (shots, updatable, drawable)
                    PowerUp.containers = (powerups, updatable, drawable)

                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    updatable.add(player)
                    drawable.add(player)

                    asteroidField = AsteroidField()
                elif result == 'quit':
                    return
                    
            title_screen.draw(screen)
            pygame.display.flip()
            
        elif current_screen == 'game':
            # Handle respawn timer
            if game_state.respawn_timer > 0:
                game_state.respawn_timer = max(0, game_state.respawn_timer - dt)
                if game_state.respawn_timer == 0 and not game_state.game_over:
                    # Respawn player
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    updatable.add(player)
                    drawable.add(player)
                    game_state.respawn_immunity = 3.0  # 3 seconds of immunity
            
            # Update immunity timer
            if game_state.respawn_immunity > 0:
                game_state.respawn_immunity = max(0, game_state.respawn_immunity - dt)
                player.force_field = game_state.respawn_immunity  # Use force field effect for immunity
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player in updatable:
                        # Get nearest asteroid for missile targeting
                        nearest_asteroid = None
                        min_distance = float('inf')
                        if player.current_weapon == 'missile':
                            for asteroid in asteroids:
                                dist = (asteroid.position - player.position).length()
                                if dist < min_distance:
                                    min_distance = dist
                                    nearest_asteroid = asteroid
                        
                        # Shoot with target if missile, otherwise normal shot
                        new_shots = player.shoot(nearest_asteroid)
                        if new_shots:
                            shots.add(new_shots)
                    elif event.key == pygame.K_r and game_state.game_over:
                        # Restart game
                        current_screen = 'title'
            
            screen.fill((0, 0, 0))
            updatable.update(dt)

            if player in updatable:  # Only check collisions if player is alive
                for asteroid in asteroids:
                    if player.collides_with(asteroid) and game_state.respawn_immunity <= 0:
                        if player.take_damage():
                            game_state.lives -= 1
                            player.kill()
                            if game_state.lives > 0:
                                game_state.respawn_timer = 2.0  # 2 second respawn delay
                            else:
                                game_state.game_over = True

                    for shot in shots:
                        if asteroid.collides_with(shot):
                            game_state.score += 100 * (asteroid.radius // ASTEROID_MIN_RADIUS)
                            
                            # Chance to spawn power-up when asteroid is destroyed
                            if random.random() < 0.3:  # 30% chance
                                PowerUp(asteroid.position.x, asteroid.position.y)
                            
                            asteroid.split()
                            shot.kill()
                            break
                            
                for powerup in powerups:
                    if player.collides_with(powerup):
                        player.apply_powerup(powerup)
                        powerup.kill()

            for sprite in drawable:
                sprite.draw(screen)
                
            # Draw HUD
            score_text = font.render(f'Score: {game_state.score}', True, (255, 255, 255))
            lives_text = font.render(f'Lives: {game_state.lives}', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))
            
            if player in updatable:
                weapon_text = font.render(f'Weapon: {player.current_weapon.title()}', True, (255, 255, 255))
                screen.blit(weapon_text, (10, 90))
                
                if player.shield > 0:
                    shield_text = font.render(f'Shield: {player.shield}', True, (0, 0, 255))
                    screen.blit(shield_text, (10, 130))
                if player.force_field > 0:
                    force_field_text = font.render(f'Force Field: {player.force_field:.1f}s', True, (100, 100, 255))
                    screen.blit(force_field_text, (10, 170))
                    
            if game_state.game_over:
                game_over_text = font.render('GAME OVER - Press R to Restart', True, (255, 0, 0))
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                screen.blit(game_over_text, text_rect)
            
            pygame.display.flip()

if __name__ == "__main__":
    main()
