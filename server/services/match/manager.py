#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..connector import Connector
from .processor import Processor


class Manager(Connector):

    def __init__(self):
        super(Manager, self).__init__('match-service')

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('/{}/+'.format(self.topic))

    def on_message(self, client, userdata, msg):
        event = msg.topic.split('/')[-1]
        data = msg.payload.decode('utf-8')
        handler = Processor(event, data)
        handler.start()

    def setup(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def run(self):
        self.setup()
        self.connect()
        self.client.loop_forever()
