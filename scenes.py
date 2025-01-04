import pygame


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


class Menu(Scene):
    """
    The main menu scene of the game

    Attributes:
        image1 (pygame.Surface): The first image in the menu
        image2 (pygame.Surface): The second image in the menu
        # ... and so on ...
    """
    def __init__(self):
        """ Initializes the menu scene """
        pass

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
        pass
