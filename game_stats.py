class GameStats:
    # track statistic for alien invantion.

    def __init__(self, ai_game):
        # initilize statistics.
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        # initilize statistics that can change during the game.
        self.ships_left = self.settings.ship_limit