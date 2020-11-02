#!/usr/bin/env python3


import yaml
import logging as log
from time import sleep

from services import player, match, ranking


class Main:
    services_poll = []

    def __init__(self, log_level=log.INFO):
        log.basicConfig(
            format='[ Servidor ][ %(levelname)s ] %(message)s', level=log_level)

    def start(self):
        log.info('Carregando configurações')
        self.config = yaml.load(
            open('config.yaml', 'r'), Loader=yaml.FullLoader)
        log.info('Iniciando servidor')
        self.services_poll = [player, match, ranking]
        log.info('Criando instancia dos serviços')
        self.services_poll = [service.Manager(self.config)
                              for service in self.services_poll]
        log.info('Iniciando serviços')
        for service in self.services_poll:
            service.start()
        log.info('Servidor iniciado, Ctrl + C para parar a execução ...')

    def join(self):
        for service in self.services_poll:
            service.join()

    def stop(self):
        log.info('Parando execução do servidor')
        for service in self.services_poll:
            service.stop()
        log.info('Até logo e obrigado pelos peixes!')


if __name__ == "__main__":
    server = Main()
    server.start()
    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        server.stop()
