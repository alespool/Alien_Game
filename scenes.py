import pygame
from images import Images

class Scene:
    """
    Base class for all scenes in the game

    Attributes:
        None

    Methods:
        __init__: Initializes the scene
        setup: Loads all necessary data
        handle_events: Handles events for the scene
        update: Runs any necessary logic for the scene
        render: Draws the scene to the screen
    """
    def __init__(self):
        """ Initializes the scene """
        pass

    def setup(self):
        """ Loads all necessary data """
        pass

    def handle_events(self, events):
        """ Handles events for the scene """
        pass

    def update(self, dt):
        """ Runs any necessary logic for the scene """
        pass
    
    def render(self, screen):
        """ Draws the scene to the screen """
        pass


class MenuScene(Scene):
    """
    The main menu scene of the game

    Attributes:
        None
    """
    def __init__(self, settings):
        """ Initializes the menu scene """
        super().__init__()
        self.settings = settings

    def setup(self):
        """ Loads all necessary data """
        pass

    def handle_events(self, events):
        """ Handles events for the menu scene """
        pass

    def update(self, dt):
        """ Runs any necessary logic for the menu scene """
        pass
    
    def render(self, screen):
        """ Draws the menu scene to the screen """
        self._draw_menu_gradient(screen, (0, 0, 0), (25, 25, 112)) 

    def _draw_menu_gradient(self, screen, start_color, end_color):
        """Draw a vertical gradient background."""
        for y in range(self.settings.screen_height):
            r = start_color[0] + (end_color[0] - start_color[0]) * y // self.settings.screen_height
            g = start_color[1] + (end_color[1] - start_color[1]) * y // self.settings.screen_height
            b = start_color[2] + (end_color[2] - start_color[2]) * y // self.settings.screen_height
            pygame.draw.line(screen, (r, g, b), (0, y), (self.settings.screen_width, y))


class Inventory(Scene):
    """
    The inventory scene of the game

    Attributes:
        items (list): A list of items in the inventory
        selected_item (int): The index of the selected item
    """
    def __init__(self):
        """ Initializes the inventory scene """
        pass

    def setup(self):
        """ Loads all necessary data """
        pass

    def handle_events(self, events):
        """ Handles events for the inventory scene """
        pass

    def update(self, dt):
        """ Runs any necessary logic for the inventory scene """
        pass
    
    def render(self, screen):
        """ Draws the inventory scene to the screen """
        pass

class BossScene(Scene):
    """
    The boss fight scene of the game

    Attributes:
        boss (pygame.Surface): The boss image
    """
    def __init__(self):
        """ Initializes the boss scene """
        super().__init__()
        self.boss = None
        self.image_retrieve = Images()
        
    def setup(self):
        """ Loads all necessary data """
        self.boss = self.image_retrieve.boss['boss']

    def handle_events(self, events):
        """ Handles events for the boss scene """
        pass

    def update(self, dt):
        """ Runs any necessary logic for the boss scene """
        pass
    
    def render(self, screen):
        """ Draws the boss scene to the screen """
        screen.blit(self.boss, (100, 100))  # Example position

class BasicScene(Scene):
    """
    The basic scene of the game

    Attributes:
        background (pygame.Surface): The background image
    """
    def __init__(self):
        """ Initializes the basic scene """
        super().__init__()
        self.background = None
        self.image_retrieve = Images()

    def setup(self):
        """ Loads all necessary data """
        self.background = self.image_retrieve.backgrounds['first_background']

    def handle_events(self, events):
        """ Handles events for the basic scene """
        pass

    def update(self, dt):
        """ Runs any necessary logic for the basic scene """
        pass
    
    def render(self, screen):
        """ Draws the basic scene to the screen """
        screen.blit(self.background, (0, 0))  # Draw the background image