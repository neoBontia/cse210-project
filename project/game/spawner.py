import arcade
import random
from game import constants

class Spawner():
    def spawn_platform(self, platforms, dynamics, all):
        platform = arcade.Sprite("project\\art\platform_ph.png", constants.SCALE)

        platform.top = random.randint(platforms[-1]._get_top() - (
            100 * constants.SCALE), platforms[-1]._get_top() + (100 * constants.SCALE))
        platform.left = platforms[-1]._get_right() + \
            random.randint(50, 120)

        if platform.bottom < 0:
            platform.top = platforms[-1]._get_top() + \
                (100 * constants.SCALE)
        if platform.top >= constants.HEIGHT - 70:
            platform.top = platforms[-1]._get_top() - \
                (100 * constants.SCALE)

        platforms.append(platform)
        dynamics.append(platform)
        all.append(platform)
