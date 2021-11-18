import arcade
import random
from game import constants

class Game(arcade.Window):
    """Infinite side scroller platform jumping game
    Player starts from the left and must continue
    going to the right jumping from one platform to
    the other collecting coins and power-up, and
    evading the enemy."""

    def __init__(self, width, height, title):
        
        super().__init__(width, height, title)

        self.platforms_list = arcade.SpriteList()
        self.dynamic_sprites = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.is_paused = False

        self.setup()

    def setup(self):

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player = arcade.Sprite("project\\art\character_ph.png", constants.SCALE)
        self.player.bottom = 1
        self.player.left = 10
        self.all_sprites.append(self.player)

        self.platform = arcade.Sprite("project\\art\platform_ph.png", constants.SCALE)
        self.platform.top = random.randint(32, self.height)
        self.platform.left = random.randint(10, self.width - 96)
        self.platforms_list.append(self.platform)
        self.dynamic_sprites.append(self.platform)
        self.all_sprites.append(self.platform)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()
