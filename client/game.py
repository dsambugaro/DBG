#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import string
from time import sleep

from kafka import KafkaProducer, KafkaConsumer

from utils import Utils
from board import Board


class Game:

    player_turn = True
    running = False
    encoding = 'utf-8'
    vertical_separator = '\t||\t'
    horizontal_separator = '------------------'

    def __init__(self, dimension, pretty, username, uuid):
        self.username = username
        self.dimension = dimension
        self.pretty = pretty
        self.uuid = uuid
        self.player_board = Board(self.dimension)
        self.oponent_board = Board(self.dimension)
        self._connect()

    def _connect(self):
        try:
            self.producer = KafkaProducer(bootstrap_servers='localhost:1234')
            self.consumer = KafkaConsumer(
                '{}-{}'.format(self.uuid, self.username))
        except Exception:
            self.producer = None
            self.consumer = None

    def _draw_col_indexes(self):
        cols = 1
        print('X', end=' ')
        while cols <= self.dimension:
            print(cols, end=' ')
            cols += 1

    def _set_ships(self):
        done = False
        Utils.clear()
        self.player_board.randomize_ships()
        while not done:
            print('\n\n')
            print('Suas embarcações: ', end='')
            print('{}'.format(self.vertical_separator))
            print(self.horizontal_separator, end='')
            print(self.vertical_separator)
            self._draw_col_indexes()
            print(self.vertical_separator)
            row_letter = 0
            matrix = Utils.build_matrix(
                self.player_board.control_matrix, self.pretty)
            for row in matrix:
                print(string.ascii_uppercase[row_letter], end=' ')
                for cell in row:
                    print(cell, end='' if self.pretty else ' ')
                print(self.vertical_separator)
                row_letter += 1

            print('='*25)
            print('')

            op = input('Reorganizar embarcações aleatóriamente (s/N): ')
            if op.strip().lower() in ['s', 'y', 'sim', 'yes']:
                Utils.clear()
                self.player_board.randomize_ships()
                continue
            op = input('Pronto para iniciar a partida (S/n): ')
            if op.strip().lower() in ['n', 'nao', 'não', 'no']:
                continue
            done = True

    def _draw(self):
        player = Utils.build_matrix(
            self.player_board.control_matrix, self.pretty)
        oponent = Utils.build_matrix(
            self.oponent_board.control_matrix, self.pretty, show_ships=False)

        print('\n\n')
        print('Seu tabuleiro: ', end='')
        print('\t{}'.format(self.vertical_separator), end='')
        print('Tabuleiro oponente: ')
        print(self.horizontal_separator, end='')
        print(self.vertical_separator, end='')
        print(self.horizontal_separator)
        self._draw_col_indexes()
        print(self.vertical_separator, end='')
        self._draw_col_indexes()
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

        print('='*50)
        print('')

    def is_running(self):
        return self.running

    def stop(self):
        self.running = False

    def start(self):
        self.running = True
        self._run()

    def _run(self):

        while self.running:
            Utils.clear()
            self._set_ships()
            self._draw()

            while not self.player_turn:
                print('Turno do oponente      ', end='\r')
                sleep(.5)
                print('Turno do oponente .', end='\r')
                sleep(.5)
                print('Turno do oponente . .', end='\r')
                sleep(.5)
                print('Turno do oponente . . .', end='\r')
                sleep(.5)

            print('Seu turno!')
            has_played = False
            while not has_played:
                move = input('Realize uma jogada (? para obter ajuda): ')
                move = move.strip().lower()
                if move == '?':
                    Utils.show_help()
                    has_played = True
                elif move == 'desistir':
                    answer = input('Deseja realmente desistir (s/N): ')
                    answer = answer.strip()
                    if answer.lower() in ['s', 'sim', 'y', 'yes']:
                        self.stop()
                        has_played = True
                else:
                    if len(move) > 2:
                        print('\nJogada inválida! ', end='')
                        print('Digite uma casa do tabuleiro no formato ', end='')
                        print('<linha><coluna>')
                        print('\tEx: A1\n')
                    elif self.producer:
                        self.producer.send(
                            self.uuid, move.encode(self.encoding))
                    else:
                        has_played = True
