#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Handler:
    def __init__(self, event, data):
        super(Handler, self).__init__()
        self.event = event
        self.data = data

    def run(self):
        handler = getattr(self, self.event, None)
        if callable(handler):
            handler(self.data)
