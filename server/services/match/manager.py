#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from threading import Thread

from ..connector import Connector
from .processor import Processor


class Manager(Connector, Thread):

    def __init__(self, log_level=log.INFO):
        super(Manager, self).__init__('match')
        log.basicConfig(
            format='[ Match Service ][ %(levelname)s ] %(message)s', level=log_level)

    def processor(self, event, data):
        return Processor(self, event, data)

    def on_message(self, client, userdata, msg):
        event = msg.topic.split('/')[-1]
        data = msg.payload.decode(self.encoding)
        handler = self.processor(event, data)
        handler.start()
