import sys
import pygame

class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create game resources"""
        pygame.init()

        self.screen = pygame.display.set_mode((3840,2160))
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main game loop"""
        while True:
            # Watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()            