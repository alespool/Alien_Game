import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/first_alien_cut.png')
        self.rect = self.image.get_rect()

        # Start each new alien at the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if an alien ship has hit the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if (self.rect.right >= screen_rect.right) or (self.rect.left <= 0):
            return True

    def update(self, delta_time):
        """Move the alien ship to the right."""
        self.x += ((self.settings.alien_speed * delta_time)
                   * self.settings.fleet_direction)
        self.rect.x = self.x