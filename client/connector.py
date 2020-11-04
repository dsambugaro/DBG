#!/usr/bin/env python3


from json import loads, dumps

import paho.mqtt.client as mqtt


class Connector:

    running = False

    def __init__(self, config):
        self.client = mqtt.Client()
        self.UUID = config['UUID']
        self.encoding = config['encoding']
        self.host = config['connection']['host']
        self.port = config['connection']['port']
        self.qos = config['connection']['QoS']
        self.username = config['connection']['username']
        self.pwd = config['connection']['password']

    def stop(self):
        self.running = False
        self.client.disconnect()

    def publish(self, topic, value):
        self.client.publish(topic, value, self.qos)

    def publish_event(self, service, event, data):
        data['clientUUID'] = self.UUID
        self.publish(
            '/DBG/{}/{}'.format(service, event),
            dumps(data).encode(self.encoding)
        )

    def publish_match_event(self, adversary_uuid, data):
        self.publish(
            '/DBG/{}/events'.format(adversary_uuid),
            dumps(data).encode(self.encoding)
        )

    def connect(self):
        if self.username:
            self.client.username_pw_set(self.username, self.pwd)
        self.client.connect(self.host, self.port)

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('/DBG/{}/events'.format(self.UUID))

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode(self.encoding)
        try:
            data = loads(data)
        except ValueError:
            pass
        self.handler(data)

    def setup(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
