import arcade
from game.director import Game
from pathlib import Path
from game import constants


class InstructionView(arcade.View):
    def on_show(self):
        """ This is run once when we switch to this view """
        # arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.bgm = arcade.load_sound(Path("project/sounds/bgm.mp3"))
        self.button = arcade.load_sound(Path("project/sounds/buttons.wav"))

        arcade.play_sound(self.bgm)
        arcade.schedule(self.play_bgm, 48.0)

        self.setup()

    def setup(self):
        self.larry = arcade.Sprite(Path("project/art/character_ph.png"), constants.SCALE * 3)
        self.larry.center_x = 180
        self.larry.bottom = 100

        self.platform = arcade.Sprite(Path("project/art/sm_platform_ph.png"), constants.SCALE * 0.5)
        self.platform.right = 950
        self.platform.bottom = 400

        self.coin = arcade.Sprite(Path("project/art/coin_ph.png"), constants.SCALE)
        self.coin.right = 915
        self.coin.bottom = 340

        self.enemy = arcade.Sprite(Path("project/art/enemy_ph.png"), constants.SCALE)
        self.enemy.right = 930
        self.enemy.bottom = 250

        self.refill = arcade.Sprite(Path("project/art/refill.png"), constants.SCALE)
        self.refill.right = 915
        self.refill.bottom = 190

    def play_bgm(self, delta_time: float):
        arcade.play_sound(self.bgm)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Leaping Laser Larry", 1350, constants.HEIGHT - 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        self.larry.draw()

        arcade.draw_text("This is Larry.", 450, constants.HEIGHT - 120,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("And your job is to help him escape to the right.", 450, constants.HEIGHT - 170,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Why the right? I don't know.", 450, constants.HEIGHT - 220,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Larry doesn't know either.", 450, constants.HEIGHT - 270,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        self.platform.draw()
        
        arcade.draw_text("Leap from one platform to another to advance.", 1350, 440,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Make sure to not touch the bottom of the screen or else Larry will die.", 1350, 420,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Press A to go left, D to go right, and W to jump.", 1350, 400,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

        self.coin.draw()

        arcade.draw_text("Collect coins to gain a point.", 1160, 350,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

        self.enemy.draw()

        arcade.draw_text("Do not let the enemies touch you, or you'll lose a life.", 1350, 280,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Good thing Larry has three. However, you cannot gain any more.", 1350, 260,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

        self.refill.draw()
        arcade.draw_text("Collect these orbs to recharge your laser. (Now you know why he's Laser Larry)", 1350, 210,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Press SPACE to use a laser charge to kill an enemy and gain 5 points.", 1350, 190,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

        arcade.draw_text("Once you're ready, press SPACE to start.", 1350, 100,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("You can also press Q to quit the game, and P to pause it.", 1350, 70,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            arcade.play_sound(self.button)
            arcade.close_window()
        if symbol == arcade.key.SPACE:
            arcade.play_sound(self.button)
            game_view = Game()
            self.window.show_view(game_view)
