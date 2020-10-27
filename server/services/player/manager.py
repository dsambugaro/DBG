#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from threading import Thread

from ..connector import Connector
from .processor import Processor


class Manager(Connector, Thread):

    def __init__(self, log_level=log.INFO):
        super(Manager, self).__init__('player')
        log.basicConfig(
            format='[ Player Service ][ %(levelname)s ] %(message)s', level=log_level)

    def processor(self, event, data):
        return Processor(self, event, data)

    def handler(self, event, data):
        handler = self.processor(event, data)
        handler.start()
