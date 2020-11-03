#!/usr/bin/env python3

import uuid

import yaml
from menu import Menu


class Main:

    dimension = 8

    def start(self):
        with open('config.yaml') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

        if not self.config['UUID']:
            self.config['UUID'] = uuid.uuid4().hex
            with open('config.yaml', 'w') as f:
                yaml.dump(self.config, f)

        self.menu = Menu(self.config)
        self.menu.start()


if __name__ == "__main__":
    main = Main()
    main.start()
