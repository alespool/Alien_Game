class GameStats:
    """A class to track the statistics for Alien Invasion."""

    def __init__(self, ai_game):
       """Initialize the game statistics.""" 
       self.settings = ai_game.settings
       self.reset_stats()

    def reset_stats(self):
        """Initialize the statistics that can change during the game."""
        self.ships_remaining = self.settings.ship_limit