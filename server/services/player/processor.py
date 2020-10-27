#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from threading import Thread

from ..handler import Handler
from ..database import Database


class Processor(Handler, Thread):
    def __init__(self, manager, event, data):
        super(Processor, self).__init__(event, data)
        self.manager = manager
        self.db = Database('player')

    def ping(self, data):
        if data == 'ping':
            self.manager.ping()

    def register(self, data):
        result = None
        username = data['_id']
        new_player = data.copy()
        new_player['pwd'] = hashlib.sha224(
            data['pwd'].encode('utf-8')).hexdigest()
        new_player.pop('clientUUID', None)
        player = self.db.find_by_id(username)
        response = {
            'msg': 'user registered',
            'code': 201
        }

        if player:
            response['msg'] = 'user already registered'
            response['code'] = 406
            self.manager.publish_event(data['clientUUID'], response)
        else:
            result = self.db.insert(new_player)
            if not result:
                response['msg'] = 'internal server error'
                response['code'] = 500
            self.manager.publish_event(data['clientUUID'], response)

    def login(self, data):
        username = data['_id']
        player = self.db.find_by_id(username)
        response = {
            'msg': 'unauthorized',
            'code': 401
        }
        if player:
            pwd = hashlib.sha224(data['pwd'].encode('utf-8')).hexdigest()
            if player['pwd'] == pwd:
                response['msg'] = 'success'
                response['code'] = 200

        self.manager.publish_event(data['clientUUID'], response)

    def info(self, data):
        username = data['_id']
        player = self.db.find_by_id(username)
        response = {
            'msg': 'User not found',
            'code': 404
        }
        if player:
            response = {
                'username': player['_id'],
                'name': player['display_name'],
                'code': 200
            }
        self.manager.publish_event(data['clientUUID'], response)
