import pygame


class Settings:
    """A class to store all the settings of the game characters"""

    def __init__(self):
        """Initialize the game's settings"""
        
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)

        self.bg_image = pygame.image.load('images/first_background_resize.jpg')

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 215, 0)

        # Alien settings 
        self.fleet_drop_speed = 10

        # Game speeds up
        self.speedup_scale = 5.5

        # Set difficulty rates
        self.easy = 0.5
        self.medium = 0.7
        self.hard = 1.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game."""
        self.ship_speed = 25.0
        self.bullet_speed = 25.0
        self.alien_speed = 15.0

        self.fleet_direction = 1 # 1 is right, -1 is left

    def increase_speed(self):
        """Increase the speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

    def set_difficulty(self, level):
        """Set the difficulty for the settings in the game."""
        if level == "Easy":
            self.alien_speed *= self.easy
            self.bullet_speed *= self.easy
        elif level == "Medium":
            self.alien_speed *= self.medium
            self.bullet_speed *= self.medium
        elif level == "Hard":
            self.alien_speed *= self.hard
            self.bullet_speed *= self.hard
 
    def _draw_menu_gradient(self, start_color, end_color):
        """Draw a vertical gradient background."""
        for y in range(self.settings.screen_height):
            r = start_color[0] + (end_color[0] - start_color[0]) * y // self.settings.screen_height
            g = start_color[1] + (end_color[1] - start_color[1]) * y // self.settings.screen_height
            b = start_color[2] + (end_color[2] - start_color[2]) * y // self.settings.screen_height
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.settings.screen_width, y))
