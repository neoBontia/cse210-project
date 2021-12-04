import arcade
import random

from arcade import physics_engines
from game import constants
from game.spawner import Spawner
from game.player import Player
# from game.gameover import GameOverView


class Game(arcade.View):
    """Infinite side scroller platform jumping game
    Player starts from the left and must continue
    going to the right jumping from one platform to
    the other collecting coins and power-up, and
    evading the enemy."""

    def __init__(self):

        super().__init__()

        self.list_of_object_list = {
            "platforms": arcade.SpriteList(),
            "dynamics": arcade.SpriteList(),
            "coins": arcade.SpriteList(),
            "enemies": arcade.SpriteList(),
            "all": arcade.SpriteList()
        }

        self.platforms_list = arcade.SpriteList()
        self.dynamic_sprites = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        self.spawner = Spawner()
        self.score = 0
        self.paused = False

        self.setup()
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.list_of_object_list["platforms"], gravity_constant=0.9)

    def setup(self):

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player = Player(
            "project\\art\character_ph.png", constants.SCALE)
        self.list_of_object_list["all"].append(self.player)

        ground = arcade.Sprite(
            "project\\art\lg_platform_ph.png", constants.SCALE)
        ground.top = 64
        ground.left = 0
        # Testing enemy logic
        # self.spawner.spawn_enemy(ground, self.list_of_object_list)

        self.list_of_object_list["platforms"].append(ground)
        self.list_of_object_list["dynamics"].append(ground)
        self.list_of_object_list["all"].append(ground)

        for _ in range(6):
            self.spawner.spawn_platform(self.score, self.list_of_object_list)

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
        # if player is still alive
        if self.player.get_lives() < 1:
            view = GameOverView(self.score)
            self.window.show_view(view)

        # sprite updates
        if not self.paused:
            for sprite in self.list_of_object_list["all"]:
                sprite.center_x = int(
                    sprite.center_x + sprite.change_x * delta_time
                )
                sprite.center_y = int(
                    sprite.center_y + sprite.change_y * delta_time
                )
            # physics updates
            self.physics_engine.update()

        # coin collision
        collided_coin = self.player.collides_with_list(
            self.list_of_object_list["coins"])
        if len(collided_coin) > 0:
            self.score += collided_coin[0].get_score()
            collided_coin[0].obtained(self.list_of_object_list)

        # enemy collision
        collided_enemy = self.player.collides_with_list(
            self.list_of_object_list["enemies"])
        if len(collided_enemy) > 0:
            self.player.lives -= collided_enemy[0].get_damage()
            collided_enemy[0].remove(self.list_of_object_list)

        # camera panning
        self.pan_camera()
        # platform respawn
        for platform in self.list_of_object_list["platforms"]:
            if platform.right < 0:
                self.list_of_object_list["platforms"].remove(platform)
                self.list_of_object_list["dynamics"].remove(platform)
                self.list_of_object_list["all"].remove(platform)
                self.spawner.spawn_platform(
                    self.score, self.list_of_object_list)

        # enemy movement
        for enemy in self.list_of_object_list["enemies"]:
            if enemy._get_left() < enemy.reference._get_left():
                enemy.velocity = (250, 0)
            if enemy._get_right() > enemy.reference._get_right():
                enemy.velocity = (-200, 0)
            if enemy._get_right() < 0:
                enemy.remove(self.list_of_object_list)

        # player movement borders
        if self.player.top > constants.HEIGHT:
            self.player.top = constants.HEIGHT
        if self.player.right > constants.WIDTH/2:
            self.player.right = constants.WIDTH/2
        if self.player.bottom < 0:
            view = GameOverView(self.score)
            self.window.show_view(view)
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
        arcade.start_render()
        self.list_of_object_list["all"].draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, constants.HEIGHT -
                         28, arcade.csscolor.BLACK, 18)

        lives_text = f"Lives: {self.player.get_lives()}"
        arcade.draw_text(lives_text, 200, constants.HEIGHT -
                         28, arcade.csscolor.BLACK, 18)

    def pan_camera(self):
        mid = constants.WIDTH / 2
        if (self.player.right > mid):
            for sprite in self.list_of_object_list["dynamics"]:
                sprite.center_x = int(sprite.center_x - 5)





# GameOver Class

class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, score):
        """ This is run once when we switch to this view """
        super().__init__()
        # self.texture = arcade.load_texture("game_over.png")
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, constants.WIDTH - 1,
                            0, constants.HEIGHT - 1)
        self.curr_score = score
        self.score_list = []
        self.fetch_highscores()
        self.update_highscores()
        self.fetch_highscores()

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Game Over", self.window.width / 4, self.window.height / 2+50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to play again.", self.window.width / 4, self.window.height / 2-50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press Q to Quit.", self.window.width / 4, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Your score is " + str(self.curr_score), self.window.width / 4, self.window.height / 2 + 15,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
        highscore_label = "HIGHSCORES\n"
        arcade.draw_text(highscore_label, self.window.width * 0.75, self.window.height - 105,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        count = 1
        for line in self.score_list:
            arcade.draw_text(line, self.window.width * 0.75, self.window.height - 115 - (count * 40),
                           arcade.color.WHITE, font_size=20, anchor_x="center")
            count += 1

        
        # self.texture.draw_sized(constants.WIDTH / 2, constants.HEIGHT / 2,
        #                        constants.WIDTH, constants.HEIGHT)



    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = Game()
        self.window.show_view(game_view)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            arcade.close_window()

    def fetch_highscores(self):
        f = open("project\game\highscores.txt", "r")

        self.score_list = f.readlines()
        f.close()

    def update_highscores(self):
        for i in range(len(self.score_list) - 1):
            if self.curr_score > int(self.score_list[i]):
                self.score_list.insert(i, str(self.curr_score) + "\n")
                break
        self.score_list.pop(-1)
        self.score_list[-1] = " "

        f = open("project\game\highscores.txt", "w")
        f.writelines(self.score_list)
        f.close()
