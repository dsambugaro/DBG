#!/usr/bin/env python3


from json import loads, dumps

import paho.mqtt.client as mqtt


class Connector:

    def __init__(self, topic, config):
        super(Connector, self).__init__()
        self.topic = topic
        self.client = mqtt.Client()
        self.encoding = config['encoding']
        self.host = config['connection']['host']
        self.port = config['connection']['port']
        self.qos = config['connection']['QoS']

    def stop(self):
        self.running = False
        self.client.disconnect()

    def ping(self):
        self.client.publish('/DBG/{}/pong'.format(self.topic),
                            'pong'.encode(self.encoding), self.qos)

    def publish(self, topic, value):
        self.client.publish(topic, value, self.qos)

    def publish_event(self, uuid, response):
        self.publish(
            '/DBG/{}/events'.format(uuid),
            dumps(response).encode(self.encoding)
        )

    def connect(self):
        self.client.connect(self.host, self.port)

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('/DBG/{}/+'.format(self.topic))

    def on_message(self, client, userdata, msg):
        event = msg.topic.split('/')[-1]
        data = msg.payload.decode(self.encoding)
        try:
            data = loads(data)
        except ValueError:
            pass
        self.handler(event, data)

    def setup(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def run(self):
        self.setup()
        self.connect()
        self.client.loop_forever()
