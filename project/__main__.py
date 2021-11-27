import arcade
from pyglet import window
from game.director import Game
from game import constants
from game.instruction import InstructionView

if __name__ == "__main__":
    window = arcade.Window(constants.WIDTH, constants.HEIGHT,
                           "Infinite Side Scroller Platform Jumping Game")
    #start_view = Game()
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()
