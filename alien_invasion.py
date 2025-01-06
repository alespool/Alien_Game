import sys
import pygame
import json
import random
from pathlib import Path
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien, BossAlien
from time import sleep
from game_stats import GameStats
from buttons import Button
from scoreboard import Scoreboard
from fleet_patterns import FleetStructure
from sounds import SoundManager
from images import Images
from upgrades import Upgrade


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

        self.sound_manager = SoundManager()
        self.image_retrieve = Images()

        # Create an instance to store the stats  
        self.stats = GameStats(self)
        self.score = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.fleet = FleetStructure(self)
        self.enemies_killed = 0
        self.upgrade_spawned = False
        self.bullet_type = 'bullet'

        self._create_fleet()

        self.play_button = Button(self, "PLAY")
        self._make_difficulty_buttons()

        # Start the game on active state
        self.game_active = False  

        self.boss = None

    def run_game(self):
        """Start the main game loop."""
        while True:
            # Check events
            self._check_events()

            # Calculate delta time
            delta_time = self.clock.get_time() / 100  # Time in seconds

            if self.game_active:
                self.ship.update_position(delta_time) 
                self.ship.update_rotation()
                self._update_bullets(delta_time)
                self._update_aliens(delta_time)

            # Redraw screen
            self._update_screen()

            # Limit frame rate
            self.clock.tick(120)

    def _check_events(self):
        """Check for events or letters typed."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self._close_game()

            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        # Start the game with P
        if event.key == pygame.K_p and not self.game_active:
            self._start_game()

        # Move the ship with the arrow keys or WASD
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.movement.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.movement.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.movement.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.movement.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._play_noise('laserShoot')
            self._fire_bullet()

        # QUIT THE GAME
        if event.key == pygame.K_q:
            self._close_game()
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.movement.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.movement.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.movement.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.movement.moving_down = False

    def _create_fleet(self):
        """Create the fleet of alien ships."""
        alien_type = self.stats.level % 3 + 1
        self.aliens.empty()  # Clear existing aliens before creating the new fleet.

        self.fleet.create_fleet(alien_type)

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
        self.screen.blit(self.image_retrieve.backgrounds['first_background'], (0, 0))  # Draw the background image

        self.ship.blitme()
        self.draw_mouse_indicator(self.screen)
        self.aliens.draw(self.screen)
        self.upgrades.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.score.show_score()

        if not self.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        # Get the mouse position 
        pos = pygame.mouse.get_pos()

        mouse_x = pos[0]
        mouse_y = pos[1]

        new_bullet = Bullet(self, mouse_x, mouse_y, self.bullet_type)
        self.bullets.add(new_bullet)

        # Reset bullet_type
        print(f"Bullet type: {self.bullet_type}")
        if self.bullet_type == 'missile' or self.bullet_type == 'laser':
            self.bullet_type = 'bullet'
        
    def _update_bullets(self, delta_time):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update(delta_time)

        # Get rid of bullets outside windows
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()
        
    def _play_noise(self, selection:str):
        """Select a sound to be made when an event happens."""
        self.sound_manager.play_sound_effect(selection)
        
    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        # If bullets hit the alien do collision
        collision = pygame.sprite.groupcollide(
                self.bullets, self.aliens, False, True # True means it will remove the sprite from the group
        )

        if collision:
            self._play_noise('damageSound')
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.score.prep_score()
            self.score.check_high_score()
            self.enemies_killed += len(aliens)
            if self.enemies_killed >= 2 and not self.upgrade_spawned:
                self._create_upgrade() 
                self.enemies_killed = 0

        # If no more aliens, recreate the fleet
        if not self.aliens:
            self.bullets.empty()
            self.stats.level += 1
            if self.stats.level % 5 == 0:  # Example condition for boss level
                self._start_boss_fight()
            else:
                self._create_fleet()
                self.settings.increase_speed()


    def _create_upgrade(self):
        """Create an upgrade at a random location."""
        upgrade_type = random.choice(['missile','laser'])  
        location = (random.randint(0, self.settings.screen_width), 
                    random.randint(0, self.settings.screen_height))
        upgrade = Upgrade(upgrade_type, location, self.image_retrieve)
        self.upgrades.add(upgrade)
        print(f"Created upgrade: {upgrade_type} at {location}")


    def _update_aliens(self, delta_time):
        """Update the alien fleet position."""
        self._check_fleet_edges(delta_time)
        self.aliens.update(delta_time)

        # If the alien ship collides with our ship, or goes below the edges lose game
        if pygame.sprite.spritecollide(self.ship, self.aliens, False):
            self._ship_hit()
        
        self._check_aliens_bottom()
        self._check_upgrade_collision()
        
    def _check_upgrade_collision(self):
        """Check for collisions between the ship and upgrades."""
        upgrade_collisions = pygame.sprite.spritecollide(self.ship, self.upgrades, True)
        for upgrade in upgrade_collisions:
            upgrade.apply_upgrade(self.ship)
            self.upgrade_spawned = False
            if upgrade.upgrade_type == 'missile':
                self.bullet_type = 'missile'
            if upgrade.upgrade_type == 'laser':
                self.bullet_type = 'laser'
                

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.settings.shield_strength > 0:
            self.settings.shield_strength -= 1
            self.ship.center_ship()
        else:
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
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._play_noise('enterGameSound')
            self._start_game()

    def _make_difficulty_buttons(self):
        """Create buttons for difficulty levels."""
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")

        # Position buttons on the screen to not overlap
        self.easy_button.rect.top = (
            self.play_button.rect.top + 1.5*self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (
            self.easy_button.rect.top + 1.5*self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = (
            self.medium_button.rect.top + 1.5*self.medium_button.rect.height)
        self.hard_button._update_msg_position()

        self.medium_button.set_highlighted_color()

    def _check_difficulty_buttons(self, mouse_pos):
        """Set the right difficulty for the game as chosen with the mouse."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self._play_noise('selectionSound')
            self.settings.difficulty_level = 'Easy'
            self.easy_button.set_highlighted_color()
            self.medium_button.set_base_color()
            self.hard_button.set_base_color()
        elif medium_button_clicked:
            self._play_noise('selectionSound')
            self.settings.difficulty_level = 'Medium'
            self.easy_button.set_base_color()
            self.medium_button.set_highlighted_color()
            self.hard_button.set_base_color()
        if hard_button_clicked:
            self._play_noise('selectionSound')           
            self.settings.difficulty_level = 'Hard'
            self.easy_button.set_base_color()
            self.medium_button.set_base_color()
            self.hard_button.set_highlighted_color()

    def _start_game(self):
        """Start a new game."""
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.score.prep_score()
        self.game_active = True

        self.bullets.empty()
        self.aliens.empty()

        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    def draw_mouse_indicator(self, screen):
        """Draw a custom indicator at the mouse position."""
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (255, 0, 0), mouse_pos, 5)  # Red dot
        pygame.draw.line(screen, (255, 0, 0), (mouse_pos[0] - 10, mouse_pos[1]), 
                        (mouse_pos[0] + 10, mouse_pos[1]), 2)  # Horizontal line
        pygame.draw.line(screen, (255, 0, 0), (mouse_pos[0], mouse_pos[1] - 10), 
                        (mouse_pos[0], mouse_pos[1] + 10), 2)  # Vertical line


    def _close_game(self):
        """Saves highest score and exit the game."""
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)


        sys.exit()

    def _start_boss_fight(self):
        """Start the boss fight."""
        self.boss = BossAlien(self)
        self.aliens.add(self.boss)


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()