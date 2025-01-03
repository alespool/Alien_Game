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
        self.ship_acceleration = 10.0
        self.ship_max_speed = 300.0
        self.ship_friction = 0.9

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 215, 0)

        # Alien settings 
        self.fleet_drop_speed = 10

        # Game speeds up
        self.speedup_scale = 1.1

        # Alien points value increase
        self.score_scale = 1.5

        # Set initial difficulty
        self.difficulty_level = 'Medium'
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game."""
        print(f"Initializing settings for difficulty: {self.difficulty_level}.")
        self.set_difficulty()
        self.fleet_direction = 1 # 1 is right, -1 is left

    def increase_speed(self):
        """Increase the speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self):
        """Set the difficulty for the settings in the game."""
        if self.difficulty_level == "Easy":
            self.ship_speed = 25.0
            self.bullet_speed = 25.0
            self.alien_speed = 15.0
            self.alien_points = 25
        elif self.difficulty_level == "Medium":
            self.ship_speed = 20.0
            self.bullet_speed = 20.0
            self.alien_speed = 25.0
            self.alien_points = 50
        elif self.difficulty_level == "Hard":
            self.ship_speed = 15.0
            self.bullet_speed = 15.0
            self.alien_speed = 35.0
            self.alien_points = 75
