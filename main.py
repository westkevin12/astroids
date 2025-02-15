import pygame
from constants import *


def main():
    pygame.init()
    print(f"Starting asteroids!\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((0, 0, 0))  # Fill screen with black
        pygame.display.flip()  # Refresh display



if __name__ == "__main__":
    main()
