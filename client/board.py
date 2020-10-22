#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import random

import numpy as np

from errors import InvalidRow, InvalidCol


class Board:
    """Essa classe representa um tabuleiro de batalha naval"""
    dimension = None
    control_matrix = None

    ships = ['Canoa', 'Canoa', 'Canoa',
             'Lancha', 'Lancha', 'Lancha', 'Navio']
    ship_data = {
        'Canoa': {
            'size': 1,
            'code': 3
        },
        'Lancha': {
            'size': 3,
            'code': 4
        },
        'Navio': {
            'size': 5,
            'code': 5
        }
    }

    def __init__(self, dimension):
        self.dimension = dimension
        self.control_matrix = np.zeros(
            (self.dimension, self.dimension), dtype='int')

    def fire(self, row, col):
        """Realiza uma jogada no tabuleiro.
        Parâmetros:
        row: linha do tabuleiro
        col: coluna do tabuleiro

        Retorna:
        1 caso tenha errado
        2 caso tenha acertado
        0 caso a jogada seja repetida
        """

        if type(row) is str:
            row_upper = row.upper()
            if len(row_upper) == 1 and row_upper in string.ascii_uppercase:
                row_int = string.ascii_uppercase.index(row_upper)
            else:
                row_int = -1
        else:
            row_int = int(row)

        if type(col) is str:
            col_upper = col.upper()
            if len(col_upper) == 1 and col_upper in string.ascii_uppercase:
                col_int = string.ascii_uppercase.index(col_upper)
            else:
                col_int = -1
        else:
            col_int = int(col)

        if row_int >= self.dimension or row_int < 0:
            raise InvalidRow('A linha {} está fora do tabuleiro'.format(row))
        if col_int >= self.dimension or col_int < 0:
            raise InvalidCol('A coluna {} está fora do tabuleiro'.format(col))

        if self.control_matrix[row_int][col_int] == 0:
            self.control_matrix[row_int][col_int] = 1
            return 1
        if self.control_matrix[row_int][col_int] > 2:
            self.control_matrix[row_int][col_int] = 2
            return 2
        return 0

    def set_ship(self, start, end, ship):
        if start[0] == end[0]:
            row = start[0]
            for col in range(start[1], end[1]+1):
                if self.control_matrix[row][col] > 0:
                    return False
            for col in range(start[1], end[1]+1):
                self.control_matrix[row][col] = ship

        elif start[1] == end[1]:
            col = start[1]
            for row in range(start[0], end[0]+1):
                if self.control_matrix[row][col] > 0:
                    return False
            for row in range(start[0], end[0]+1):
                self.control_matrix[row][col] = ship

        return True

    def randomize_ships(self):
        self.control_matrix = np.zeros(
            (self.dimension, self.dimension), dtype='int')

        for ship in self.ships:
            done = False
            while not done:
                rotation = random.randint(0, 1)
                row = random.randint(0, 7)
                col = random.randint(0, 7)

                if rotation > 0:
                    new_col = col + self.ship_data[ship]['size'] - 1
                    if new_col < self.dimension:
                        if self.set_ship((row, col), (row, new_col), self.ship_data[ship]['code']):
                            done = True
                    elif col - self.ship_data[ship]['size'] + 1 >= 0:
                        new_col = col - self.ship_data[ship]['size'] + 1
                        if self.set_ship((row, new_col), (row, col), self.ship_data[ship]['code']):
                            done = True

                else:
                    new_row = row + self.ship_data[ship]['size'] - 1
                    if new_row < self.dimension:
                        if self.set_ship((row, col), (new_row, col), self.ship_data[ship]['code']):
                            done = True
                    elif row - self.ship_data[ship]['size'] + 1 >= 0:
                        new_row = row - self.ship_data[ship]['size'] + 1
                        if self.set_ship((new_row, col), (row, col), self.ship_data[ship]['code']):
                            done = True
