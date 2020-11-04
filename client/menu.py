#!/usr/bin/env python3

import yaml

from connector import Connector
from utils import Utils
from game import Game


class Menu(Connector):

    dimension = 8

    def __init__(self, config):
        super(Menu, self).__init__(config)
        self.config = config

    def print_ship_art(self):
        Utils.clear()
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

    def config_menu(self, username, message=''):
        # Settings Function
        try:
            self.print_ship_art()
            self.show_alert(message)
            print('* CONFIGURACOES *\n')
            print(
                '1 - EMOJIS -- {}\n'.format(
                    'ON' if self.config['pretty'] else 'OFF'
                )
            )
            print(
                '2 - ENDEREÇO DO SERVIDOR -- {}\n'.format(
                    self.config['connection']['host']
                )
            )
            print(
                '3 - PORTA DO SERVIDOR -- {}\n'.format(
                    self.config['connection']['port']
                )
            )
            print('4 - VOLTAR\n')

            command = input('--> ').strip()
            if command.lower() in ['4', 'voltar']:
                self.logged_in_menu(username)
            elif command.lower() in ['1', 'emojis']:
                try:
                    term = 'DESATIVAR' if self.config['pretty'] else 'ATIVAR'
                    res = input('* {} EMOJIS? (s/N) *\n'.format(term)).strip()
                    if res.lower() in Utils.AFFIRMATIVE_ANSWER:
                        self.config['pretty'] = not self.config['pretty']
                        with open('config.yaml', 'w') as f:
                            yaml.dump(self.config, f)
                        print(
                            '* MODO PRETTY {} *\n'.format(
                                term.replace('R', 'DO'))
                        )
                except KeyboardInterrupt:
                    pass
                finally:
                    self.config_menu(username)

            elif command.lower() in ['2', 'endereço', 'endereço do servidor']:
                try:
                    new_address = input('NOVO ENCEREÇO DO SERVIDOR: ').strip()
                    self.config['connection']['host'] = new_address
                    with open('config.yaml', 'w') as f:
                        yaml.dump(self.config, f)
                    print('ENDEREÇO DO SERVIDOR ALTERADO COM SUCESSO')
                except KeyboardInterrupt:
                    pass
                finally:
                    self.config_menu(username)
            elif command.lower() in ['3', 'porta', 'porta do servidor']:
                try:
                    new_port = int(input('NOVA PORTA DO SERVIDOR: ').strip())
                    self.config['connection']['port'] = new_port
                    with open('config.yaml', 'w') as f:
                        yaml.dump(self.config, f)
                    print('PORTA DO SERVIDOR ALTERADA COM SUCESSO')
                    self.config_menu(username)
                except ValueError:
                    self.config_menu(username, 'Valor inválido para porta')
                except KeyboardInterrupt:
                    self.config_menu(username)

            else:
                # Invalid Command
                self.config_menu(username, 'Comando inválido')
        except KeyboardInterrupt:
            self.logged_in_menu(username)

    def find_ranking(self, username, message='', rank=None):
        try:
            self.print_ship_art()
            self.show_alert(message)

            if rank:
                print('- - - - - - - - - - - - - - - - ')
                print('Usuário\tPontuação\tData')
                for i in range(len(rank)):
                    print(rank['username'][i], rank['score'][i], rank['last_updated'][i])
                print('- - - - - - - - - - - - - - - - \n')
                print('1 - OUTRAS OPÇÕES\n')
                print('2 - VOLTAR\n')
                res = input('--> ').strip()

                if res.lower() in ['1', 'outras opções']:
                    self.find_ranking(username)
                elif res.lower() in ['2', 'voltar']:
                    self.logged_in_menu(username)
                else:
                    self.find_ranking(username, 'Comando inválido', rank)
            else:
                print('1 - BUSCAR POR JOGADOR\n')
                print('2 - RANKING GERAL\n')
                print('3 - NOVAS PONTUAÇÕES\n')
                print('4 - VOLTAR\n')
                res = input('--> ').strip()

                if res.lower() in ['1', 'buscar por jogador']:
                    #find_by_id
                    print('* NOME DO JOGADOR *\n')
                    id_to_find = input('--> ').strip()
                    data = {
                        '_id': id_to_find
                    }
                    self.publish_event('ranking', 'query_by_id', data)
                    self.rank_response = 0

                    while self.rank_response == 0:
                        Utils.show_wait_message('Realizando busca')
                    if self.rank_response == 200:
                        self.find_ranking(username, 'Jogador encontrado', self.rank_data)
                    elif self.rank_response == 404:
                        self.find_ranking(username, 'Jogador não encontrado')
                    else:
                        self.find_ranking(username, 'Erro desconhecido no servidor')

                elif res.lower() in ['2', 'ranking geral']:
                    #find by id (high or low)
                    self.logged_in_menu(username)    

                elif res.lower() in ['3', 'novas pontuações']:
                    #find by latest updates
                    self.publish_event('ranking', 'query_by_date', data)
                    self.rank_response = 0

                    while self.rank_response == 0:
                        Utils.show_wait_message('Realizando busca')
                    if self.rank_response == 200:
                        self.find_ranking(username, 'Informações encontradas', self.rank_data)
                    elif self.rank_response == 404:
                        self.find_ranking(username, 'Informações não encontradas')
                    else:
                        self.find_ranking(username, 'Erro desconhecido no servidor')

                elif res.lower() in ['4', 'voltar']:
                    self.logged_in_menu(username)
                else:
                    self.find_ranking(username, 'Comando inválido', rank)
        except KeyboardInterrupt:
            self.logged_in_menu(username)

    def logged_in_menu(self, username, message=''):
        try:
            self.print_ship_art()
            self.show_alert(message)
            print('1 - BUSCAR JOGADOR\n')
            print('2 - ENCONTRAR PARTIDA\n')
            print('3 - LEADERBOARDS\n')
            print('4 - CONFIGURAÇÕES\n')
            print('5 - SAIR\n')

            command = input('--> ').strip()
            if command.lower() in ['5', 'sair']:
                self.exit()

            elif command.lower() in ['1', 'buscar jogador']:
                # Finding player profile
                self.find_player(username)

            elif command.lower() in ['2', 'encontrar partida']:
                self.find_match(username)

            elif command.lower() in ['3', 'leaderboards']:
                self.find_ranking(username)

            elif command.lower() in ['4', 'configuracoes']:
                self.config_menu(username)

            else:
                # Invalid Command
                self.logged_in_menu(username, 'Comando inválido')
        except KeyboardInterrupt:
            self.exit()
            self.logged_in_menu(username)

    def find_player(self, username, message='', player=None):
        try:
            self.print_ship_art()
            self.show_alert(message)
            if player:
                print('- - - - - - - - - - - - - - - - ')
                print('Nome: {}'.format(player['name']))
                print('Usuário: {}'.format(player['username']))
                print('Pontuação: {}'.format(player['score']))
                print('- - - - - - - - - - - - - - - - \n')
                print('1 - BUSCAR OUTRO JOGADOR\n')
                print('2 - VOLTAR\n')
                res = input('--> ').strip()
                if res.lower() in ['1', 'buscar outro jogador']:
                    self.find_player(username)
                elif res.lower() in ['2', 'voltar']:
                    self.logged_in_menu(username)
                else:
                    self.find_player(username, 'Comando inválido', player)
            else:
                print('* NOME DO JOGADOR *\n')
                username_to_find = input('--> ').strip()
                data = {
                    '_id': username_to_find
                }
                self.publish_event('player', 'info', data)
                self.info_response = 0
                while self.info_response == 0:
                    Utils.show_wait_message('Realizando busca')
                if self.info_response == 200:
                    self.find_player(
                        username, 'Jogador encontrado', self.info_data)
                elif self.info_response == 404:
                    self.find_player(username, 'Jogador não encontrado')
                else:
                    self.find_player(username, 'Erro desconhecido no servidor')
        except KeyboardInterrupt:
            self.logged_in_menu(username)

    def find_match(self, username, message=''):
        try:
            self.print_ship_art()
            self.show_alert(message)
            data = {
                '_id': username
            }
            self.publish_event('match', 'find_game', data)
            self.find_match_response = 0
            while self.find_match_response == 0:
                Utils.show_wait_message('Buscando partida')

            if self.find_match_response == 42:
                self.game = Game(self.dimension, self.config, username)
                self.game.start()
            else:
                self.logged_in_menu(
                    username, 'Erro no servidor ao iniciar partida')

        except KeyboardInterrupt:
            self.publish_event('match', 'cancel_find_game', data)
            self.logged_in_menu(username, 'Busca por partida cancelada')

    def login_menu(self, message=''):
        try:
            self.print_ship_art()
            self.show_alert(message)
            print('* DIGITE SUAS CREDENCIAIS *\n')
            username = input('USUÁRIO: ').strip()
            pwd = input('SENHA: ').strip()
            data = {
                '_id': username,
                'pwd': pwd
            }
            self.publish_event('player', 'login', data)
            self.login_response = 0
            while self.login_response == 0:
                Utils.show_wait_message('Realizando login')
            if self.login_response == 200:
                self.logged_in_menu(username)
            elif self.login_response == 401:
                self.login_menu('Usuário e/ou senha incorreto(s)')
            else:
                self.login_menu('Erro desconhecido no servidor')
        except KeyboardInterrupt:
            self.main_menu()

    def register_menu(self, message=''):
        try:
            self.print_ship_art()
            print('* NOVO JOGADOR *\n')
            self.show_alert(message)
            name = input('NOME: ').strip()
            username = input('USUÁRIO: ').strip()
            pwd = input('SENHA: ').strip()
            data = {
                '_id': username,
                'display_name': name,
                'pwd': pwd
            }
            self.publish_event('player', 'register', data)
            self.register_response = 0
            while self.register_response == 0:
                Utils.show_wait_message('Realizando registro')
            if self.register_response == 201:
                self.logged_in_menu(username)
            elif self.register_response == 406:
                self.register_menu('Usuário já existente')
            else:
                self.register_menu('Erro desconhecido no servidor')
        except KeyboardInterrupt:
            self.main_menu()

    def main_menu(self, message=''):
        try:
            self.print_ship_art()
            self.show_alert(message)
            print('1 - REGISTRAR\n')
            print('2 - LOGAR\n')
            print('3 - SAIR\n')

            command = input('--> ').strip()
            if command.lower() in ['3', 'sair']:
                self.exit()

            elif command.lower() in ['1', 'registrar']:
                # Register new user
                self.register_menu()

            elif command.lower() in ['2', 'logar']:
                # Log into account
                self.login_menu()

            else:
                # Invalid Command
                self.main_menu('Comando inválido')
        except KeyboardInterrupt:
            self.exit()
            self.main_menu()

    def handler(self, data):
        if data['service'] == 'player':
            if data['event'] == 'register':
                self.register_response = data['code']
            if data['event'] == 'login':
                self.login_response = data['code']
            if data['event'] == 'info':
                self.info_data = data['info']
                self.info_response = data['code']
        elif data['service'] == 'ranking':
            if data['event'] == 'query_by_id':
                self.rank_data = data['rank']
                self.rank_response = data['code']
            if data['event'] == 'query_by_date':
                self.rank_data = data['rank']
                self.rank_response = data['code']

    def exit(self):
        res = input('\nDeseja realmente fechar o jogo? (s/N): ').strip()
        if res.lower() in Utils.AFFIRMATIVE_ANSWER:
            Utils.clear()
            exit(0)

    def show_alert(self, message):
        if message:
            print('--> {} <--\n'.format(message))

    def start(self):
        self.setup()
        self.connect()
        self.client.loop_start()
        self.main_menu()
