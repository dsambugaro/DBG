#!/usr/bin/env python3


import re
import datetime
from threading import Thread

from ..handler import Handler
from ..database import Database


class Processor(Handler, Thread):
    def __init__(self, manager, event, data):
        super(Processor, self).__init__(event, data)
        self.manager = manager
        self.db = Database('rank')

    def ping(self, data):
        """Função para confirmação de conexão"""
        if data == 'ping':
            self.manager.ping()

    def register(self, data):
        """Registro de ranking
        Atualização de scores
        Inicialização de score para novos jogadores
        """
        username = data['_id']
        rank = self.db.find_by_id(username)
        new_time = datetime.date.today().strftime("%Y-%m-%dT00:00:0.000Z")

        if rank:
            new_rank = rank['score'] + data['score']
            self.db.update(
                username, {"$set": {"score": new_rank, "last_updated": new_time}})
        else:
            data.pop('clientUUID', None)
            self.db.insert(data)

    def query_by_id(self, data):
        """Filtragem de ranking por id
        Recebe id de usuario
        Retorna informações de score
        """
        response = {
            'code': 404,
            'msg': 'player not found',
            'result': [],
            'service': 'ranking',
            'event': 'query'
        }

        rgx = re.compile('.*{}.*'.format(data['_id']), re.IGNORECASE)
        ranks = list(self.db.find({'_id': rgx}))

        if ranks:
            response['code'] = 200
            response['msg'] = 'success'
            response['result'] = ranks

        self.manager.publish_event(data['clientUUID'], response)

    def query_by_score(self, data):
        """Filtragem de ranking por score
        Recebe opção de ordenação (cresc. ou descres.)
        Retorna informações de score ordenados 
        """
        response = {
            'code': 404,
            'msg': 'ranking information not found',
            'result': [],
            'service': 'ranking',
            'event': 'query'
        }

        if (data['order_by']) == 'high':
            ranks = list(self.db.find_by_score('high'))
        else:
            ranks = list(self.db.find_by_score('low'))

        if ranks:
            response['code'] = 200
            response['msg'] = 'success'
            response['result'] = ranks

        self.manager.publish_event(data['clientUUID'], response)

    def query_by_date(self, data):
        """Filtragem de ranking por últimas atualizações
        Retorna informações de score ordenados por data
        """
        response = {
            'code': 404,
            'msg': 'ranking information not found',
            'result': [],
            'service': 'ranking',
            'event': 'query'
        }

        ranks = list(self.db.find_by_latest())

        if ranks:
            response['code'] = 200
            response['msg'] = 'success'
            response['result'] = ranks

        self.manager.publish_event(data['clientUUID'], response)
