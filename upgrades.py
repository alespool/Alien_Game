from pygame.sprite import Sprite
from images import Images

class Upgrade(Sprite):
    def __init__(self, upgrade_type, location, image_retrieve):
        super().__init__()
        self.upgrade_type = upgrade_type
        self.image = image_retrieve.upgrades[upgrade_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def apply_upgrade(self, ship):
        """Apply the upgrade effect to the ship."""
        if self.upgrade_type == 'shooting_speed':
            ship.settings.bullet_speed *= 5.2
            ship.settings.bullet_color = (255, 0,0)
        elif self.upgrade_type == 'shield':
            ship.settings.shield_strength += 1
        elif self.upgrade_type == 'extra_life':
            ship.stats.lives += 1
