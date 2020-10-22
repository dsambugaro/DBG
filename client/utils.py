#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
from os import system

from emoji import emojize


class Utils:

    @classmethod
    def clear(self):
        """Limpa a janela do temrinal de sistemas Windows ou Linux"""
        sys_name = platform.system()
        if sys_name == 'Windows':
            system('cls')
        elif sys_name == 'Linux':
            system('clear')

    @classmethod
    def build_matrix(self, control_matrix, pretty, show_ships=True):
        pretty_chars = [':droplet:', ':cross_mark:',
                        ':fire:', ':canoe:', ':speedboat:', ':ship:']
        chars = ['~', 'X', 'O', 'B']
        matrix = []
        if pretty:
            for control_row in control_matrix:
                row = []
                for cell in control_row:
                    if not show_ships and cell > 2:
                        row.append(emojize(pretty_chars[0]))
                    else:
                        row.append(emojize(pretty_chars[cell]))
                matrix.append(row)
            return matrix

        for control_row in control_matrix:
            row = []
            for cell in control_row:
                if cell > 2:
                    if not show_ships:
                        row.append(chars[0])
                    else:
                        row.append(chars[3])
                else:
                    row.append(chars[cell])
            matrix.append(row)
        return matrix

    @classmethod
    def show_help(self):
        Utils.clear()
        print('\n\n')
        print('* * * * * * * * * * * * * * * * * * * * AJUDA * * * * * * * * * * * * * * * * * * * *\n')
        print('-> Para realizar uma jogada digite uma casa do tabuleiro no formato <linha><coluna>')
        print('\tPor exemplo: A1')
        print('-> Para desistir da partida digite "desistir", sem as aspas (")')
        print('\tPor exemplo: desistir')
        print('\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
        input('Pressione enter para continuar ...')
