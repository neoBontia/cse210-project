import arcade
import random
from game import constants

class Platform(arcade.Sprite):
    def __init__(self, sprite, scale, object_list):
        super().__init__(sprite, scale)

        self.top = random.randint(object_list["platforms"][-1]._get_top() - (
            100 * constants.SCALE), object_list["platforms"][-1]._get_top() + (100 * constants.SCALE))
        self.left = object_list["platforms"][-1]._get_right() + \
            random.randint(50, 120)

        if self.bottom < 0:
            self.top = object_list["platforms"][-1]._get_top() + \
                (100 * constants.SCALE)
        if self.top >= constants.HEIGHT - 70:
            self.top = object_list["platforms"][-1]._get_top() - \
                (100 * constants.SCALE)
