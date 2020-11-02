#!/usr/bin/env python3


class InvalidRow(Exception):
    def __init__(self, row):
        if row:
            self.row = row
            self.message = 'Linha inválida: {} está fora do tabuleiro'.format(
                self.row)
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Uma exceção de "Linha inválida" ocorreu'


class InvalidCol(Exception):
    def __init__(self, col):
        if col:
            self.col = col
            self.message = 'Coluna inválida: {} está fora do tabuleiro'.format(
                self.col)
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Uma exceção de "Coluna inválida" ocorreu'
