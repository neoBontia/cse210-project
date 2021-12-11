import random
from game import constants
from game.platform import Platform
from game.coin import Coin
from game.enemy import Enemy
from game.projectile import Projectile
from game.refill import Refill
from pathlib import Path

platform_sprites = [
    Path("project/art/sm_platform_ph.png"),
    Path("project/art/md_platform_ph.png"),
    Path("project/art/lg_platform_ph.png")
]

class Spawner():
    def spawn_platform(self, score, object_list):
        platform = Platform(random.choice(platform_sprites), constants.SCALE, object_list)
        
        object_list["platforms"].append(platform)
        object_list["dynamics"].append(platform)
        object_list["all"].append(platform)

        chance = random.randint(1, 3)
        if chance == 1:
            self.spawn_coin(platform, object_list)
            
        elif chance == 2:
            if score > 1:
                self.spawn_enemy(platform, object_list)
        elif chance == 3:
            if random.randint(1, 2) == 1:
                self.spawn_refill(platform, object_list)

    def spawn_coin(self, platform, object_list):
        Coin(Path("project/art/coin_ph.png"), constants.SCALE, platform, object_list)

    def spawn_enemy(self, platform, object_list):
        Enemy(Path("project/art/enemy_ph.png"), constants.SCALE, platform, object_list)

    def spawn_projectile(self, player, object_list):
        Projectile(Path("project/art/projectile.png"), constants.SCALE, player, object_list)

    def spawn_refill(self, platform, object_list):
        Refill(Path("project/art/refill.png"), constants.SCALE, platform, object_list)
