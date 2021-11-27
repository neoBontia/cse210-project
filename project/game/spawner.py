import random
from game import constants
from game.platform import Platform
from game.coin import Coin

class Spawner():
    def spawn_platform(self, object_list):
        platform = Platform("project\\art\platform_ph.png", constants.SCALE, object_list)
        
        object_list["platforms"].append(platform)
        object_list["dynamics"].append(platform)
        object_list["all"].append(platform)

        if random.randint(1, 2) == 1:
            self.spawn_coin(platform, object_list)

    def spawn_coin(self, platform, object_list):
        Coin("project\\art\coin_ph.png", constants.SCALE, platform, object_list)