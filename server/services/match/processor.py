#!/usr/bin/env python3


from threading import Thread
from random import getrandbits

from ..handler import Handler


class Processor(Handler, Thread):
    def __init__(self, manager, event, data):
        super(Processor, self).__init__(event, data)
        self.manager = manager

    def ping(self, data):
        if data == 'ping':
            self.manager.ping()

    def new_match(self, data):
        player_one = data['one']
        player_two = data['two']

        response_one = {
            'code': 42,
            'msg': 'match found',
            'adversary': player_two,
            'goes_first': bool(getrandbits(1)),
            'service': 'match',
            'event': 'new_match'
        }

        response_two = response_one.copy()
        response_two['adversary'] = player_one
        response_two['goes_first'] = not response_one['goes_first']

        self.manager.publish_event(
            player_one['clientUUID'], response_one)
        self.manager.publish_event(
            player_two['clientUUID'], response_two)
