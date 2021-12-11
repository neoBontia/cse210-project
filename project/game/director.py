from os import kill
import arcade
import random

from arcade import physics_engines
from game import constants
from game.spawner import Spawner
from game.player import Player
from pathlib import Path


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
            "refill": arcade.SpriteList(),
            "enemies": arcade.SpriteList(),
            "projectiles": arcade.SpriteList(),
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
            Path("project\\art\character_ph.png"), constants.SCALE)
        self.list_of_object_list["all"].append(self.player)

        ground = arcade.Sprite(
            Path("project\\art\lg_platform_ph.png"), constants.SCALE)
        ground.top = 64
        ground.left = 0
        # Testing enemy logic
        #self.spawner.spawn_enemy(ground, self.list_of_object_list)

        self.list_of_object_list["platforms"].append(ground)
        self.list_of_object_list["dynamics"].append(ground)
        self.list_of_object_list["all"].append(ground)

        for _ in range(6):
            self.spawner.spawn_platform(self.score, self.list_of_object_list)

        self.jump_sound = arcade.load_sound(Path("project\sounds\jump.wav"))
        self.coin_collision_sound = arcade.load_sound(Path("project\sounds\coins.mp3"))
        self.game_over_sound = arcade.load_sound(Path("project\sounds\game_over.wav"))
        self.shoot_projectile = arcade.load_sound(Path("project\sounds\shooting.mp3"))
        self.button = arcade.load_sound(Path("project\sounds\\buttons.wav"))
        self.player_enemy_collision = arcade.load_sound(Path("project\sounds\player_enemy.wav"))
        self.projectile_enemy_collision = arcade.load_sound(Path("project\sounds\projectile_enemy.wav"))
        self.refill_collision = arcade.load_sound(Path("project\sounds\\refill_collision.wav"))

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            arcade.play_sound(self.button)
            arcade.close_window()

        if symbol == arcade.key.P:
            arcade.play_sound(self.button)
            self.paused = not self.paused

        if (symbol == arcade.key.W or symbol == arcade.key.UP) and self.physics_engine.can_jump():
            self.player.change_y = 20  # JUMP
            arcade.play_sound(self.jump_sound)

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 5

        if symbol == arcade.key.SPACE:
            if self.player.can_shoot():
                arcade.play_sound(self.shoot_projectile)
                self.spawner.spawn_projectile(self.player, self.list_of_object_list)
                self.player.projectiles -= 1

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
        # if player is dead
        if self.player.get_lives() < 1:
            arcade.play_sound(self.game_over_sound)
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

        # projectile physics
        for projectile in self.list_of_object_list["projectiles"]:
            if projectile.left > constants.WIDTH:
                projectile.remove(self.list_of_object_list)

            killed_enemy = projectile.collides_with_list(self.list_of_object_list["enemies"])
            if len(killed_enemy) > 0:
                arcade.play_sound(self.projectile_enemy_collision)
                self.score += 5
                killed_enemy[0].remove(self.list_of_object_list)
                projectile.remove(self.list_of_object_list)

        # coin collision
        collided_coin = self.player.collides_with_list(
            self.list_of_object_list["coins"])
        if len(collided_coin) > 0:
            arcade.play_sound(self.coin_collision_sound)
            self.score += collided_coin[0].get_score()
            collided_coin[0].obtained(self.list_of_object_list)

        # refill collision
        obtained_refill = self.player.collides_with_list(self.list_of_object_list["refill"])
        if len(obtained_refill) > 0:
            arcade.play_sound(self.refill_collision)
            self.player.projectiles += obtained_refill[0].get_value()
            obtained_refill[0].obtained(self.list_of_object_list)

        # enemy collision
        collided_enemy = self.player.collides_with_list(
            self.list_of_object_list["enemies"])
        if len(collided_enemy) > 0:
            arcade.play_sound(self.player_enemy_collision)
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
            arcade.play_sound(self.game_over_sound)
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

        projectile_text = f"Projectiles: {self.player.projectiles}"
        arcade.draw_text(projectile_text, 390, constants.HEIGHT -
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
        self.can_update = True
        self.initials_input = arcade.load_sound(Path("project\sounds\highscore_input.mp3"))
        self.button = arcade.load_sound(Path("project\sounds\\buttons.wav"))

        self.inputs = ["A", "A", "A"]

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Game Over", self.window.width / 4, self.window.height / 2+50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text(f"Your score is {str(self.curr_score)}!", self.window.width / 4, self.window.height / 2 + 15,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        arcade.draw_text("Initials: ", 425, self.window.height / 2 - 20,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        count = 1
        for char in self.inputs:
            arcade.draw_text(char, 455 + (count * 22), self.window.height / 2 - 20,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
            count += 1

        arcade.draw_text("Press ENTER to save your highscore.", self.window.width / 4, self.window.height / 2-50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press SPACE to play again.", self.window.width / 4, self.window.height / 2-95,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press ESC to Quit.", self.window.width / 4, self.window.height / 2-120,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        


        arcade.draw_text("HIGHSCORES", self.window.width * 0.75, self.window.height - 105,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        count = 1
        for line in self.score_list:
            arcade.draw_text(f"{line}", self.window.width * 0.75, self.window.height - 115 - (count * 40),
                           arcade.color.WHITE, font_size=20, anchor_x="center")
            count += 1

        
        
        # self.texture.draw_sized(constants.WIDTH / 2, constants.HEIGHT / 2,
        #                        constants.WIDTH, constants.HEIGHT)


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.play_sound(self.button)
            arcade.close_window()
        if symbol == arcade.key.ENTER:
            if self.can_update:
                arcade.play_sound(self.button)
                self.update_highscores()
                self.fetch_highscores()
                self.can_update = False
        if symbol == arcade.key.SPACE:
            arcade.play_sound(self.button)
            game_view = Game()
            self.window.show_view(game_view)

        if symbol == arcade.key.A:
            arcade.play_sound(self.initials_input)
            self.inputs.append("A")
            self.inputs.pop(0)
        if symbol == arcade.key.B:
            arcade.play_sound(self.initials_input)
            self.inputs.append("B")
            self.inputs.pop(0)
        if symbol == arcade.key.C:
            arcade.play_sound(self.initials_input)
            self.inputs.append("C")
            self.inputs.pop(0)
        if symbol == arcade.key.D:
            arcade.play_sound(self.initials_input)
            self.inputs.append("D")
            self.inputs.pop(0)
        if symbol == arcade.key.E:
            arcade.play_sound(self.initials_input)
            self.inputs.append("E")
            self.inputs.pop(0)
        if symbol == arcade.key.F:
            arcade.play_sound(self.initials_input)
            self.inputs.append("F")
            self.inputs.pop(0)
        if symbol == arcade.key.G:
            arcade.play_sound(self.initials_input)
            self.inputs.append("G")
            self.inputs.pop(0)
        if symbol == arcade.key.H:
            arcade.play_sound(self.initials_input)
            self.inputs.append("H")
            self.inputs.pop(0)
        if symbol == arcade.key.I:
            arcade.play_sound(self.initials_input)
            self.inputs.append("I")
            self.inputs.pop(0)
        if symbol == arcade.key.J:
            arcade.play_sound(self.initials_input)
            self.inputs.append("J")
            self.inputs.pop(0)
        if symbol == arcade.key.K:
            arcade.play_sound(self.initials_input)
            self.inputs.append("K")
            self.inputs.pop(0)
        if symbol == arcade.key.L:
            arcade.play_sound(self.initials_input)
            self.inputs.append("L")
            self.inputs.pop(0)
        if symbol == arcade.key.M:
            arcade.play_sound(self.initials_input)
            self.inputs.append("M")
            self.inputs.pop(0)
        if symbol == arcade.key.N:
            arcade.play_sound(self.initials_input)
            self.inputs.append("N")
            self.inputs.pop(0)
        if symbol == arcade.key.O:
            arcade.play_sound(self.initials_input)
            self.inputs.append("O")
            self.inputs.pop(0)
        if symbol == arcade.key.P:
            arcade.play_sound(self.initials_input)
            self.inputs.append("P")
            self.inputs.pop(0)
        if symbol == arcade.key.Q:
            arcade.play_sound(self.initials_input)
            self.inputs.append("Q")
            self.inputs.pop(0)
        if symbol == arcade.key.R:
            arcade.play_sound(self.initials_input)
            self.inputs.append("R")
            self.inputs.pop(0)
        if symbol == arcade.key.S:
            arcade.play_sound(self.initials_input)
            self.inputs.append("S")
            self.inputs.pop(0)
        if symbol == arcade.key.T:
            arcade.play_sound(self.initials_input)
            self.inputs.append("T")
            self.inputs.pop(0)
        if symbol == arcade.key.U:
            arcade.play_sound(self.initials_input)
            self.inputs.append("U")
            self.inputs.pop(0)
        if symbol == arcade.key.V:
            arcade.play_sound(self.initials_input)
            self.inputs.append("V")
            self.inputs.pop(0)
        if symbol == arcade.key.W:
            arcade.play_sound(self.initials_input)
            self.inputs.append("W")
            self.inputs.pop(0)
        if symbol == arcade.key.X:
            arcade.play_sound(self.initials_input)
            self.inputs.append("X")
            self.inputs.pop(0)
        if symbol == arcade.key.Y:
            arcade.play_sound(self.initials_input)
            self.inputs.append("Y")
            self.inputs.pop(0)
        if symbol == arcade.key.Z:
            arcade.play_sound(self.initials_input)
            self.inputs.append("Z")
            self.inputs.pop(0)

    def fetch_highscores(self):
        f = open(Path("project\game\highscores.txt"), "r")

        self.score_list = f.readlines()
        f.close()

    def update_highscores(self):
        for i in range(len(self.score_list)):
            split_line = self.score_list[i].split()
            if self.curr_score > int(split_line[0]):
                initials = ""
                for char in self.inputs:
                    initials += char
                self.score_list.insert(i, f"{str(self.curr_score)} - {initials}\n")
                self.score_list.pop(-1)
                break
        
        f = open(Path("project\game\highscores.txt"), "w")
        f.writelines(self.score_list)
        f.close()
