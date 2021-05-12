import pygame.font

class Scoreboard:
    # A class to report scoring information.

    def __init__(self, ai_game):
        # initilize scorekeeping attributes.
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score imgae. 
        self.prep_score()
        
    def prep_score(self):
        # turn the score into rendered image.
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.score_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        # draw score to the screen. 
        self.screen.blit(self.score_image, self.score_rect)