#!/usr/bin/env python3


from threading import Thread

from ..handler import Handler
from ..database import Database


class Processor(Handler, Thread):
    def __init__(self, manager, event, data):
        super(Processor, self).__init__(event, data)
        self.manager = manager
        self.db = Database('rank')

    def ping(self, data):
        if data == 'ping':
            self.manager.ping()

    def register(self, data):
        username = data['_id']
        rank = self.db.find_by_id(username)
        if rank:
            new_rank = rank['score'] + data['score']
            self.db.update(username, {"$set": {"score": new_rank}})
        else:
            data.pop('clientUUID', None)
            self.db.insert(data)

    def query(self, data):
        response = {
            'code': 200,
            'msg': 'success',
            'result': [],
            'service': 'ranking',
            'event': 'query'
        }
        rank = self.db.find_by_id('flame2br')
        response['result'] = rank
        self.manager.publish_event(data['clientUUID'], response)
