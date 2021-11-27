import arcade
from game.director import Game


class InstructionView(arcade.View):
    def on_show(self):
        """ This is run once when we switch to this view """
        # arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2+50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Press Q to Quit", self.window.width / 2, self.window.height / 2+15,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Press P to Pause", self.window.width / 2, self.window.height / 2-15,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Click here to PLAY", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Game()
        # game_view.setup()
        self.window.show_view(game_view)
