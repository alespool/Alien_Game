import math
import pygame
from images import Images

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image_retrieve = Images()

        # Load the ship image and get its rect.
        self.original_image = self.image_retrieve.ships['human_ship']
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        from movements import MovementSystem
        self.movement = MovementSystem(self, self.settings)

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
# TODO: se one update func
    def update_rotation(self):
        """Update the ship's rotation."""
        self.movement.update_rotation()

    def update_position(self, delta_time):
        """Update the ship's position."""
        self.movement.update_position(delta_time)

    def center_ship(self):
        """Center the ship on the middle of the screen."""
        self.movement.center_entity()

    def shield_hit(self):
        """Handle the ship being hit by an alien."""
        if self.settings.shield_strength > 0:
            self.settings.shield_strength -= 1
        else:
            self.settings.ships_left -= 1
            self.center_ship()