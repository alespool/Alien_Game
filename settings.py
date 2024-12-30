class Settings:
    """A class to store all the settings of the game characters"""

    def __init__(self):
        """Initialize the game's settings"""
        
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (65,105,225)

        # Ship settings
        self.ship_speed = 25.0

        # Bullet settings
        self.bullet_speed = 25.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)

        # Alien settings 
        self.alien_speed = 15.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # 1 is right, -1 is left

        # TODO: Check speed with time
        # self.framerate = 60
        # self.deltatime = 1/self.framerate