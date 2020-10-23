#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread

from ..handler import Handler


class Processor(Handler, Thread):
    def __init__(self, manager, event, data):
        super(Processor, self).__init__(event, data)
        self.manager = manager

    def ping(self, data):
        if data == 'ping':
            self.manager.ping()

    def register(self, data):
        print(data)

    def login(self, data):
        print(data)

    def info(self, data):
        print(data)
