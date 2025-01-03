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
        
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float with the ship's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x_velocity = 0.0
        self.y_velocity = 0.0

        self.angle = 0

        # Direct the ship
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update_rotation(self):
        """Draw the rotated ship at its current location."""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the angle between the ship and the mouse pointer
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90  # Subtract 90 to adjust for image orientation.

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, delta_time):
        """Update the ship's position with smooth movement"""
        acceleration = self.settings.ship_acceleration
        max_speed = self.settings.ship_max_speed
        friction = self.settings.ship_friction

        # Adjust velocities based on movement flags
        if self.moving_right and not self.moving_left:
            self.x_velocity = min(self.x_velocity + acceleration * delta_time, max_speed)
        elif self.moving_left and not self.moving_right:
            self.x_velocity = max(self.x_velocity - acceleration * delta_time, -max_speed)
        else:
            # Apply friction when no horizontal movement is active
            self.x_velocity *= friction

        if self.moving_up and not self.moving_down:
            self.y_velocity = max(self.y_velocity - acceleration * delta_time, -max_speed)
        elif self.moving_down and not self.moving_up:
            self.y_velocity = min(self.y_velocity + acceleration * delta_time, max_speed)
        else:
            # Apply friction when no vertical movement is active
            self.y_velocity *= friction

        # Update positions based on velocities
        self.x += self.x_velocity * delta_time
        self.y += self.y_velocity * delta_time

        # Ensure the ship stays within screen bounds
        if self.rect.right + self.x_velocity > self.screen_rect.right or self.rect.left + self.x_velocity < 0:
            self.x_velocity = 0
        if self.rect.bottom + self.y_velocity > self.screen_rect.bottom or self.rect.top + self.y_velocity < 0:
            self.y_velocity = 0

        self.rect.x = self.x
        self.rect.y = self.y

    # def update(self, delta_time):
    #     """Update the ship's position based on the movement flag"""
    #     if self.moving_right == True and self.rect.right < self.screen_rect.right:
    #         self.x += self.settings.ship_speed * delta_time
    #     if self.moving_left == True and self.rect.left > 0:
    #         self.x -= self.settings.ship_speed * delta_time
    #     if self.moving_up == True and self.rect.top > 0:
    #         self.y -= self.settings.ship_speed * delta_time
    #     if self.moving_down == True and self.rect.bottom <= self.screen_rect.height:
    #         self.y += self.settings.ship_speed * delta_time

    #     # Update the rect object from self.x
    #     self.rect.x = self.x
    #     self.rect.y = self.y

    def center_ship(self):
        """Center the ship on the middle of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)