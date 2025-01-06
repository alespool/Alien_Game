import pygame
import math
from pygame.sprite import Sprite
from images import Images

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    
    def __init__(self, ai_game, mouse_x, mouse_y, bullet_type):
        """Initialize the missile attributes."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = Images()

        print(bullet_type)
        self.image_retrieve = self.image.bullets[bullet_type]

        # Get starting position from ship
        start_x, start_y = ai_game.ship.rect.center
        self.pos = [float(start_x), float(start_y)]
        
        # Calculate direction vector and normalize it
        self.dir = (mouse_x - start_x, mouse_y - start_y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        
        # Create and rotate the bullet surface
        # self.bullet_type = _bullet_type()
        self.bullet = self.image_retrieve
        
        # Calculate angle and rotate bullet
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        
        # Create rect for positioning
        self.rect = self.bullet.get_rect(center=self.pos)
        
        # Store the bullet speed
        self.speed = self.settings.bullet_speed

    def update(self, delta_time):
        """Move the bullet across the screen"""
        # Update position using direction vector and delta time
        self.pos[0] += self.dir[0] * self.speed * delta_time
        self.pos[1] += self.dir[1] * self.speed * delta_time
        
        # Update rect position
        self.rect.center = (round(self.pos[0]), round(self.pos[1]))

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.bullet, self.rect)
