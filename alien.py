import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/first_alien_cut.png')
        self.rect = self.image.get_rect()

        # Start each new alien at the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)
        