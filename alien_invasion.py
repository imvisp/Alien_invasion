import sys
import pygame
from settings import settings
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

        self.ship = ship(self)
        self.bullets = pygame.sprite.Group()
        self.alians = pygame.sprite.Group()

        self._create_fleet()

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
        # create the first of aliens.
        for alien_number in range(number_aliens_x):
            self._create_fleet(alien_number)
        
    def _create_alien(self, alien_number):
        # create an alien and place it in the raw.
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 1.5 * alien_width * alien_number
        alien.rect.x = alien.x
        self.alians.add(alien)
        
    def run_game(self):
        #starts the main loop for the game 
        while True:
            self.check_event()
            self.ship.update()
            self._update_bullets()

    def _update_bullets(self):
        #update position of the bullets and get rid of old bullets.
        #update bullet position
            self.bullets.update()

            #get rid of bullets that have disappeared
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))

            self.update_screen()
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
    
    def update_screen(self):
        #update image on the screen, and flip to the new screen.
        #redraw the screen durinng each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.alians.draw(self.screen)
        #make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #make a game instance, and run the game.
    ai = Alieninvasion()
    ai.run_game()
