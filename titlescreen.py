import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class TitleScreen:
    def __init__(self):
        self.font_large = pygame.font.SysFont('arial', 64)
        self.font_small = pygame.font.SysFont('arial', 32)
        self.selected_option = 0
        self.options = ['Start Game', 'Quit']
        
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Draw title
        title = self.font_large.render('ASTEROIDS', True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        screen.blit(title, title_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font_small.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + i * 50))
            screen.blit(text, rect)
            
        # Draw controls info
        controls = [
            'Controls:',
            'WASD - Move',
            'SPACE - Shoot',
            '1-4 - Switch Weapons',
            'UP/DOWN - Select',
            'ENTER - Confirm'
        ]
        
        for i, line in enumerate(controls):
            text = self.font_small.render(line, True, (200, 200, 200))
            rect = text.get_rect(left=50, top=SCREEN_HEIGHT - 250 + i * 40)
            screen.blit(text, rect)
            
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    return 'start_game'
                elif self.selected_option == 1:
                    return 'quit'
        return None
