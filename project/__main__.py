from game.director import Game
from game import constants

if __name__ == "__main__":
    app = Game(constants.WIDTH, constants.HEIGHT, "Infinite Side Scroller Platform Jumping Game")
    app.run()
