class settings:
    # a class to store all the settings for alien invesion

    def __init__(self):
        # initilize the game's static settings.
        self.screen_width = 1200
        self.screen_height = 670
        self.bg_color = (230, 230, 230)
        
        #Alien settings
        self.alien_speed = 5.0
        self.fleet_drop_speed = 15

        # how quickly the game speed up.
        self.speedup_scale = 1.1

        # how quickly the alien points values increase
        self.score_scale = 1.5

        self.initilize_dynamic_settings()
        
        # fleet_direction od 1 represent right; -1 represent left.
        self.fleet_direction = 1

        #bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # ship settings
        self.ship_speed = 10  
        self.ship_limit = 3

    def initilize_dynamic_settings(self):
        # initilize settings that change thourghout the game.
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # scoring
        self.alien_points = 50

    def increase_speed(self):
        # increase speed settings and alien point value.
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
               
        self.alien_points = int(self.alien_points * self.score_scale)
        