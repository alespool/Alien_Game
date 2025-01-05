import pygame
from pygame.sprite import Sprite
from images import Images

class Alien(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game, alien_type=1):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image_retrieve = Images()

        # Load the alien image and set its rect attribute
        if alien_type == 1:
            self.image = self.image_retrieve.aliens['first_alien']
        elif alien_type == 2:
            self.image = self.image_retrieve.aliens['second_alien']
        elif alien_type == 3:
            self.image = self.image_retrieve.aliens['third_alien']
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