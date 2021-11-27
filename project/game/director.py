import arcade
import random

from arcade import physics_engines
from game import constants
from game.spawner import Spawner


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
        self.spawner = Spawner()
        self.is_paused = False

        self.setup()
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platforms_list, gravity_constant=0.9)


    def setup(self):

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player = arcade.Sprite(
            "project\\art\character_ph.png", constants.SCALE)
        self.player.bottom = 65
        self.player.left = 10
        self.all_sprites.append(self.player)

        ground = arcade.Sprite("project\\art\platform_ph.png", constants.SCALE)
        ground.top = 64
        ground.left = 0
        self.platforms_list.append(ground)
        self.dynamic_sprites.append(ground)
        self.all_sprites.append(ground)

        for _ in range(9):
            self.spawner.spawn_platform(self.platforms_list, self.dynamic_sprites, self.all_sprites)


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if (symbol == arcade.key.W or symbol == arcade.key.UP) and self.physics_engine.can_jump():
            self.player.change_y = 20  # JUMP

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 5


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
            
        self.physics_engine.update()

        self.pan_camera()
        for platform in self.platforms_list:
            if platform.right < 0:
                self.platforms_list.remove(platform)
                self.dynamic_sprites.remove(platform)
                self.all_sprites.remove(platform)
                self.spawner.spawn_platform(self.platforms_list, self.dynamic_sprites, self.all_sprites)

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width/2:
            self.player.right = self.width/2
        if self.player.bottom < 0:
            arcade.close_window()
        if self.player.left < 0:
            self.player.left = 0


    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()


    def pan_camera(self):
        mid = self.width / 2
        if (self.player.right > mid):
            for sprite in self.dynamic_sprites:
                sprite.center_x = int(sprite.center_x - 5)