import arcade
import random
from game import constants

class Player(arcade.Sprite):
    def __init__(self, sprite, scale):
        super().__init__(sprite, scale)

        self.bottom = 65
        self.left = 10

        self.lives = 3

    def get_lives(self):
        return self.lives