import arcade
import random

class Enemy(arcade.Sprite):
    def __init__(self, sprite, scale, platform, object_list):
        super().__init__(sprite, scale)

        self.bottom = platform._get_top()
        self.center_x = random.randint(
            platform._get_left(), platform._get_right())

        self.velocity = (250, 0)
        self.reference = platform

        self.damage = 1

        object_list["enemies"].append(self)
        object_list["dynamics"].append(self)
        object_list["all"].append(self)

    def remove(self, object_list):
        object_list["enemies"].remove(self)
        object_list["dynamics"].remove(self)
        object_list["all"].remove(self)

    def get_damage(self):
        return self.damage