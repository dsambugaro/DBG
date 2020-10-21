#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string

import numpy as np

from errors import InvalidRow, InvalidCol


class Board:
    """Essa classe representa um tabuleiro de batalha naval"""
    dimension = None
    control_matrix = None

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
