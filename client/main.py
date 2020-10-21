#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from game import Game


if __name__ == "__main__":
    dimension = 8
    pretty = True
    game = Game(dimension, pretty)
    game.draw()
