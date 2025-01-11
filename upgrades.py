from pygame.sprite import Sprite

class Drop(Sprite):
    def __init__(self, upgrade_type, location, image_retrieve):
        super().__init__()
        self.upgrade_type = upgrade_type
        self.image = image_retrieve.upgrades[upgrade_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = location

    def apply_upgrade(self, ship):
        """Apply the upgrade effect to the ship."""
        if self.upgrade_type == 'shooting_speed':
            ship.settings.bullet_speed *= 5.0
            ship.settings.bullet_color = (255, 0,0)
        elif self.upgrade_type == 'ship_speed':
            ship.settings.ship_speed += 200
        elif self.upgrade_type == 'ship_shield':
            ship.settings.shield_strength += 1
        elif self.upgrade_type == 'extra_life':
            ship.stats.lives += 1

    def reset_upgrades(self, ship):
        """Reset the upgrades to the default settings."""
        ship.settings.set_difficulty()