import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create game resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()


    def run_game(self):
        """Start the main game loop"""
        while True:
            # Watch for keyboard and mouse events
            self._check_events()

            # Calculate time passed between frames (delta_time)
            delta_time = self.clock.get_time() / 100  # Time in seconds

            # Update the ship movement with delta_time
            self.ship.update(delta_time)

            # Update the bullet movement with delta_time
            self._update_bullets(delta_time)

            # Redraw the screen during each pass to give the color
            self._update_screen()

            # Set the internal game clock
            self.clock.tick(60)


    def _check_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Move the ship
                if event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()        

        # QUIT THE GAME
        if event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _create_fleet(self):
        """Create the fleet of alien ships."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x,current_y = alien_width * 0.5, alien_height
        while current_y < (self.settings.screen_height -3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width * 0.5

            # Write another row
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create a new alien at the defined x position in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_screen(self):
        """Update the images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        
    def _update_bullets(self, delta_time):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update(delta_time)

        # Get rid of bullets outside windows
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)



if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()



    # def _create_fleet(self):
    #     """Create the fleet of alien ships that we need to destroy."""
    #     alien = Alien(self)
    #     alien_width = alien.rect.width
    #     total_space = self.settings.screen_width - 2 * alien_width

    #     spacing = (total_space - (25 * alien_width)) / 24  # 25 aliens, 24 gaps

    #     current_x = alien_width
    #     for _ in range(25):
    #         new_alien = Alien(self)
    #         new_alien.x = current_x
    #         new_alien.rect.x = current_x
    #         self.aliens.add(new_alien)
    #         current_x += alien_width + spacing