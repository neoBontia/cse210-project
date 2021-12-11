import arcade


class Projectile(arcade.Sprite):
    def __init__(self, sprite, scale, player, object_list):
        super().__init__(sprite, scale)

        self.center_y = player._get_center_y()
        self.center_x = player._get_center_x() + 32

        self.velocity = (1200, 0)

        object_list["projectiles"].append(self)
        object_list["dynamics"].append(self)
        object_list["all"].append(self)

    def remove(self, object_list):
        object_list["projectiles"].remove(self)
        object_list["dynamics"].remove(self)
        object_list["all"].remove(self)