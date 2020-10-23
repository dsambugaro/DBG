#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt


class Connector:

    host = 'mqtt.eclipse.org'
    port = 1883
    qos = 1

    def __init__(self, topic):
        super(Connector, self).__init__()
        self.topic = topic
        self.client = mqtt.Client()

    def start(self):
        self.running = True
        self.run()

    def stop(self):
        self.running = False
        self.client.disconnect()

    def publish(self, topic, value):
        self.client.publish(topic, value, self.qos)

    def connect(self):
        self.client.connect(self.host, self.port)
