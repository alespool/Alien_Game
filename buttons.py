import pygame.font

class Button:
    """A class to build buttons for the game."""
    def __init__(self, ai_game, msg, y_offset=0):
        """Initialize the button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.msg = msg

        # Set the dimensions of the button
        self.width, self.height = 200,50
        self.button_color = (0,135,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += y_offset

        # The message on the button
        self._button_msg(msg)

    def _button_msg(self, msg):
        """Turn the message into a rendered image and center the text on the button."""
        self.msg_image = self.font.render(msg, True, 
                self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the blank button and then draw the message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
