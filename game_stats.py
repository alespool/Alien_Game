import json
from pathlib import Path

class GameStats:
    """A class to track the statistics for Alien Invasion."""

    def __init__(self, ai_game):
       """Initialize the game statistics.""" 
       self.settings = ai_game.settings
       self.reset_stats()

       self.high_score = self.get_saved_high_score()

    def get_saved_high_score(self):
        """Gets the highest score ever made from a file, if there is one."""
        path = Path('high_score.json')
        try:
            contents = path.read_text()
            high_score = json.loads(contents)
            return high_score
        except FileNotFoundError:
            return 0

    def reset_stats(self):
        """Initialize the statistics that can change during the game."""
        self.ships_remaining = self.settings.ship_limit
        self.score = 0
        self.level = 0