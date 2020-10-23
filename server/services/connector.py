#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt


class Connector:

    encoding = 'utf-8'
    host = 'mqtt.eclipse.org'
    port = 1883
    qos = 1

    def __init__(self, topic):
        super(Connector, self).__init__()
        self.topic = topic
        self.client = mqtt.Client()

    def stop(self):
        self.running = False
        self.client.disconnect()

    def ping(self):
        self.client.publish('/{}/pong'.format(self.topic),
                            'pong'.encode(self.encoding), self.qos)

    def publish(self, topic, value):
        self.client.publish(topic, value, self.qos)

    def connect(self):
        self.client.connect(self.host, self.port)

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('/DBG/{}/+'.format(self.topic))

    def setup(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def run(self):
        self.setup()
        self.connect()
        self.client.loop_forever()
