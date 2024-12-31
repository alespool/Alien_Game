import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from buttons import Button

class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, create game resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store the stats
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_buttons = self._create_buttons()

        # Start the game on active state
        self.game_active = False

    def run_game(self):
        """Start the main game loop"""
        while True:
            # Watch for keyboard and mouse events
            self._check_events()

            # Calculate time passed between frames (delta_time)
            delta_time = self.clock.get_time() / 100  # Time in seconds
            
            if self.game_active:
                self.ship.update(delta_time)
                self._update_bullets(delta_time)
                self._update_aliens(delta_time)

            # Redraw the screen during each pass to give the color
            self._update_screen()
            # Set the internal game clock
            self.clock.tick(120)


    def _check_events(self):
        """Check for events or letters typed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        # Move the ship
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

        # Start the game with P
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

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

        current_x,current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height -3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

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

    def _check_fleet_edges(self, delta_time):
        """If any alien ship hits the edge, change behavior."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction(delta_time)
                break
        
    def _change_fleet_direction(self, delta_time):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed * delta_time
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update the images on the screen, and flip to the new screen"""
        self.screen.blit(self.settings.bg_image, (0, 0))  # Draw the background image

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        if not self.game_active:
            # Create buttons
            for button in self.play_buttons:
                button.draw_button()

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

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        # If bullets hit the alien do collision
        collision = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True # True means it will remove the sprite from the group
        )

        # If no more aliens, recreate the fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_aliens(self, delta_time):
        """Update the alien fleet position."""
        self._check_fleet_edges(delta_time)
        self.aliens.update(delta_time)

        # If the alien ship collides with our ship, or goes below the edges lose game
        if pygame.sprite.spritecollide(self.ship, self.aliens, False):
            self._ship_hit()
        
        self._check_aliens_bottom()
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_remaining > 0:
            self.stats.ships_remaining -= 1

            # Get rid of remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this same as if the ship got hit
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        for button in self.play_buttons:
            if button.rect.collidepoint(mouse_pos) and not self.game_active:
                if button.msg == "SCORES":
                    pass
                elif button.msg == "Easy":
                    self.settings.set_difficulty("Easy")
                elif button.msg == "Medium":
                    self.settings.set_difficulty("Medium")
                elif button.msg == "Hard":
                    self.settings.set_difficulty("Hard")
                self._start_game()
                break

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.game_active = True

        self.bullets.empty()
        self.aliens.empty()

        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    def _create_buttons(self):
        """Create buttons for difficulty levels."""
        play_buttons = []
        button_texts = ["SCORES", "Easy", "Medium", "Hard"]
        button_spacing = 60 

        for i, text in enumerate(button_texts):
            y_offset = i * button_spacing
            button = Button(self, text, y_offset=y_offset)
            play_buttons.append(button)

        return play_buttons

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