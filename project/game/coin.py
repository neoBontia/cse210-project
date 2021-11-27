import arcade
import random

class Coin(arcade.Sprite):
    def __init__(self, sprite, scale, platform, object_list):
        super().__init__(sprite, scale)

        self.score = 1

        self.top = platform._get_top() + 37
        self.center_x = random.randint(
            platform._get_left(), platform._get_right())

        object_list["coins"].append(self)
        object_list["dynamics"].append(self)
        object_list["all"].append(self)

    def obtained(self, object_list):
        object_list["coins"].remove(self)
        object_list["dynamics"].remove(self)
        object_list["all"].remove(self)

    def get_score(self):
        return self.score
