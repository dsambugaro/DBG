#!/usr/bin/env python3


import string

from utils import Utils
from board import Board
from connector import Connector
from errors import InvalidRow, InvalidCol


class Game(Connector):

    last_result = -1
    have_adversary_ships = False
    oponent_gave_up = False
    wins = False
    loses = False
    vertical_separator = '\t||\t'
    horizontal_separator = '------------------'

    def __init__(self, dimension, config, username, adversary, player_turn):
        super(Game, self).__init__(config)
        self.username = username
        self.dimension = dimension
        self.adversary = adversary
        self.player_turn = player_turn
        self.encoding = config['encoding']
        self.pretty = config['pretty']
        self.uuid = config['UUID']
        self.player_board = Board(self.dimension)
        self.oponent_board = Board(self.dimension)

    def _draw_col_indexes(self):
        cols = 1
        print('X', end=' ')
        while cols <= self.dimension:
            print(cols, end=' ')
            cols += 1

    def give_up(self):
        answer = input('Deseja realmente desistir (s/N): ')
        answer = answer.strip()
        if answer.lower() in Utils.AFFIRMATIVE_ANSWER:
            data = {
                'code': 51,
                'msg': 'give up',
                'event': 'move'
            }
            self.publish_match_event(
                self.adversary['clientUUID'], data
            )
            return True
        return False

    def _set_ships(self):
        done = False
        Utils.clear()
        self.player_board.randomize_ships()
        while not done:
            try:
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
                if op.strip().lower() in Utils.AFFIRMATIVE_ANSWER:
                    Utils.clear()
                    self.player_board.randomize_ships()
                    continue
                op = input('Pronto para iniciar a partida (S/n): ')
                if op.strip().lower() in Utils.NEGATIVE_ANSWER:
                    Utils.clear()
                    continue
                done = True
            except KeyboardInterrupt:
                if self.give_up():
                    self.stop()
                    break
                else:
                    continue

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

        for row in range(self.dimension):
            print(string.ascii_uppercase[row], end=' ')
            for cell in player[row]:
                print(cell, end='' if self.pretty else ' ')
            print(self.vertical_separator, end='')
            print(string.ascii_uppercase[row], end=' ')
            for cell in oponent[row]:
                print(cell, end='' if self.pretty else ' ')
            print('')

        print('='*50)
        print('')

    def is_running(self):
        return self.running

    def start(self):
        self.running = True
        self.setup()
        self.connect()
        self.client.loop_start()
        self._run()

    def handler(self, data):
        if data['event'] == 'set_board':
            if data['code'] == 13:
                self.oponent_board.control_matrix = data['matrix']
                self.have_adversary_ships = True
        if data['event'] == 'move':
            if data['code'] == 22:
                move = data['move']
                self.player_board.fire(move['row'], move['col'])
                self.player_turn = True
            elif data['code'] == 51:
                self.oponent_gave_up = True
                self.wins = True

    def _run(self):
        self._set_ships()
        data = {
            'code': 13,
            'matrix': self.player_board.control_matrix,
            'event': 'set_board'
        }
        self.publish_match_event(
            self.adversary['clientUUID'], data
        )
        print('Oponente: {}'.format(self.adversary['_id']))
        while not self.have_adversary_ships:
            try:
                Utils.show_wait_message(
                    'Aguardando {} posicionar os navios'.format(
                        self.adversary['_id']
                    )
                )
                if self.oponent_gave_up:
                    break
            except KeyboardInterrupt:
                if self.give_up():
                    self.stop()
                    break
                else:
                    continue

        while self.running:
            Utils.clear()
            self._draw()

            if self.last_result == 1:
                print('\nTiro na água!\n')
            elif self.last_result == 3:
                print('\nAcertou uma Canoa!\n')
            elif self.last_result == 4:
                print('\nAcertou uma Lancha!\n')
            elif self.last_result == 5:
                print('\nAcertou um Navio!\n')

            if not self.oponent_board.is_over():
                while not self.player_turn:
                    try:
                        Utils.show_wait_message(
                            'Turno do oponente - {} - {}'.format(
                                self.adversary['_id'], self.oponent_gave_up
                            )
                        )
                        if self.oponent_gave_up:
                            break
                    except KeyboardInterrupt:
                        if self.give_up():
                            self.stop()
                            break
                        else:
                            continue

            if self.oponent_gave_up:
                print(
                    ' * O oponente {} desistiu da partida * '.format(
                        self.adversary['_id']
                    )
                )

            if self.oponent_board.is_over():
                self.wins = True
                self.loses = False
            elif self.player_board.is_over():
                self.loses = True
                self.wins = False

            if self.wins:
                Utils.show_cup()
                data = {
                    '_id': self.username,
                    'score': 5
                }
                self.publish_event('ranking', 'register', data)
                input('\nPressione enter para continuar ...')
                self.stop()
                continue

            if self.loses:
                Utils.show_skull()
                input('\nPressione enter para continuar ...')
                self.stop()
                continue

            Utils.clear()
            self._draw()

            print('Seu turno!')
            has_played = False
            while not has_played:
                try:
                    move = input('Realize uma jogada (? para obter ajuda): ')
                    move = move.strip().lower()
                    if move == '?':
                        Utils.show_help()
                        has_played = True
                    elif move == 'desistir':
                        if self.give_up():
                            self.stop()
                            break
                        else:
                            continue
                    else:
                        if len(move) != 2:
                            print('\nJogada inválida! ', end='')
                            print('Digite uma casa do tabuleiro no ', end='')
                            print('formato <linha><coluna>')
                            print('\tEx: A1\n')
                        else:
                            try:
                                self.last_result = self.oponent_board.fire(
                                    move[0], int(move[1])
                                )
                                if self.last_result > 0:
                                    data = {
                                        'code': 22,
                                        'move': {
                                            'row': move[0],
                                            'col': int(move[1])
                                        },
                                        'event': 'move'
                                    }
                                    self.publish_match_event(
                                        self.adversary['clientUUID'], data
                                    )
                                    has_played = True
                                    self.player_turn = False
                                else:
                                    print('\nJogada já realizada!\n')
                            except InvalidRow:
                                print('\nJogada inválida! ', end='')
                                print(
                                    'A linha {} não existe no tabuleiro\n'.format(
                                        move[0]
                                    )
                                )
                            except InvalidCol:
                                print('\nJogada inválida! ', end='')
                                print(
                                    'A coluna {} não existe no tabuleiro\n'.format(
                                        move[1]
                                    )
                                )
                            except ValueError:
                                print('\nJogada inválida! ', end='')
                                print('Digite uma casa do tabuleiro no ', end='')
                                print('formato <linha><coluna>')
                                print('\tEx: A1\n')
                except KeyboardInterrupt:
                    if self.give_up():
                        self.stop()
                        break
                    else:
                        continue
