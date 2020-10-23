#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import match  # noqa
from . import player  # noqa
from . import ranking  # noqa

from .handler import Handler  # noqa
from .database import Database  # noqa
from .connector import Connector  # noqa

__all__ = ['player', 'match', 'ranking', 'database.Database',
           'handler.Handler', 'connector.Connector']
__name__ = 'services'
__package__ = ''
