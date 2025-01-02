import math
import random
from alien import Alien

class FleetStructure:
    """A class to control the position of the alien fleet."""

    def __init__(self, ai_game):
        """Initialize the relevant parameters."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.aliens = ai_game.aliens

    def create_fleet(self, alien_type):
        """Create the fleet of alien ships."""
        alien = Alien(self, alien_type)
        alien_width, alien_height = alien.rect.size

        fleet_patterns = [
            (self._create_random_fleet, "Random"),
            (self._create_circular_fleet, "Circular"),
            (self._create_spiral_fleet, "Spiral"),
            (self._create_clustered_fleet, "Clustered"),
        ]
        
        # Choose and execute a random pattern
        pattern_func, pattern_name = random.choice(fleet_patterns)
        print(f"Creating fleet pattern: {pattern_name}")  # Debug log
        pattern_func(alien_type, alien_width, alien_height)

    def _create_random_fleet(self, alien_type, alien_width, alien_height):
        """Create a dynamic fleet of alien ships."""

        # Calculate available screen space
        screen_width, screen_height = self.settings.screen_width, self.settings.screen_height
        max_columns = screen_width // (alien_width * 2)  # Max columns based on alien size
        max_rows = screen_height // (alien_height * 3)  # Max rows with vertical spacing

        # Adjust row and column limits for larger ships
        columns = max(5, max_columns - len(self.aliens) // 5)
        rows = max(3, max_rows - len(self.aliens) // 10)

        # Spacing factors for variety
        x_spacing = alien_width + random.randint(alien_width // 2, alien_width)
        y_spacing = alien_height + random.randint(alien_height // 2, alien_height)

        # Start creating aliens in a grid with random gaps
        for row in range(rows):
            for col in range(columns):
                if random.random() > 0.2:  # Skip some positions for randomness
                    x = (alien_width + col * x_spacing) % (screen_width - alien_width)
                    y = (alien_height + row * y_spacing) % (screen_height // 2)
                    self._create_alien(x, y, alien_type)

    def _create_circular_fleet(self, alien_type, alien_width, alien_height):
        """Create a circular pattern for the alien fleet."""
        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 4  # Position fleet in the upper section
        
        max_radius = min(center_x, center_y) - alien_width  # Ensure no aliens go off-screen
        num_circles = 3  # Number of concentric circles
        
        for circle in range(1, num_circles + 1):
            radius = circle * max_radius // num_circles
            num_aliens = 8 * circle  # More aliens in outer circles
            for i in range(num_aliens):
                angle = 2 * math.pi * i / num_aliens
                x = center_x + int(radius * math.cos(angle)) - alien_width // 2
                y = center_y + int(radius * math.sin(angle)) - alien_height // 2
                self._create_alien(x, y, alien_type)

    def _create_spiral_fleet(self, alien_type, alien_width, alien_height):
        """Create a spiral pattern for the alien fleet."""

        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 4  # Position fleet in the upper section
        
        num_aliens = 30  # Total number of aliens in the spiral
        angle_increment = math.pi / 6  # Angle step for each alien
        radius_increment = alien_width // 2  # Distance between spirals

        for i in range(num_aliens):
            angle = i * angle_increment
            radius = i * radius_increment
            x = center_x + int(radius * math.cos(angle)) - alien_width // 2
            y = center_y + int(radius * math.sin(angle)) - alien_height // 2
            
            # Ensure aliens don't go off-screen
            if 0 < x < self.settings.screen_width - alien_width and 0 < y < self.settings.screen_height // 2:
                self._create_alien(x, y, alien_type)

    def _create_clustered_fleet(self, alien_type, alien_width, alien_height):
        """Create clusters of aliens."""
        
        # Number of clusters and aliens per cluster
        num_clusters = 5
        aliens_per_cluster = 6
        
        for cluster in range(num_clusters):
            # Random cluster center within screen bounds
            center_x = random.randint(alien_width * 2, self.settings.screen_width - alien_width * 2)
            center_y = random.randint(alien_height * 2, self.settings.screen_height // 2 - alien_height * 2)
            
            for i in range(aliens_per_cluster):
                # Random position around the cluster center
                offset_x = random.randint(-alien_width, alien_width)
                offset_y = random.randint(-alien_height, alien_height)
                x = center_x + offset_x
                y = center_y + offset_y
                self._create_alien(x, y, alien_type)

    def _create_alien(self, x_position, y_position, alien_type):
        """Create a new alien at the defined x and y positions."""
        new_alien = Alien(self, alien_type)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

