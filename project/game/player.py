import arcade
import random
from game import constants

class Player(arcade.Sprite):
    def __init__(self, sprite, scale):
        super().__init__(sprite, scale)

        self.bottom = 65
        self.left = 10

        self.lives = 3
        self.projectiles = 1

    def get_lives(self):
        return self.lives

    def can_shoot(self):
        if self.projectiles > 0:
            return True
        else:
            return False