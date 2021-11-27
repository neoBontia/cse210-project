import arcade
import random
from game import constants

class Spawner():
    def spawn_platform(self, object_list):
        platform = arcade.Sprite("project\\art\platform_ph.png", constants.SCALE)
        
        platform.top = random.randint(object_list["platforms"][-1]._get_top() - (
            100 * constants.SCALE), object_list["platforms"][-1]._get_top() + (100 * constants.SCALE))
        platform.left = object_list["platforms"][-1]._get_right() + \
            random.randint(50, 120)

        if platform.bottom < 0:
            platform.top = object_list["platforms"][-1]._get_top() + \
                (100 * constants.SCALE)
        if platform.top >= constants.HEIGHT - 70:
            platform.top = object_list["platforms"][-1]._get_top() - \
                (100 * constants.SCALE)

        object_list["platforms"].append(platform)
        object_list["dynamics"].append(platform)
        object_list["all"].append(platform)

        self.spawn_coin(platform, object_list)

    def spawn_coin(self, platform, object_list):
        coin = arcade.Sprite("project\\art\coin_ph.png", constants.SCALE)

        coin.top = platform._get_top() + 37
        coin.center_x = platform._get_center_x()

        object_list["dynamics"].append(coin)
        object_list["all"].append(coin)
