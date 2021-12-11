import arcade
from game.director import Game
from pathlib import Path


class InstructionView(arcade.View):
    def on_show(self):
        """ This is run once when we switch to this view """
        # arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.bgm = arcade.load_sound(Path("project\sounds\\bgm.mp3"))
        self.button = arcade.load_sound(Path("project\sounds\\buttons.wav"))

        arcade.play_sound(self.bgm)
        arcade.schedule(self.play_bgm, 48.0)

    def play_bgm(self, delta_time: float):
        arcade.play_sound(self.bgm)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Ready To Jump?", self.window.width / 2, self.window.height / 2+75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click here to PLAY", self.window.width / 2, self.window.height / 2+25,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("How to play:", self.window.width / 2, self.window.height / 2-25,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("A = Left; D = Right;  W = Jump", self.window.width / 2, self.window.height / 2-50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Collect coins to get 1 point, avoid enemies to stay alive.", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Jumping on their head however, gives you 5 points.", self.window.width / 2, self.window.height / 2-100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press Q to Quit", self.window.width / 2, self.window.height / 2-125,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Press P to Pause", self.window.width / 2, self.window.height / 2-150,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Game()
        self.window.show_view(game_view)

    
