#!/usr/bin/env python3


import platform
from os import system
from time import sleep

from emoji import emojize


class Utils:

    AFFIRMATIVE_ANSWER = ['s', 'sim', 'y', 'yes']
    NEGATIVE_ANSWER = ['n', 'nao', 'não', 'no']

    @classmethod
    def clear(cls):
        """Limpa a janela do terminal de sistemas Windows ou Linux"""
        sys_name = platform.system()
        if sys_name == 'Windows':
            system('cls')
        elif sys_name == 'Linux':
            system('clear')

    @classmethod
    def build_matrix(cls, control_matrix, pretty, show_ships=True):
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
    def show_help(cls):
        Utils.clear()
        print('\n\n')
        print('* * * * * * * * * * * * * * * * * * * * AJUDA * * * * * * * * * * * * * * * * * * * *\n')
        print('-> Para realizar uma jogada digite uma casa do tabuleiro no formato <linha><coluna>')
        print('\tPor exemplo: A1')
        print('-> Para desistir da partida digite "desistir", sem as aspas (")')
        print('\tPor exemplo: desistir')
        print('\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
        input('Pressione enter para continuar ...')

    @classmethod
    def show_wait_message(cls, message, interval=.5):
        print('{}      '.format(message), end='\r')
        sleep(interval)
        print('{} .'.format(message), end='\r')
        sleep(interval)
        print('{} . .'.format(message), end='\r')
        sleep(interval)
        print('{} . . .'.format(message), end='\r')
        sleep(interval)
    
    @classmethod
    def show_ship(cls):
        print(
            '* * * * * * * * * * * * * BATTLESHIP * * * * * * * * * * * * *\n'
            '                                  )___(\n'
            '                           _______/__/_\n'
            '                  ___     /===========|   ___\n'
            ' ____       __   [\\\\\\]___/____________|__[///]   __\n'
            ' \\   \\_____[\\\\]__/___________________________\\__[//]___\n'
            '  \\                                                    |\n'
            '   \\                                                  /\n'
            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
            '* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n'
        )


    @classmethod
    def show_cup(cls):
        print("\t░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
        print("\t░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
        print("\t░░░░░░█████████████████████░░░░░░")
        print("\t░░░░░░░██░░░░░░░░░░░░░░░██░░░░░░░")
        print("\t░░░░░░░░██░░░░░▀█░▀░░░░██░░░░░░░░")
        print("\t░░░░░░░░░██░░░░░█░░░░░██░░░░░░░░░")
        print("\t░░░░░░░░░░██░░░▀▀▀░░░██░░░░░░░░░░")
        print("\t░░░░░░░░░░░██░░░░░░░██░░░░░░░░░░░")
        print("\t░░░░░░░░░░░░░███████░░░░░░░░░░░░░")
        print("\t░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░░")
        print("\t░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░░")
        print("\t░░░░░░░░░░░░░░█████░░░░░░░░░░░░░░")
        print("\t░░░░░░░░░░░░█████████░░░░░░░░░░░░")
        print("\t░░░░░░░░░░█████████████░░░░░░░░░░")
        print("\t░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
        print("\t░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")

    @classmethod
    def show_skull(cls):
        print("\t█████████████████████████████████")
        print("\t███████▀░░░░░░░░░░░░░░░░░▀███████")
        print("\t██████│░░░░░░░░░░░░░░░░░░░│██████")
        print("\t█████▌│░░░░░░░░░░░░░░░░░░░│▐█████")
        print("\t█████░└┐░░░░░░░░░░░░░░░░░┌┘░█████")
        print("\t█████░░└┐░░░░░░░░░░░░░░░┌┘░░█████")
        print("\t█████░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░█████")
        print("\t█████▌░│██████▌░░░▐██████│░▐█████")
        print("\t██████░│▐███▀▀░░▄░░▀▀███▌│░██████")
        print("\t█████▀─┘░░░░░░░▐█▌░░░░░░░└─▀█████")
        print("\t█████▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄█████")
        print("\t███████▄─┘██▌░░░░░░░▐██└─▄███████")
        print("\t████████░░▐█─┬┬┬┬┬┬┬─█▌░░████████")
        print("\t███████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐███████")
        print("\t████████▄░░░└┴┴┴┴┴┴┴┘░░░▄████████")
        print("\t██████████▄░░░░░░░░░░░▄██████████")
        print("\t█████████████████████████████████")
