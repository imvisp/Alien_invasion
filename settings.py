class settings:
    # a class to store all the settings for alien invesion

    def __init__(self):
        # initilize the game's settings.
        self.screen_width = 1200
        self.screen_height = 670
        self.bg_color = (230, 230, 230)
        
        #Alien settings
        self.alien_speed = 2.0
        self.fleet_drop_speed = 15
        
        # fleet_direction od 1 represent right; -1 represent left.
        self.fleet_direction = 1

        #bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # ship settings
        self.ship_speed = 5  
               
        