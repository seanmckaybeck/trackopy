__title__ = 'trackopy'
__version__ = '1.1.1'
__author__ = 'Sean Beck'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Sean Beck'

from .trackobot import Trackobot

__all__ = ['Trackobot']

import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

