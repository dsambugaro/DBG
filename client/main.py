#!/usr/bin/env python3



from game import Game


if __name__ == "__main__":
    dimension = 8
    pretty = True
    game = Game(dimension, pretty, 'dsambugaro', 'UUID')
    game.start()
