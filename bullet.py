import pygame
import math
from pygame.sprite import Sprite
from images import Images

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    
    def __init__(self, ai_game, mouse_x, mouse_y, bullet_type):
        """Initialize the bullet attributes."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = Images()
        self.image_retrieve = self.image.bullets[bullet_type]
        
        # Set starting position from ship
        self.rect = self.image_retrieve.get_rect(center=ai_game.ship.rect.center)
        
        # Calculate direction vector and normalize it
        self._calc_direction(mouse_x, mouse_y)
        
        # Rotate the bullet surface
        self._rotate_bullet()
        
        # Store the bullet speed
        self.speed = self.settings.bullet_speed
        self.delta_time = 0

    def _calc_direction(self, mouse_x, mouse_y):
        """Calculate direction vector and normalize it."""
        self.dir = (mouse_x - self.rect.x, mouse_y - self.rect.y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        
    def _rotate_bullet(self):
        """Rotate the bullet surface."""
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.image_retrieve = pygame.transform.rotate(self.image_retrieve, angle)
        
    def update(self, delta_time):
        """Move the bullet across the screen"""
        # Update position using direction vector and delta time
        self.rect.move_ip(self.dir[0] * self.speed * delta_time, self.dir[1] * self.speed * delta_time)

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.image_retrieve, self.rect)
