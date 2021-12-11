import arcade
from pyglet import window
from game.director import Game
from game import constants
from game.instruction import InstructionView

if __name__ == "__main__":
    window = arcade.Window(constants.WIDTH, constants.HEIGHT,
                           "Leaping Laser Larry")
    #start_view = Game()
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()
