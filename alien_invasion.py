import sys
import pygame
import json
import random
from pathlib import Path
from settings import Settings
from ship import Ship
from bullet import Bullet, AlienBullet
from alien import BossAlien, Alien
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
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.enemies_killed = 0
        self.upgrade_spawned = False
        self.bullet_type = 'bullet'

        self.last_alien_spawn_time = pygame.time.get_ticks()
        self.alien_spawn_interval = self.settings.alien_spawn_interval
        
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
        # TODO: Put in input mov class. Sound when bullet fires
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

    def _spawn_alien(self):
        """Spawn a single alien at a random location."""
        alien_type = self.stats.level % 3 + 1 
        x_position = random.randint(0, self.settings.screen_width - 50)  # Keep aliens on-screen
        y_position = random.randint(-100, -40)  # Spawn just above the screen

        new_alien = Alien(self, alien_type)
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    # def _check_fleet_edges(self, delta_time):
    #     """If any alien ship hits the edge, change behavior."""
    #     for alien in self.aliens.sprites():
    #         if alien.check_edges():
    #             self._change_fleet_direction(delta_time)
    #             break
        
    # def _change_fleet_direction(self, delta_time):
    #     """Drop the entire fleet and change the fleet's direction."""
    #     for alien in self.aliens.sprites():
    #         alien.rect.y += self.settings.fleet_drop_speed * delta_time
    #     self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update the images on the screen, and flip to the new screen"""
        self.screen.blit(self.image_retrieve.backgrounds['first_background'], (0, 0))  # Draw the background image

        self.ship.blitme()
        self.draw_mouse_indicator(self.screen)
        self.aliens.draw(self.screen)
        self.upgrades.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()

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
        self.alien_bullets.update(delta_time)

        # Get rid of bullets outside windows
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Get rid of alien bullets outside windows
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(alien_bullet)

        self._check_bullet_alien_collision()
        
    def _play_noise(self, selection:str):
        """Select a sound to be made when an event happens."""
        self.sound_manager.play_sound_effect(selection)
        
    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        self._handle_collisions()
        self._check_if_level_finished()
        self._check_if_boss_fight_should_start()

    def _handle_collisions(self):
        """Handle collisions between bullets and aliens."""
        # If bullets hit the alien do collision
        player_bullets_collision = pygame.sprite.groupcollide(
                self.bullets, self.aliens, False, True # True means it will remove the sprite from the group
            )

        alien_player_collision = pygame.sprite.spritecollide(
            self.ship, self.alien_bullets, True, False
            )

        if player_bullets_collision or alien_player_collision:
            self._play_noise('damageSound')
            for aliens in player_bullets_collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.score.prep_score()
            self.score.check_high_score()
            self.enemies_killed += len(aliens)
            if self.enemies_killed >= 25 and not self.upgrade_spawned:
                self._create_upgrade() 
                self.enemies_killed = 0

    def _check_if_level_finished(self):
        """Check if all aliens have been destroyed."""
        if not self.aliens:
            self.bullets.empty()
            self.stats.level += 1
            # self._create_fleet()
            self.settings.increase_speed()

        # Reduce spawn interval to increase difficulty
        self.alien_spawn_interval = max(500, self.alien_spawn_interval - 200)  # Minimum of 500 ms

    def _check_if_boss_fight_should_start(self):
        """Check if it is time for a boss fight to start."""
        if self.stats.level % 5 == 0 and self.stats.level != 0:
            self._start_boss_fight()


    def _create_upgrade(self):
        """Create an upgrade at a random location."""
        upgrade_type = random.choice(['missile','laser','shooting_speed', 'ship_speed', 'ship_shield'])  
        location = (random.randint(0, self.settings.screen_width), 
                    random.randint(0, self.settings.screen_height))
        upgrade = Upgrade(upgrade_type, location, self.image_retrieve)
        self.upgrades.add(upgrade)
        self.upgrade_spawned = True
        print(f"Created upgrade: {upgrade_type} at {location}")

    def _update_aliens(self, delta_time):
        """Update the alien positions and spawn new aliens."""
        current_time = pygame.time.get_ticks()

        # Spawn a new alien at regular intervals
        if current_time - self.last_alien_spawn_time > self.alien_spawn_interval:
            self._spawn_alien()
            self.last_alien_spawn_time = current_time

        # Update existing aliens
        self.aliens.update(delta_time)

        self._alien_shoot()

        # Check for collisions
        self._check_alien_collision()

    def _alien_shoot(self):
        """Handle the bullets shot by the alien ships."""
        for alien in self.aliens:
            if random.random() < 0.01:
                new_bullet = AlienBullet(alien, self)
                self.alien_bullets.add(new_bullet)
        
    def _check_alien_collision(self): 
        """Check alien ship collisions with our ship."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # collisions = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)

        
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
                # self._create_fleet()
                self.ship.center_ship()
                sleep(0.5)
            else:
                self.game_active = False
                pygame.mouse.set_visible(True)

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

        # self._create_fleet()
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