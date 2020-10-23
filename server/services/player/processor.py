#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process

from ..handler import Handler


class Processor(Handler, Process):
    def __init__(self, event, data):
        super(Processor, self).__init__(event, data)

    def register(self, data):
        print(data)

    def login(self, data):
        print(data)

    def info(self, data):
        print(data)
