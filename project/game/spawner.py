import random
from game import constants
from game.platform import Platform
from game.coin import Coin
from game.enemy import Enemy

platform_sprites = [
    "project\\art\sm_platform_ph.png",
    "project\\art\md_platform_ph.png",
    "project\\art\lg_platform_ph.png"
]

class Spawner():
    def spawn_platform(self, score, object_list):
        platform = Platform(random.choice(platform_sprites), constants.SCALE, object_list)
        
        object_list["platforms"].append(platform)
        object_list["dynamics"].append(platform)
        object_list["all"].append(platform)

        if random.randint(1, 2) == 1:
            self.spawn_coin(platform, object_list)
        elif 2:
            if score > 1:
                self.spawn_enemy(platform, object_list)

    def spawn_coin(self, platform, object_list):
        Coin("project\\art\coin_ph.png", constants.SCALE, platform, object_list)

    def spawn_enemy(self, platform, object_list):
        Enemy("project\\art\enemy_ph.png", constants.SCALE, platform, object_list)
