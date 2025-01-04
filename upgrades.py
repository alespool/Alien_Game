import pygame
from pygame.sprite import Sprite


class Upgrade(Sprite):
    UPGRADE_TYPES = {
        'shooting_speed': 'images/upgrades/increase_shooting_speed.png',
        'shield': 'images/upgrades/shield_upgrade.png',
        'extra_life': 'images/upgrades/upgrades/extra_life.png',  # New upgrade
    }

    def __init__(self, upgrade_type, location):
        super().__init__()
        self.upgrade_type = upgrade_type
        self.image = self._load_image(upgrade_type)
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def _load_image(self, upgrade_type):
        """Load the appropriate image for the upgrade type."""
        path = self.UPGRADE_TYPES.get(upgrade_type, 'images/default_upgrade.png')
        return pygame.image.load(path).convert_alpha()

    def apply_upgrade(self, ship):
        """Apply the upgrade effect to the ship."""
        if self.upgrade_type == 'shooting_speed':
            ship.settings.bullet_speed *= 1.2
        elif self.upgrade_type == 'shield':
            ship.settings.shield_strength += 1
        elif self.upgrade_type == 'extra_life':
            ship.stats.lives += 1
