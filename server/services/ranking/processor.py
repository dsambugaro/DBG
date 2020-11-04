#!/usr/bin/env python3


from threading import Thread
from time import strftime
import datetime

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
        new_time = datetime.date.today().strftime("%Y-%m-%dT00:00:0.000Z")

        if rank:
            new_rank = rank['score'] + data['score']
            self.db.update(username, {"$set": {"score": new_rank, "last_updated": new_time}})
        else:
            data.pop('clientUUID', None)
            self.db.insert(data)

    def query_by_id(self, data):
        #from id, returns ids general score
        response = {
            'code': 404,
            'msg': 'player not found',
            'result': [],
            'service': 'ranking',
            'event': 'query'
        }

        rank = self.db.find_by_id(data['_id'])

        if rank:
            response['code'] = 200
            response['msg'] ='success'
            response['result'] = rank

        self.manager.publish_event(data['clientUUID'], response)

    def query_by_score(self, data):
        #returns all scores ordered 
        response = {
            'code': 404,
            'msg': 'ranking information not found',
            'result': [],
            'service': 'ranking',
            'event': 'query'
        }

        if (data['order_by']) == 'high':
            ranks = self.db.find_by_score('high')
        else:
            ranks = self.db.find_by_score('low')
        
        if ranks:
            response['code'] = 200
            response['msg'] ='success'
            response['result'] = ranks            

        self.manager.publish_event(data['clientUUID'], response)

    def query_by_date(self, data):
        #returns last updated scores
        response = {
            'code': 404,
            'msg': 'ranking information not found',
            'result': [],
            'service': 'ranking',
            'event': 'query'
        }

        ranks = self.db.find_by_latest()

        if ranks:
            response['code'] = 200
            response['msg'] =''
            response['result'] = ranks            

        self.manager.publish_event(data['clientUUID'], response)