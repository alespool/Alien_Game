import pygame


IMAGES = { 
    'UPGRADES': {'shooting_speed': 'images/upgrades/increase_shooting_speed.png',
                'ship_speed': 'images/upgrades/increase_ship_speed.png',
                'ship_shield': 'images/upgrades/increase_ship_shield.png',
                'missile' : 'images/upgrades/bigger_missile.png'},
    'ALIENS': {'first_alien': 'images/first_alien_cut.png',
                'second_alien': 'images/second_alien_cut.png',
                'third_alien': 'images/third_alien_cut.png'},
    'SHIPS': {'human_ship': 'images/ships_human.png'},
    'BULLETS': {'bullet': 'images/bullets/bullet.png',
                'missile': 'images/bullets/missile.png'},
    'BACKGROUNDS': {'first_background': 'images/first_background_resize.jpg'}, 
}

class Images:
    """Initiate all images for the game."""

    def __init__(self):
        """Initialize the images."""
        self.upgrades = self.load_images(IMAGES['UPGRADES'])
        self.aliens = self.load_images(IMAGES['ALIENS'])
        self.ships = self.load_images(IMAGES['SHIPS'])
        self.bullets = self.load_images(IMAGES['BULLETS'])
        self.backgrounds = self.load_images(IMAGES['BACKGROUNDS'])

    def load_images(self, image_dict):
        """Load all images from a dictionary."""
        images = {}
        for key, value in image_dict.items():
            images[key] = pygame.image.load(value).convert_alpha()
        return images