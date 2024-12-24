class Settings:
    """A class to store all the settings of the game characters"""

    def __init__(self):
        """Initialize the game's settings"""
        
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (65,105,225)

        # Ship settings
        self.ship_speed = 1.5