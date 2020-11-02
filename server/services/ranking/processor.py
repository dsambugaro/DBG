#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        pass

    def query(self, data):
        pass


