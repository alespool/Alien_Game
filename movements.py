import pygame
import math

class MovementSystem:
    """A physics-based movement system with acceleration, friction, and momentum"""
    
    def __init__(self, entity, settings):
        """Initialize the movement system with an entity to control"""
        self.entity = entity
        self.settings = settings
        self.screen_rect = entity.screen.get_rect()
        
        # Position and velocity tracking
        self.x = float(entity.rect.x)
        self.y = float(entity.rect.y)
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        
        # Rotation tracking
        self.angle = 0
        self.original_image = entity.original_image
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def update_position(self, delta_time):
        """Update position using physics-based movement"""
        # Get movement parameters
        acceleration = self.settings.ship_acceleration
        max_speed = self.settings.ship_speed
        friction = self.settings.ship_friction
        
        # Update horizontal velocity
        if self.moving_right and not self.moving_left:
            self.x_velocity = min(self.x_velocity + acceleration * delta_time, max_speed)
        elif self.moving_left and not self.moving_right:
            self.x_velocity = max(self.x_velocity - acceleration * delta_time, -max_speed)
        else:
            # Apply friction when no horizontal movement is active
            self.x_velocity *= friction
            
        # Update vertical velocity
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
        
        # Handle screen boundaries
        if (self.entity.rect.right + self.x_velocity > self.screen_rect.right or 
            self.entity.rect.left + self.x_velocity < 0):
            self.x_velocity = 0
        if (self.entity.rect.bottom + self.y_velocity > self.screen_rect.bottom or 
            self.entity.rect.top + self.y_velocity < 0):
            self.y_velocity = 0
            
        # Update entity position
        self.entity.rect.x = self.x
        self.entity.rect.y = self.y
        
    def update_rotation(self):
        """Update rotation to face mouse pointer"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Calculate angle between entity and mouse pointer
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90  # Adjust for image orientation
        
        # Rotate image and update rect
        self.entity.image = pygame.transform.rotate(self.original_image, self.angle)
        self.entity.rect = self.entity.image.get_rect(center=(self.x, self.y))
        
    def center_entity(self):
        """Center the entity on the screen"""
        self.entity.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.entity.rect.x)
        self.y = float(self.entity.rect.y)
        # Reset velocities when centering
        self.x_velocity = 0.0
        self.y_velocity = 0.0