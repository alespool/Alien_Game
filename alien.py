import math
import pygame
import random
from pygame.sprite import Sprite
from images import Images

class Alien(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game, alien_type=1):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.ai_game = ai_game
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
        self.spawn_aliens()

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def update(self, delta_time):
        
        self.rect.x += self.x_speed * delta_time
        self.rect.y += self.y_speed * delta_time       
        
        dir_x, dir_y = self.ai_game.ship.movement.x - self.rect.x, self.ai_game.ship.movement.y - self.rect.y
        self.rotation = (180 / math.pi) * -math.atan2(-dir_x, -dir_y)
        self.image = pygame.transform.rotate(self.image, self.rotation)

        # self.check_edges()

    def spawn_aliens(self):
        """Spawn alien ships at random positions."""
        self.direction = random.randrange(4)
        if self.direction == 0:
            self.rect.x = random.randrange(self.settings.screen_width - self.rect.width)
            self.rect.y = random.randrange(-20, -4)
            self.x_speed = 0
            self.y_speed = random.randrange(1, 8)
        elif self.direction == 1:
            self.rect.x = random.randrange(self.settings.screen_width - self.rect.width)
            self.rect.y = random.randrange(self.settings.screen_height, self.settings.screen_height + 6)
            self.x_speed = 0
            self.y_speed = -random.randrange(1, 8)
        elif self.direction == 2:
            self.rect.x = random.randrange(-20, -4)
            self.rect.y = random.randrange(self.settings.screen_height - self.rect.height)
            self.x_speed = random.randrange(1, 8)
            self.y_speed = 0
        elif self.direction == 3:
            self.rect.x = random.randrange(self.settings.screen_width, self.settings.screen_width + 6)
            self.rect.y = random.randrange(self.settings.screen_height - self.rect.height)
            self.x_speed = -random.randrange(1, 8)
            self.y_speed = 0

    # def _create_alien(self, x_position, y_position, alien_type):
    #     """Create a new alien at the defined x and y positions."""
    #     new_alien = Alien(self, alien_type)
    #     new_alien.x = x_position
    #     new_alien.rect.x = x_position
    #     new_alien.rect.y = y_position
    #     self.aliens.add(new_alien)



    def check_edges(self):
        """Return True if an alien ship has hit the edge of the screen."""

        # Respawn the alien if it goes out of the screen
        if self.direction == 0:
            if self.rect.top > self.settings.screen_height:
                self.spawn_aliens()
        elif self.direction == 1:
            if self.rect.bottom < -10:
                self.spawn_aliens()
        elif self.direction == 2:
            if self.rect.left > self.settings.screen_width:
                self.spawn_aliens()
        elif self.direction == 3:
            if self.rect.right < -10:
                self.spawn_alies()

class BossAlien(Sprite):
    """A class to manage the boss alien"""

    def __init__(self, ai_game):
        """Initialize the boss alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image_retrieve = Images()

        # Load the boss alien image and set its rect attribute
        self.image = self.image_retrieve.boss['boss']
        self.rect = self.image.get_rect()

        # Start the boss alien at the top center
        self.rect.x = self.screen.get_rect().centerx - self.rect.width // 2
        self.rect.y = self.rect.height

        # Store the boss alien's exact position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, delta_time):
        """Keep the boss alien fixed at the top center."""
        self.rect.x = self.screen.get_rect().centerx - self.rect.width // 2
        self.rect.y = self.rect.height

    def check_edges(self):
        """Boss alien does not move, so it never hits the edges."""
        return False