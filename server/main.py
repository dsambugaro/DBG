#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import player

if __name__ == "__main__":
    player_service = player.Manager()
    player_service.start()
