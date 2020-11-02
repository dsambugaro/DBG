#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from threading import Thread
from itertools import combinations

from ..connector import Connector
from .processor import Processor


class Manager(Connector, Thread):

    queue = []

    def __init__(self, config, log_level=log.INFO):
        super(Manager, self).__init__('match', config)
        log.basicConfig(
            format='[ Match Service ][ %(levelname)s ] %(message)s',
            level=log_level
        )

    def processor(self, event, data):
        return Processor(self, event, data)

    def handler(self, event, data):
        if event == 'find_game':
            if data not in self.queue:
                self.queue.append(data)
            while len(self.queue) >= 2:
                combinations_list = list(combinations(self.queue, 2))
                players = {
                    'one': combinations_list[0][0],
                    'two': combinations_list[0][1],
                }
                try:
                    self.queue.remove(players['one'])
                    self.queue.remove(players['two'])
                    new_match = self.processor('new_match', players)
                    new_match.start()
                except ValueError:
                    log.error(
                        'O valor ({}|{}) não existe na fila de partida'.format(
                            players['one'], players['two']
                        )
                    )
        else:
            handler = self.processor(event, data)
            handler.start()
