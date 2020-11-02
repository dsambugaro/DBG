#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import Utils


class menu:

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

    def config_menu(self):
        # Settings Function
        self.print_ship_art()
        print('* CONFIGURACOES *\n')
        print('MODO PRETTY\n')
        print('PORT/IP\n')
        print('SAIR\n')

        while True:
            command = input('--> ').strip()
            if 'sair' == command.lower():
                # Exit Game
                break

            elif 'modo pretty' == command.lower():
                print('* ATIVAR MODO PRETTY? (TABULEIRO COM EMOJIS) *\n')
                command = input('Y/N --> ').strip()
                if 'y' == command.lower():
                    # Activate pretty mode
                    print('* MODO PRETTY ATIVADO *\n')
                else:
                    # Deactivate pretty mode
                    print('* MODO PRETTY DESATIVADO *\n')

            elif 'port/ip' == command.lower():
                # PORT/IP FUNCTIONS
                print('* DEFINICOES DE PORTA E IP *\n')

            else:
                # Invalid Command
                print('\nComando inválido\n')

    def logged_in_menu(self):
        self.print_ship_art()
        print('BUSCAR JOGADOR\n')
        print('ENCONTRAR PARTIDA\n')
        print('CONFIGURACOES')
        print('SAIR\n')

        while True:
            command = input('--> ').strip()
            if 'sair' == command.lower():
                # Exit Game
                break

            elif 'buscar jogador' == command.lower():
                # Finding player profile
                self.print_ship_art()
                print('* NOME DO JOGADOR *\n')
                command = input('--> ').strip()

            elif 'encontrar partida' == command.lower():
                # Matchmaking Function
                self.print_ship_art()
                print('* ENCONTRANDO PARTIDA *\n')

            elif 'configuracoes' == command.lower():
                self.config_menu()

            else:
                # Invalid Command
                print('\nComando inválido\n')

    def login_menu(self):
        self.print_ship_art()
        print('* JOGADOR EXISTENTE *\n')
        self.username = input('USERNAME: ').strip()
        self.senha = input('SENHA: ').strip()

        if 'USERNAME' == True and 'SENHA' == True:
            # Database Verification
            print('* LOG SUCCESS *\n')
            self.logged_in_menu()
        else:
            print('* LOG FAILED *')

    def register_menu(self):
        self.print_ship_art()
        print('* NOVO JOGADOR *\n')
        self.username = input('USERNAME: ').strip()
        self.senha = input('SENHA: ').strip()
        # New User Function
        self.logged_in_menu()

    def main_menu(self):
        self.print_ship_art()
        print('REGISTRAR\n')
        print('LOGAR\n')
        print('SAIR\n')

        while True:
            command = input('--> ').strip()
            if 'sair' == command.lower():
                # Exit Game
                break

            elif 'registrar' == command.lower():
                # Register new user
                self.register_menu()

            elif 'logar' == command.lower():
                # Log into account
                self.logged_in_menu()

            else:
                # Invalid Command
                print('\nComando inválido\n')
