import arcade
import random
from game import constants

class Platform(arcade.Sprite):
    def respawn(self, platforms):
        platforms.remove(self)
        platform = platforms[-1]

        if self.right < 0:
            self.top = random.randint(platform._get_top() - (100 * constants.SCALE), platform._get_top() + (100 * constants.SCALE))
            self.left = platform._get_right() + 20
            if self.bottom < 0:
                self.top = platform._get_top() + \
                    100 * constants.SCALE
            if self.top >= constants.HEIGHT - 70:
                self.top = constants.HEIGHT - 70
                
        platforms.append(self)
