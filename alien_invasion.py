import sys
from time import sleep
import pygame
from settings import settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import ship
from bullet import bullet
from alien import Alien

class Alieninvasion:
    #overall class to manage game assets and behavior

    def __init__(self):
        #initialize the game and create game resources
        pygame.init()
        self.settings = settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien invesion")

        # create an instance to store game statistics,
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # make the play button.
        self.play_button = Button(self, "play")

        # set the background color.
        self.bg_color =(230, 230, 230)

    def _create_fleet(self):
        #create the fleet of aliens.
        # create an alien and find the number of aliens in a raw
        # spacing between each alien is equal to one  alien width.
        #make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width)
        number_aliens_x = available_space_x // (alien_width)

        #determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _create_alien(self, alien_number, row_number):
        # create an alien and place it in the raw.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 1.0 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.0 * alien.rect.height * row_number
        self.aliens.add(alien)
        
    def run_game(self):
        #starts the main loop for the game 
        while True:
            self.check_event()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _update_aliens(self):
        # check if fleet is at the adge then update the position of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        # look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

        # check for any bullets that have hit aliens.
        # if so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
                self.stats.score += self.settings.alien_points
                self.sb.prep_score()
   
    def _update_bullets(self):
        #update position of the bullets and get rid of old bullets.
        #update bullet position
            self.bullets.update()
           
            #get rid of bullets that have disappeared
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))

            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # respond to bullet-alien collision.
        # remove any bullets and aliens that have collied.
            if not self.aliens:
                # destroy existing bullets and create new fleet.
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()
                self._update_screen()
            #watch for keyboard and mouse event

    def check_event(self):
        #respond to keypresses and mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # start a new game when player clicks the play.
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset the game stastics.
            self.settings.initilize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True 
   
            # get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
   
            # create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # hide the mouse cursor.
            pygame.mouse.set_visible(False)
    
    def check_keydown_events(self, event):
        #respond to keypresses
        if event.key == pygame.K_RIGHT:
            #move the ship to right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:      
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()        
    
    def check_keyup_events(self, event):
        #respond to key releases.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.ship.rect.x += 1

    def _fire_bullet(self):
        #create a new bullet and add it to the bullet group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_screen(self):
        #update image on the screen, and flip to the new screen.
        #redraw the screen durinng each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        #make the most recently drawn screen visible
        pygame.display.flip()

    def _check_fleet_edges(self):
        #responce appropriatly if any aliens have reached an edge.
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        #drop the entire fleet and change the fleet's direction.
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed 
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        # respond to the ship being hit by an alien.
        if self.stats.ships_left > 0:
            #decrement ships_left.
            self.stats.ships_left -= 1

            # get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            #print("game over!!!")


    def _check_aliens_bottom(self):
        # check if any aliens have reached the bottom of the screen.
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat this the same as if the ship got hit.
                self._ship_hit()
                break 

if __name__ == '__main__':
    #make a game instance, and run the game.
    ai = Alieninvasion()
    ai.run_game()
