#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import string

from utils import Utils
from board import Board


class Game:

    vertical_separator = '\t||\t'
    horizontal_separator = '------------------'

    def __init__(self, dimension, pretty):
        self.dimension = dimension
        self.pretty = pretty
        self.player_board = Board(self.dimension)
        self.oponent_board = Board(self.dimension)

    def _draw_col_indexes(self, dimension):
        cols = 1
        print('X', end=' ')
        while cols <= dimension:
            print(cols, end=' ')
            cols += 1

    def draw(self):
        player = Utils.build_matrix(
            self.player_board.control_matrix, self.pretty)
        oponent = Utils.build_matrix(
            self.oponent_board.control_matrix, self.pretty)

        print('Seu tabuleiro: ', end='')
        print('\t{}'.format(self.vertical_separator), end='')
        print('Tabuleiro oponente: ')
        print(self.horizontal_separator, end='')
        print(self.vertical_separator, end='')
        print(self.horizontal_separator)
        self._draw_col_indexes(self.dimension)
        print(self.vertical_separator, end='')
        self._draw_col_indexes(self.dimension)
        print('')

        row_letter = 0
        for row in player:
            print(string.ascii_uppercase[row_letter], end=' ')
            for cell in row:
                print(cell, end='' if self.pretty else ' ')
            print(self.vertical_separator, end='')
            print(string.ascii_uppercase[row_letter], end=' ')
            for cell in oponent[0]:
                print(cell, end='' if self.pretty else ' ')
            print('')
            row_letter += 1
