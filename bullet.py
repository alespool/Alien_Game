import math
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game, mouse_x, mouse_y):
        """Create a bullet object at the ship's current location"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0,0) then move to correct position
        self.original_surface = pygame.Surface( 
                (self.settings.bullet_width, self.settings.bullet_height),
                pygame.SRCALPHA)
        self.original_surface.fill(self.color)
        self.surface = self.original_surface

        # Move the bullet to the starting position
        self.rect = self.surface.get_rect()
        self.rect.center = ai_game.ship.rect.center
        self.floating_point_x, self.floating_point_y = self.rect.center

        # Calculate the angle in radians between the start points and end point
        x_diff = mouse_x - ai_game.ship.rect.centerx
        y_diff = mouse_y - ai_game.ship.rect.centery
        self.angle = math.degrees(math.atan2(-y_diff, x_diff))

        # Rotate and update the rect to math the new surface
        self.surface = pygame.transform.rotate(self.original_surface, self.angle)
        self.rect = self.surface.get_rect(center=self.rect.center)

        # Calculate the velocity of the bullet
        velocity = self.settings.bullet_speed
        self.change_x = math.cos(math.radians(self.angle)) * velocity
        self.change_y = -math.sin(math.radians(self.angle)) * velocity


    def update(self, delta_time):
        """Move the bullet up the screen"""
        # Update the position of the bullet
        self.floating_point_x += self.change_x * delta_time
        self.floating_point_y += self.change_y * delta_time
        
        # Update the rect position
        self.rect.x = int(self.floating_point_x)
        self.rect.y = int(self.floating_point_y)

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)