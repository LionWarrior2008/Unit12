from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
class GameStats():
    def __init__(self,game:'AlienInvasion'):
        self.game=game
        self.settings=game.settings
        self.max_score=0
    def reset_stats(self):
        self.ship_left=self.settings.ship_limit
        self.score=0
        self.level=1
    def update(self,collisions):
        self.update_score(collisions)
        self.update_max_score()
    def update_max_score(self):
        if self.score>self.max_score:
            self.max_score=self.score

    def update_score(self,collisions):
        for alien in collisions.values():
            self.score+=self.settings.alien_points
    def update_level(self):
        self.level+=1



        pass