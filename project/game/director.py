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

        for _ in range(5): # platforms still need to spawn outside of the screen
            platform = arcade.Sprite("project\\art\platform_ph.png", constants.SCALE)
            platform.top = random.randint(32, self.height)
            platform.left = random.randint(10, self.width - 96)
            self.platforms_list.append(platform)
            self.dynamic_sprites.append(platform)
            self.all_sprites.append(platform)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused
        
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player.change_y = 5000 # JUMP

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -250

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 250

    def on_key_release(self, symbol, modifiers):
        if (
            symbol == arcade.key.W
            or symbol == arcade.key.S
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.A
            or symbol == arcade.key.D
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )
        self.player.change_y = -250 # GRAVITY

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()

    def handle_collision(self):
        pass

    def pan_camera(self):
        pass