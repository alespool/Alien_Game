import math
import pygame


class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        self.original_image = pygame.image.load('images/ships_human.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        from movements import MovementSystem
        self.movement = MovementSystem(self, self.settings)

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update_rotation(self):
        """Update the ship's rotation."""
        self.movement.update_rotation()

    def update_position(self, delta_time):
        """Update the ship's position."""
        self.movement.update_position(delta_time)

    def center_ship(self):
        """Center the ship on the middle of the screen."""
        self.movement.center_entity()

    def apply_upgrade(self, upgrade):
        """Apply an upgrade to the ship."""
        upgrade.apply_upgrade(self)